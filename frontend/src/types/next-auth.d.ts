import NextAuth from "next-auth"

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      email: string;
      name: string;
      image?: string;
    }
    tokens?: {
      access_token: string;
      refresh_token: string;
    } | null
  }
  
  interface User {
    id: string;
    email: string;
    name: string;
    image?: string;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    access_token?: string;
    refresh_token?: string;
  }
}
