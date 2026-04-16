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

export type AuthSession = {
  email: string;
  displayName: string;
  role: AuthRole;
  libraryId: string;
  token: string;
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
  isAuthenticated: boolean;
  isAdmin: boolean;
  signIn: (input: AuthInput) => AuthSession;
  register: (input: AuthInput) => AuthSession;
  signOut: () => void;
  hasRole: (roles: AuthRole[]) => boolean;
};

const AUTH_SESSION_STORAGE_KEY = 'wl_auth_session';
const AUTH_TOKEN_STORAGE_KEY = 'wl_token';
const ACTIVE_LIBRARY_STORAGE_KEY = 'wl_active_library_id';

const AuthContext = createContext<AuthContextValue | null>(null);

const isRole = (value: unknown): value is AuthRole =>
  value === 'member' || value === 'admin' || value === 'owner';

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
  localStorage.setItem(ACTIVE_LIBRARY_STORAGE_KEY, session.libraryId);
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
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setSession(readStoredSession());
    setHydrated(true);
  }, []);

  useEffect(() => {
    const handleStorage = () => {
      setSession(readStoredSession());
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
    setSession(nextSession);
    return nextSession;
  }, []);

  const signOut = useCallback(() => {
    persistSession(null);
    setSession(null);
  }, []);

  const hasRole = useCallback(
    (roles: AuthRole[]) => !!session && roles.includes(session.role),
    [session]
  );

  const value = useMemo<AuthContextValue>(
    () => ({
      hydrated,
      session,
      isAuthenticated: !!session,
      isAdmin: !!session && (session.role === 'admin' || session.role === 'owner'),
      signIn: writeSession,
      register: writeSession,
      signOut,
      hasRole,
    }),
    [hasRole, hydrated, session, signOut, writeSession]
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