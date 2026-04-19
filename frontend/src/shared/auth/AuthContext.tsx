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

export type AdmissionStatus = 'pending' | 'admitted';

export type TenantContextSource = 'session' | 'route' | 'manual' | 'legacy';

export type AuthSession = {
  email: string;
  displayName: string;
  role: AuthRole;
  libraryId: string;
  token: string;
  admissionStatus: AdmissionStatus;
  admissionSource: 'code' | 'dev-bypass';
};

const DEFAULT_MEMBER_LANDING_PATH = '/workbox/subscription';

const normalizeNextPath = (nextPath?: string | null) => {
  if (!nextPath) {
    return null;
  }

  if (!nextPath.startsWith('/') || nextPath.startsWith('//')) {
    return null;
  }

  if (
    nextPath.startsWith('/login') ||
    nextPath.startsWith('/register') ||
    nextPath.startsWith('/onboarding/admission')
  ) {
    return null;
  }

  return nextPath;
};

const canAccessNextPath = (
  session: Pick<AuthSession, 'role' | 'admissionStatus'>,
  nextPath: string
) => {
  if (session.admissionStatus !== 'admitted') {
    return false;
  }

  if (nextPath.startsWith('/workbox/subscription')) {
    return true;
  }

  if (nextPath.startsWith('/admin/subscriptions')) {
    return session.role === 'admin' || session.role === 'owner';
  }

  return false;
};

export type CurrentTenantContext = {
  tenantId: string;
  source: TenantContextSource;
  updatedAt: string;
};

type AuthInput = {
  email: string;
  displayName: string;
  libraryId: string;
  role?: AuthRole;
  admissionCode?: string;
  admissionSource?: 'code' | 'dev-bypass';
};

type AdmissionRecord = {
  code: string;
  role: AuthRole;
  libraryId?: string;
};

type AuthContextValue = {
  hydrated: boolean;
  session: AuthSession | null;
  currentTenantContext: CurrentTenantContext | null;
  currentTenantId: string;
  isAuthenticated: boolean;
  isAdmitted: boolean;
  isAdmin: boolean;
  signIn: (input: AuthInput) => AuthSession;
  register: (input: AuthInput) => AuthSession;
  claimAdmission: (code: string) => AuthSession | null;
  signOut: () => void;
  hasRole: (roles: AuthRole[]) => boolean;
  setCurrentTenantContext: (tenantId: string, source?: TenantContextSource) => CurrentTenantContext | null;
  clearCurrentTenantContext: () => void;
};

const AUTH_SESSION_STORAGE_KEY = 'wl_auth_session';
const AUTH_TOKEN_STORAGE_KEY = 'wl_token';
const CURRENT_TENANT_CONTEXT_STORAGE_KEY = 'wl_current_tenant_context';
const ACTIVE_LIBRARY_STORAGE_KEY = 'wl_active_library_id';

const LOCAL_ADMISSION_RECORDS: AdmissionRecord[] = [
  { code: 'MEMBER-DEMO', role: 'member' },
  { code: 'ADMIN-DEMO', role: 'admin' },
  { code: 'OWNER-DEMO', role: 'owner' },
];

const AuthContext = createContext<AuthContextValue | null>(null);

const isRole = (value: unknown): value is AuthRole =>
  value === 'member' || value === 'admin' || value === 'owner';

const isAdmissionStatus = (value: unknown): value is AdmissionStatus =>
  value === 'pending' || value === 'admitted';

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
    !isAdmissionStatus(candidate.admissionStatus) ||
    (candidate.admissionSource !== 'code' && candidate.admissionSource !== 'dev-bypass') ||
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
    admissionStatus: candidate.admissionStatus,
    admissionSource: candidate.admissionSource,
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

const resolveAdmissionRecord = (code: string, libraryId: string): AdmissionRecord | null => {
  const normalizedCode = code.trim().toUpperCase();
  const normalizedLibraryId = libraryId.trim();
  if (!normalizedCode || !normalizedLibraryId) {
    return null;
  }

  return (
    LOCAL_ADMISSION_RECORDS.find(
      (record) =>
        record.code === normalizedCode && (!record.libraryId || record.libraryId === normalizedLibraryId)
    ) || null
  );
};

const createSession = (input: AuthInput): AuthSession => {
  const normalizedLibraryId = input.libraryId.trim();
  const explicitBypass = input.admissionSource === 'dev-bypass' && input.role;
  const admissionRecord = explicitBypass
    ? null
    : resolveAdmissionRecord(input.admissionCode || '', normalizedLibraryId);
  const role = explicitBypass ? input.role : admissionRecord?.role || 'member';
  const admissionStatus: AdmissionStatus = explicitBypass || admissionRecord ? 'admitted' : 'pending';

  return {
    email: input.email.trim(),
    displayName: input.displayName.trim(),
    role,
    libraryId: normalizedLibraryId,
    token: createToken(role),
    admissionStatus,
    admissionSource: explicitBypass ? 'dev-bypass' : 'code',
  };
};

export const buildLandingPath = (
  session: Pick<AuthSession, 'role' | 'libraryId' | 'admissionStatus'>,
  nextPath?: string | null
) => {
  const normalizedNextPath = normalizeNextPath(nextPath);

  if (session.admissionStatus === 'pending') {
    return normalizedNextPath
      ? `/onboarding/admission?next=${encodeURIComponent(normalizedNextPath)}`
      : '/onboarding/admission';
  }

  if (normalizedNextPath && canAccessNextPath(session, normalizedNextPath)) {
    return normalizedNextPath;
  }

  if (session.role === 'admin' || session.role === 'owner') {
    return `/admin/subscriptions/${session.libraryId}`;
  }

  return DEFAULT_MEMBER_LANDING_PATH;
};

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
    const nextSession = createSession(input);
    persistSession(nextSession);
    const nextTenantContext =
      nextSession.admissionStatus === 'admitted'
        ? createTenantContext(nextSession.libraryId, 'session')
        : null;
    persistTenantContext(nextTenantContext);
    setSession(nextSession);
    setCurrentTenantContextState(nextTenantContext);
    return nextSession;
  }, []);

  const claimAdmission = useCallback(
    (code: string) => {
      if (!session) {
        return null;
      }

      const admissionRecord = resolveAdmissionRecord(code, session.libraryId);
      if (!admissionRecord) {
        return null;
      }

      const nextSession: AuthSession = {
        ...session,
        role: admissionRecord.role,
        token: createToken(admissionRecord.role),
        admissionStatus: 'admitted',
        admissionSource: 'code',
      };

      persistSession(nextSession);
      const nextTenantContext = createTenantContext(nextSession.libraryId, 'session');
      persistTenantContext(nextTenantContext);
      setSession(nextSession);
      setCurrentTenantContextState(nextTenantContext);
      return nextSession;
    },
    [session]
  );

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
      isAdmitted: !!session && session.admissionStatus === 'admitted',
      isAdmin:
        !!session &&
        session.admissionStatus === 'admitted' &&
        (session.role === 'admin' || session.role === 'owner'),
      signIn: writeSession,
      register: writeSession,
      claimAdmission,
      signOut,
      hasRole,
      setCurrentTenantContext,
      clearCurrentTenantContext,
    }),
    [
      claimAdmission,
      clearCurrentTenantContext,
      currentTenantContext,
      hasRole,
      hydrated,
      session,
      setCurrentTenantContext,
      signOut,
      writeSession,
    ]
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