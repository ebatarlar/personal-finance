import NextAuth from "next-auth"
import GitHub from "next-auth/providers/github"
import Credentials from "next-auth/providers/credentials"
import { userService } from "@/services/userService"
import { authService } from "@/services/authService";
import { Session } from "next-auth";
import { JWT } from "next-auth/jwt"

// Extend the JWT type to include our custom properties
declare module "next-auth/jwt" {
  interface JWT {
    error?: string;
    access_token?: string;
    refresh_token?: string;
    expires_at?: number;
  }
}

// Extend the Session type to include our custom properties
declare module "next-auth" {
  interface Session {
    error?: string;
    tokens?: {
      access_token: string;
      refresh_token: string;
    } | null;
  }
}

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    GitHub,
    Credentials({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        try {
          if (!credentials?.email || !credentials?.password) {
            throw new Error("Missing credentials");
          }

          const tokens = await authService.login({
            email: credentials.email as string,
            password: credentials.password as string,
          });

          if (tokens) {
            // Get user data after successful login
            const user = await userService.getUserByEmail(credentials.email as string);
            
            if (!user) {
              throw new Error("User not found");
            }

            // Return user object with tokens

            return {
              ...user,
              access_token: tokens.access_token,   
              refresh_token: tokens.refresh_token   
            };
          }
          return null;
        } catch (error) {
          console.error("Authentication error:", error);
          return null;
        }
      }
    })
  ],
  callbacks: {
    async signIn({ user, account }) {
      if (account?.provider === "credentials") {
        return !!user;
      }

      if (account?.provider === "github") {
        try {
          if (!user.email || !user.id) {
            throw new Error('Missing required user data');
          }

          // Store user in MongoDB
          await userService.register({
            email: user.email,
            name: user.name?.split(" ")[0] ?? "",
            surname: user.name?.split(" ").slice(1).join(" ") ?? "",
            oauth_info: {
              provider: "github",
              provider_user_id: user.id
            }
          });

          // login
          const tokenData = await userService.oauthLogin({
            email: user.email!,
            name: user.name?.split(" ")[0] ?? "",
            surname: user.name?.split(" ").slice(1).join(" ") ?? "",
          }, {
            provider: "github",
            provider_user_id: user.id!
          });

          if (tokenData) {
            // Store tokens temporarily in user object
            (user as any).access_token = tokenData.access_token;
            (user as any).refresh_token = tokenData.refresh_token;
            return true;
          }
        } catch (error) {
          console.error("Error storing user in MongoDB:", error);
          return false;
        }
      }
      return true;
    },
    async jwt({ token, user }) {
      if (user) {
        return {
          ...token,
          ...user,
          expires_at: Math.floor(Date.now() / 1000 + 15 * 60), // 15 minutes from now
        };
      }

      // Return previous token if the access token has not expired yet
      if (typeof token.expires_at === 'number' && Date.now() < token.expires_at * 1000) {
        return token;
      }

      // Access token has expired, try to refresh it
      try {
        if (!token.refresh_token) {
          return { ...token, error: "NoRefreshTokenError" };
        }

        const tokens = await authService.refreshAccessToken(token.refresh_token);
        if (!tokens) {
          return { ...token, error: "RefreshAccessTokenError" };
        }

        return {
          ...token,
          access_token: tokens.access_token,
          refresh_token: tokens.refresh_token,
          expires_at: tokens.expires_at,
        };
      } catch (error) {
        console.error("Error refreshing access token:", error);
        return { ...token, error: "RefreshAccessTokenError" };
      }
    },
    async session({ session, token }) {
      // Add user data from MongoDB to the session
      if (session.user?.email) {
        try {
          const mongoUser = await userService.getUserByEmail(session.user.email);
          if (mongoUser) {
            session.user.id = mongoUser.id;
          }
        } catch (error) {
          console.error("Error fetching user from MongoDB:", error);
        }
      }

      // Add tokens to the session
      if (token.error) {
        // If there was an error refreshing the access token
        session.error = token.error;
        session.tokens = null;
      } else if (token.access_token && token.refresh_token) {
        session.tokens = {
          access_token: token.access_token as string,
          refresh_token: token.refresh_token as string,
        };
        session.error = undefined;
      } else {
        session.tokens = null;
        session.error = undefined;
      }

      return session;
    }
  }
})