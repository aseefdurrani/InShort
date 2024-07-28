import './globals.css'; // Ensure the correct path

export const metadata = {
  title: 'InShort',
  description: 'Always in the loop',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
