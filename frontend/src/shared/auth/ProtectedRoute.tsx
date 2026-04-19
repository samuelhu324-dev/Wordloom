'use client';

import React, { useEffect } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { Spinner } from '@/shared/ui';
import { AuthRole, buildLandingPath, useAuth } from './AuthContext';

type ProtectedRouteProps = {
  children: React.ReactNode;
  allowedRoles?: AuthRole[];
};

export function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const router = useRouter();
  const pathname = usePathname();
  const { hydrated, isAuthenticated, isAdmitted, session, hasRole } = useAuth();

  useEffect(() => {
    if (!hydrated) {
      return;
    }

    if (!isAuthenticated) {
      const next = pathname ? `?next=${encodeURIComponent(pathname)}` : '';
      router.replace(`/login${next}`);
      return;
    }

    if (!isAdmitted && session) {
      router.replace(buildLandingPath(session, pathname));
      return;
    }

    if (allowedRoles && !hasRole(allowedRoles) && session) {
      router.replace(buildLandingPath(session));
    }
  }, [allowedRoles, hasRole, hydrated, isAdmitted, isAuthenticated, pathname, router, session]);

  if (!hydrated || !isAuthenticated || !isAdmitted || (allowedRoles && !hasRole(allowedRoles))) {
    return (
      <div style={{ minHeight: '50vh', display: 'grid', placeItems: 'center' }}>
        <Spinner />
      </div>
    );
  }

  return <>{children}</>;
}