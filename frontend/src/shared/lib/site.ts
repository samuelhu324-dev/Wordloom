const ABSOLUTE_URL_RE = /^(?:[a-z]+:)?\/\//i;

export const normalizeOrigin = (value: string): string => value.replace(/\/+$/, '');

export const withHttps = (value: string): string =>
  value.startsWith('http://') || value.startsWith('https://') ? value : `https://${value}`;

export const normalizeBasePath = (value: string): string => {
  const trimmed = value.trim();

  if (!trimmed || trimmed === '/') {
    return '';
  }

  const withLeadingSlash = trimmed.startsWith('/') ? trimmed : `/${trimmed}`;
  return withLeadingSlash.replace(/\/+$/, '');
};

export const siteBasePath = normalizeBasePath(process.env.NEXT_PUBLIC_BASE_PATH || '');

export const withBasePath = (path: string): string => {
  if (!path) {
    return siteBasePath || '/';
  }

  if (
    ABSOLUTE_URL_RE.test(path) ||
    path.startsWith('#') ||
    path.startsWith('mailto:') ||
    path.startsWith('tel:')
  ) {
    return path;
  }

  const normalizedPath = path === '/' ? '/' : path.startsWith('/') ? path : `/${path}`;

  if (!siteBasePath) {
    return normalizedPath;
  }

  if (normalizedPath === siteBasePath || normalizedPath.startsWith(`${siteBasePath}/`)) {
    return normalizedPath;
  }

  return normalizedPath === '/' ? `${siteBasePath}/` : `${siteBasePath}${normalizedPath}`;
};

export const buildSiteUrl = (origin: string): string => `${normalizeOrigin(withHttps(origin))}${siteBasePath}`;