"use client";

import React from 'react'
import { Button } from '../ui/button'
import { signIn, signOut } from 'next-auth/react'
import Link from 'next/link';

export const LoginGithub = () => {
  return (
    <Button 
      onClick={() => signIn('github', { callbackUrl: '/dashboard' })} 
      variant="outline" 
      className="w-full"
    >
      Login with Github
    </Button>
  )
}

export const LogoutGithub = () => {
  return (
    <Link href={'/'}
      onClick={() => {signOut({redirectTo: '/'})}} 
      className="w-full block"
    >
      Logout
    </Link>
  )
}
