'use client';

import axios, {
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from 'axios';

import { sendQuickLogEvent } from '@/shared/telemetry/quickLogClient';
import { createCorrelationId, nowMs } from '@/shared/telemetry/correlationId';

type AxiosRequestMeta = {
  startMs?: number;
  correlationId?: string;
};

const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const AUTH_SESSION_STORAGE_KEY = 'wl_auth_session';
const CURRENT_TENANT_CONTEXT_STORAGE_KEY = 'wl_current_tenant_context';
const ACTIVE_LIBRARY_STORAGE_KEY = 'wl_active_library_id';

const normalizeBaseOrigin = (input?: string | null): string => {
  if (!input) {
    return '';
  }
  return input.replace(/\/+$/, '');
};

const isUuidLike = (value: unknown): value is string =>
  typeof value === 'string' && UUID_PATTERN.test(value.trim());

const readLibraryIdFromValue = (value: unknown): string | null => {
  if (isUuidLike(value)) {
    return value.trim();
  }
  return null;
};

const extractLibraryIdFromUrl = (url?: string): string | null => {
  if (!url) {
    return null;
  }

  try {
    const parsed = new URL(url, 'http://wordloom.local');
    const fromQuery = readLibraryIdFromValue(
      parsed.searchParams.get('library_id') ?? parsed.searchParams.get('libraryId')
    );
    if (fromQuery) {
      return fromQuery;
    }

    const libraryPathMatch = parsed.pathname.match(/\/libraries\/([0-9a-f-]{36})(?=\/|$)/i);
    if (libraryPathMatch?.[1] && isUuidLike(libraryPathMatch[1])) {
      return libraryPathMatch[1];
    }
  } catch {
    return null;
  }

  return null;
};

const extractLibraryIdFromConfig = (config: InternalAxiosRequestConfig): string | null => {
  const params = config.params as Record<string, unknown> | undefined;
  const fromParams = readLibraryIdFromValue(params?.library_id ?? params?.libraryId);
  if (fromParams) {
    return fromParams;
  }

  const data = config.data as Record<string, unknown> | undefined;
  const fromData = readLibraryIdFromValue(data?.library_id ?? data?.libraryId);
  if (fromData) {
    return fromData;
  }

  return extractLibraryIdFromUrl(config.url);
};

const readActiveLibraryId = (): string | null => {
  if (!isBrowser) {
    return null;
  }
  try {
    const rawTenantContext = localStorage.getItem(CURRENT_TENANT_CONTEXT_STORAGE_KEY);
    if (rawTenantContext) {
      const parsed = JSON.parse(rawTenantContext) as
        | { tenantId?: unknown; libraryId?: unknown }
        | null;
      const explicitTenantId = readLibraryIdFromValue(parsed?.tenantId ?? parsed?.libraryId);
      if (explicitTenantId) {
        return explicitTenantId;
      }
    }

    const stored = localStorage.getItem(ACTIVE_LIBRARY_STORAGE_KEY);
    return readLibraryIdFromValue(stored);
  } catch {
    return null;
  }
};

const readDevUserIdFromSession = (): string | null => {
  if (!isBrowser) {
    return null;
  }

  try {
    const raw = localStorage.getItem(AUTH_SESSION_STORAGE_KEY);
    if (!raw) {
      return null;
    }

    const parsed = JSON.parse(raw) as { userId?: unknown } | null;
    return isUuidLike(parsed?.userId) ? parsed.userId.trim() : null;
  } catch {
    return null;
  }
};

const isBrowser = typeof window !== 'undefined';
const envBaseOrigin = normalizeBaseOrigin(process.env.NEXT_PUBLIC_API_BASE?.trim() || '');
const DEFAULT_SERVER_BASE = normalizeBaseOrigin(
  process.env.API_PROXY_TARGET?.trim() ||
    process.env.NEXT_PUBLIC_API_BASE?.trim() ||
    'http://localhost:30001'
);

// 浏览器侧默认走同源（空字符串），由 Next rewrites → API_PROXY_TARGET 处理跨端口代理；
// 仅在 Storybook/脚本/CI 等脱离 Next 环境时才依赖 NEXT_PUBLIC_API_BASE 或回落到 localhost:30001。
const API_BASE_URL = envBaseOrigin || (isBrowser ? '' : DEFAULT_SERVER_BASE);
const RAW_API_PREFIX = process.env.NEXT_PUBLIC_API_PREFIX || '/api/v1';
const API_PREFIX = RAW_API_PREFIX.startsWith('/') ? RAW_API_PREFIX : `/${RAW_API_PREFIX}`;

export const API_BASE_ORIGIN = API_BASE_URL;
export const API_PREFIX_PATH = API_PREFIX;
export const API_ROOT = `${API_BASE_ORIGIN}${API_PREFIX_PATH}`;

export const buildApiUrl = (path: string): string => {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return `${API_ROOT}${normalizedPath}`;
};

// ============ API 客户端配置 ============
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_ROOT,
  timeout: parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || '30000', 10),
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============ 请求拦截器 ============
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const headers: any = config.headers || {};
    const existingCorrelationId = headers['X-Request-Id'] || headers['x-request-id'];
    const correlationId = (existingCorrelationId as string) || createCorrelationId();
    headers['X-Request-Id'] = correlationId;
    config.headers = headers;

    (config as any).meta = {
      ...(config as any).meta,
      startMs: nowMs(),
      correlationId,
    } satisfies AxiosRequestMeta;

    // 添加 JWT Token
    const token = typeof window !== 'undefined' ? localStorage.getItem('wl_token') : null;
    const shouldSendBearerToken =
      !!token &&
      !token.startsWith('wl-dev-') &&
      token.split('.').length === 3;
    if (shouldSendBearerToken) {
      config.headers.Authorization = `Bearer ${token}`;
    } else if (process.env.NODE_ENV !== 'production') {
      const devUserId = readDevUserIdFromSession();
      if (devUserId) {
        headers['X-Dev-User-Id'] = devUserId;
      }
    }

    const existingTenantHeader = headers['X-Library-Id'] || headers['x-library-id'] || headers['X-Tenant-Id'] || headers['x-tenant-id'];
    if (!existingTenantHeader) {
      const derivedLibraryId = extractLibraryIdFromConfig(config) ?? readActiveLibraryId();
      if (derivedLibraryId) {
        headers['X-Library-Id'] = derivedLibraryId;
        headers['X-Tenant-Id'] = derivedLibraryId;
      }
    }

    // 开发期前缀 & URL 使用规范守卫 (RULE_API_PREFIX_001)
    if (process.env.NODE_ENV !== 'production') {
      const rawUrl = config.url || '';

      // 1. 禁止传入绝对 URL（应只写资源相对路径）
      if (/^https?:\/\//i.test(rawUrl)) {
        // 保留仍可请求，但提示重构。
        console.warn('[api prefix guard] 传入绝对 URL: ' + rawUrl + '。请改为相对资源路径 (例如 /libraries)。');
      }

      // 2. 防止重复包含 /api/v1 前缀（baseURL 已含前缀）
      if (rawUrl.startsWith('/api/v1/')) {
        console.warn('[api prefix guard] 路径包含重复前缀 /api/v1，将自动剥离。原始: ' + rawUrl);
        config.url = rawUrl.replace(/^\/api\/v1\//, '/');
      }

      // 3. 确保以 '/' 开头（否则 axios 会拼接为奇怪的相对路径）
      if (config.url && !config.url.startsWith('/')) {
        console.warn('[api prefix guard] 路径未以 / 开头: ' + config.url + '。自动补全。');
        config.url = '/' + config.url;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ============ 响应拦截器 ============
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    const meta: AxiosRequestMeta | undefined = (response.config as any).meta;
    const startMs = meta?.startMs;
    const correlationId = meta?.correlationId || (response.headers?.['x-request-id'] as string | undefined);
    const endMs = nowMs();
    const durationMs = startMs ? endMs - startMs : undefined;

    sendQuickLogEvent({
      type: 'http.client.response',
      timestamp: Date.now(),
      data: {
        correlation_id: correlationId,
        method: response.config.method,
        url: response.config.url,
        status_code: response.status,
        duration_ms: durationMs,
      },
    });

    return response;
  },
  (error) => {
    try {
      const cfg = error?.config;
      const meta: AxiosRequestMeta | undefined = cfg ? (cfg as any).meta : undefined;
      const startMs = meta?.startMs;
      const correlationId = meta?.correlationId;
      const endMs = nowMs();
      const durationMs = startMs ? endMs - startMs : undefined;

      sendQuickLogEvent({
        type: 'http.client.error',
        timestamp: Date.now(),
        data: {
          correlation_id: correlationId,
          method: cfg?.method,
          url: cfg?.url,
          status_code: error?.response?.status,
          duration_ms: durationMs,
          error_type: error?.name,
          error_message: String(error?.message || ''),
        },
      });
    } catch {
      // Metrics must never break requests.
    }

    // 处理全局错误
    if (error.response?.status === 401) {
      // Token 过期，清理并重定向到登录
      if (typeof window !== 'undefined') {
        localStorage.removeItem('wl_token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// ============ HTTP 方法封装 ============
export const api = {
  get<T = any>(url: string, config?: AxiosRequestConfig) {
    return apiClient.get<T>(url, config);
  },
  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
    return apiClient.post<T>(url, data, config);
  },
  patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
    return apiClient.patch<T>(url, data, config);
  },
  put<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
    return apiClient.put<T>(url, data, config);
  },
  delete<T = any>(url: string, config?: AxiosRequestConfig) {
    return apiClient.delete<T>(url, config);
  },
};

export default apiClient;
