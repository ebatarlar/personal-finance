import NextAuth from "next-auth"
import GitHub from "next-auth/providers/github"
import { userService } from "@/services/userService"
import { authService } from "@/services/authService";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [GitHub],
  callbacks: {
    

    async signIn({ user, account }) {
      if (account?.provider === "github") {
        try {
          // Store user in MongoDB
          await userService.createOrUpdateUser({
            email: user.email!,
            name: user.name?.split(" ")[0] ?? "",
            surname: user.name?.split(" ").slice(1).join(" ") ?? "",
            oauth_info: {
              provider: "github",
              provider_user_id: user.id
            }
          });
         
          //console.log("User stored in MongoDB:", user);

          // login
          const tokenData = await userService.loginByOAuth({
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
      
      // Initial sign in
      if (user) {
        // Pass the tokens from user to the token
        token.access_token = (user as any).access_token as string;
        token.refresh_token = (user as any).refresh_token as string;
        return token;
      }

      // Return previous token if it's not expired
      if (Date.now() < ((token as any).expires_at ?? 0) * 1000) {
        return token;
      }

      // Token has expired, try to refresh it
      try {
        const response = await fetch('http://localhost:8000/api/token/refresh', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ refresh_token: token.refresh_token }),
        });

        if (!response.ok) {
          return { ...token, error: "RefreshAccessTokenError" };
        }

        const tokens = await response.json();
        return {
          ...token,
          access_token: tokens.access_token,
          refresh_token: tokens.refresh_token,
          expires_at: Math.floor(Date.now() / 1000 + 15 * 60), // 15 minutes from now
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
      if (token.access_token && token.refresh_token) {
        session.tokens = {
          access_token: token.access_token as string,
          refresh_token: token.refresh_token as string,
        };
      } else {
        session.tokens = null;
      }

      return session;
    }
  }
})