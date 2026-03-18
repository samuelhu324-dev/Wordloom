import type { Metadata } from 'next';
import { Providers } from './providers';
import { defaultLanguage } from '@/i18n/config';
import '@/shared/styles/globals.css';

export const metadata: Metadata = {
  title: 'Wordloom',
  description: 'Knowledge Management System',
};

const normalizeOrigin = (value: string): string => value.replace(/\/+$/, '');
const rawApiOrigin = process.env.API_PROXY_TARGET || process.env.NEXT_PUBLIC_API_BASE || '';
const apiOrigin = rawApiOrigin ? normalizeOrigin(rawApiOrigin) : null;
const shouldPreconnect = apiOrigin != null && !/localhost|127\.0\.0\.1/i.test(apiOrigin);

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang={defaultLanguage} data-theme="silk-blue">
      <head>
        {shouldPreconnect ? <link rel="preconnect" href={apiOrigin} /> : null}
      </head>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
