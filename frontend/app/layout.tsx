import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'BIS Standards Recommendation Engine',
  description: 'AI-Powered Procurement Specifications Recommendation Engine for Smart India Hackathon 2026',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col">{children}</body>
    </html>
  );
}
