import NextAuth from "next-auth"
import GitHub from "next-auth/providers/github"
import { userService } from "@/services/userService"

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [GitHub],
  callbacks: {
    async signIn({ user, account }) {
      if (account?.provider === "github") {
        try {
          // Store user in MongoDB
          await userService.createOrUpdateUser({
            email: user.email!,
            name: user.name!,
            github_id: account.providerAccountId
          });
          return true;
        } catch (error) {
          console.error("Error storing user in MongoDB:", error);
          // Still allow sign in even if MongoDB storage fails
          return true;
        }
      }
      return true;
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
      return session;
    }
  }
})