'use client';

import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react';

export type AuthRole = 'member' | 'admin' | 'owner';

export type TenantContextSource = 'session' | 'route' | 'manual' | 'legacy';

export type AuthSession = {
  email: string;
  displayName: string;
  role: AuthRole;
  libraryId: string;
  token: string;
};

export type CurrentTenantContext = {
  tenantId: string;
  source: TenantContextSource;
  updatedAt: string;
};

type AuthInput = {
  email: string;
  displayName: string;
  role: AuthRole;
  libraryId: string;
};

type AuthContextValue = {
  hydrated: boolean;
  session: AuthSession | null;
  currentTenantContext: CurrentTenantContext | null;
  currentTenantId: string;
  isAuthenticated: boolean;
  isAdmin: boolean;
  signIn: (input: AuthInput) => AuthSession;
  register: (input: AuthInput) => AuthSession;
  signOut: () => void;
  hasRole: (roles: AuthRole[]) => boolean;
  setCurrentTenantContext: (tenantId: string, source?: TenantContextSource) => CurrentTenantContext | null;
  clearCurrentTenantContext: () => void;
};

const AUTH_SESSION_STORAGE_KEY = 'wl_auth_session';
const AUTH_TOKEN_STORAGE_KEY = 'wl_token';
const CURRENT_TENANT_CONTEXT_STORAGE_KEY = 'wl_current_tenant_context';
const ACTIVE_LIBRARY_STORAGE_KEY = 'wl_active_library_id';

const AuthContext = createContext<AuthContextValue | null>(null);

const isRole = (value: unknown): value is AuthRole =>
  value === 'member' || value === 'admin' || value === 'owner';

const isTenantContextSource = (value: unknown): value is TenantContextSource =>
  value === 'session' || value === 'route' || value === 'manual' || value === 'legacy';

const normalizeSession = (value: unknown): AuthSession | null => {
  if (!value || typeof value !== 'object') {
    return null;
  }

  const candidate = value as Partial<AuthSession>;
  if (
    typeof candidate.email !== 'string' ||
    typeof candidate.displayName !== 'string' ||
    typeof candidate.libraryId !== 'string' ||
    typeof candidate.token !== 'string' ||
    !isRole(candidate.role)
  ) {
    return null;
  }

  return {
    email: candidate.email,
    displayName: candidate.displayName,
    role: candidate.role,
    libraryId: candidate.libraryId,
    token: candidate.token,
  };
};

const normalizeTenantContext = (value: unknown): CurrentTenantContext | null => {
  if (!value || typeof value !== 'object') {
    return null;
  }

  const candidate = value as Partial<CurrentTenantContext> & { libraryId?: string };
  const tenantId =
    typeof candidate.tenantId === 'string'
      ? candidate.tenantId.trim()
      : typeof candidate.libraryId === 'string'
        ? candidate.libraryId.trim()
        : '';

  if (!tenantId || !isTenantContextSource(candidate.source) || typeof candidate.updatedAt !== 'string') {
    return null;
  }

  return {
    tenantId,
    source: candidate.source,
    updatedAt: candidate.updatedAt,
  };
};

const createTenantContext = (
  tenantId: string,
  source: TenantContextSource
): CurrentTenantContext | null => {
  const normalizedTenantId = tenantId.trim();
  if (!normalizedTenantId) {
    return null;
  }

  return {
    tenantId: normalizedTenantId,
    source,
    updatedAt: new Date().toISOString(),
  };
};

const readStoredSession = (): AuthSession | null => {
  if (typeof window === 'undefined') {
    return null;
  }

  try {
    const raw = localStorage.getItem(AUTH_SESSION_STORAGE_KEY);
    if (!raw) {
      return null;
    }
    return normalizeSession(JSON.parse(raw));
  } catch {
    return null;
  }
};

const readStoredTenantContext = (): CurrentTenantContext | null => {
  if (typeof window === 'undefined') {
    return null;
  }

  try {
    const raw = localStorage.getItem(CURRENT_TENANT_CONTEXT_STORAGE_KEY);
    if (raw) {
      const parsed = normalizeTenantContext(JSON.parse(raw));
      if (parsed) {
        return parsed;
      }
    }

    const legacyTenantId = localStorage.getItem(ACTIVE_LIBRARY_STORAGE_KEY);
    return createTenantContext(legacyTenantId || '', 'legacy');
  } catch {
    return null;
  }
};

const persistSession = (session: AuthSession | null) => {
  if (typeof window === 'undefined') {
    return;
  }

  if (!session) {
    localStorage.removeItem(AUTH_SESSION_STORAGE_KEY);
    localStorage.removeItem(AUTH_TOKEN_STORAGE_KEY);
    return;
  }

  localStorage.setItem(AUTH_SESSION_STORAGE_KEY, JSON.stringify(session));
  localStorage.setItem(AUTH_TOKEN_STORAGE_KEY, session.token);
};

const persistTenantContext = (tenantContext: CurrentTenantContext | null) => {
  if (typeof window === 'undefined') {
    return;
  }

  if (!tenantContext) {
    localStorage.removeItem(CURRENT_TENANT_CONTEXT_STORAGE_KEY);
    localStorage.removeItem(ACTIVE_LIBRARY_STORAGE_KEY);
    return;
  }

  localStorage.setItem(CURRENT_TENANT_CONTEXT_STORAGE_KEY, JSON.stringify(tenantContext));
  localStorage.setItem(ACTIVE_LIBRARY_STORAGE_KEY, tenantContext.tenantId);
};

const createToken = (role: AuthRole) => {
  const suffix =
    typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function'
      ? crypto.randomUUID()
      : `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
  return `wl-dev-${role}-${suffix}`;
};

export const buildLandingPath = (session: Pick<AuthSession, 'role' | 'libraryId'>) =>
  session.role === 'admin' || session.role === 'owner'
    ? '/admin/subscriptions'
    : '/workbox/subscription';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<AuthSession | null>(null);
  const [currentTenantContext, setCurrentTenantContextState] = useState<CurrentTenantContext | null>(null);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setSession(readStoredSession());
    setCurrentTenantContextState(readStoredTenantContext());
    setHydrated(true);
  }, []);

  useEffect(() => {
    const handleStorage = () => {
      setSession(readStoredSession());
      setCurrentTenantContextState(readStoredTenantContext());
    };

    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);

  const writeSession = useCallback((input: AuthInput) => {
    const nextSession: AuthSession = {
      email: input.email.trim(),
      displayName: input.displayName.trim(),
      role: input.role,
      libraryId: input.libraryId.trim(),
      token: createToken(input.role),
    };
    persistSession(nextSession);
    const nextTenantContext = createTenantContext(nextSession.libraryId, 'session');
    persistTenantContext(nextTenantContext);
    setSession(nextSession);
    setCurrentTenantContextState(nextTenantContext);
    return nextSession;
  }, []);

  const setCurrentTenantContext = useCallback(
    (tenantId: string, source: TenantContextSource = 'manual') => {
      const nextTenantContext = createTenantContext(tenantId, source);
      persistTenantContext(nextTenantContext);
      setCurrentTenantContextState(nextTenantContext);
      return nextTenantContext;
    },
    []
  );

  const clearCurrentTenantContext = useCallback(() => {
    persistTenantContext(null);
    setCurrentTenantContextState(null);
  }, []);

  const signOut = useCallback(() => {
    persistSession(null);
    persistTenantContext(null);
    setSession(null);
    setCurrentTenantContextState(null);
  }, []);

  useEffect(() => {
    if (!session || currentTenantContext) {
      return;
    }

    const seededTenantContext = createTenantContext(session.libraryId, 'session');
    if (!seededTenantContext) {
      return;
    }

    persistTenantContext(seededTenantContext);
    setCurrentTenantContextState(seededTenantContext);
  }, [currentTenantContext, session]);

  const hasRole = useCallback(
    (roles: AuthRole[]) => !!session && roles.includes(session.role),
    [session]
  );

  const value = useMemo<AuthContextValue>(
    () => ({
      hydrated,
      session,
      currentTenantContext,
      currentTenantId: currentTenantContext?.tenantId || session?.libraryId || '',
      isAuthenticated: !!session,
      isAdmin: !!session && (session.role === 'admin' || session.role === 'owner'),
      signIn: writeSession,
      register: writeSession,
      signOut,
      hasRole,
      setCurrentTenantContext,
      clearCurrentTenantContext,
    }),
    [clearCurrentTenantContext, currentTenantContext, hasRole, hydrated, session, setCurrentTenantContext, signOut, writeSession]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};