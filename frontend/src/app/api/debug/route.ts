import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    nextauth_url: process.env.NEXTAUTH_URL,
    has_github_id: !!process.env.AUTH_GITHUB_ID,
    has_github_secret: !!process.env.AUTH_GITHUB_SECRET,
    has_nextauth_secret: !!process.env.NEXTAUTH_SECRET,
    api_url: process.env.NEXT_PUBLIC_API_URL,
  });
}
