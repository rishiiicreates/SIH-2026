import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Manak - BIS Standards Recommendation Engine',
  description: 'AI-Powered Indian Standards Recommendation Engine for Procurement & Tenders',
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
