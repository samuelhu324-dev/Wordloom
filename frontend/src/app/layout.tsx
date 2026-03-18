import type { Metadata } from 'next';
import { Providers } from './providers';
import { defaultLanguage } from '@/i18n/config';
import '@/shared/styles/globals.css';

const normalizeOrigin = (value: string): string => value.replace(/\/+$/, '');
const withHttps = (value: string): string => (value.startsWith('http://') || value.startsWith('https://') ? value : `https://${value}`);

const rawSiteOrigin =
  process.env.NEXT_PUBLIC_SITE_URL ||
  process.env.VERCEL_PROJECT_PRODUCTION_URL ||
  process.env.VERCEL_URL ||
  'https://wordloom-v3.vercel.app';

const siteOrigin = normalizeOrigin(withHttps(rawSiteOrigin));

export const metadata: Metadata = {
  title: 'Wordloom',
  description: 'Knowledge Management System',
  metadataBase: new URL(siteOrigin),
};

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
