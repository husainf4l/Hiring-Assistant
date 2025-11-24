import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Hiring Assistant - AI-Powered Job Matching',
  description: 'Modern AI-powered hiring assistant for job matching and candidate discovery',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="app-body">
        {children}
      </body>
    </html>
  )
}


