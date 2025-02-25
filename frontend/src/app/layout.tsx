import type { Metadata } from "next"
import localFont from "next/font/local"
import { Providers } from "@/components/providers"

import "./globals.css"


const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
})
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
})

export const metadata: Metadata = {
  title: "Personal Finance App",
  description: "Manage your personal finances",
}

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  
  
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${geistSans.variable} font-geist-sans`}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
