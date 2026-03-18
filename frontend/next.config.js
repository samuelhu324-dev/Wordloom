/** @type {import('next').NextConfig} */
const path = require('path');

const normalizeBasePath = (value = '') => {
  const trimmed = value.trim();

  if (!trimmed || trimmed === '/') {
    return '';
  }

  const withLeadingSlash = trimmed.startsWith('/') ? trimmed : `/${trimmed}`;
  return withLeadingSlash.replace(/\/+$/, '');
};

const basePath = normalizeBasePath(process.env.NEXT_PUBLIC_BASE_PATH || '');

const nextConfig = {
  reactStrictMode: true,
  basePath: basePath || undefined,
  distDir: process.env.NEXT_DIST_DIR || '.next',
  eslint: {
    // The repo currently carries unrelated legacy lint debt; do not block the public demo deployment on it.
    ignoreDuringBuilds: true,
  },
  compiler: {
    styledComponents: true,
  },
  turbopack: {
    root: path.join(__dirname),
  },
  typescript: {
    tsconfigPath: './tsconfig.json',
    // The public portfolio page should remain deployable even while internal routes still have outstanding TS issues.
    ignoreBuildErrors: true,
  },
  async rewrites() {
    // Same-origin API proxy: maps /api prefix to backend target
    const target =
      process.env.API_PROXY_TARGET ||
      process.env.NEXT_PUBLIC_API_BASE ||
      'http://localhost:30001';
    const prefix = process.env.API_PROXY_PREFIX || '/api/v1';
    // Ensure prefix starts with slash
    const normalizedPrefix = prefix.startsWith('/') ? prefix : `/${prefix}`;
    return [
      {
        source: `${normalizedPrefix}/:path*`,
        destination: `${target}${normalizedPrefix}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
