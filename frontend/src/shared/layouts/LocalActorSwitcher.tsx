'use client';

import React, { useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { buildLandingPath, useAuth, type AuthRole } from '@/shared/auth';
import { Button } from '@/shared/ui';
import styles from './LocalActorSwitcher.module.css';

type LocalActorSwitcherProps = {
  className?: string;
};

const actorProfiles: Record<AuthRole, { email: string; displayName: string }> = {
  member: {
    email: 'member@wordloom.dev',
    displayName: 'member-user',
  },
  admin: {
    email: 'admin@wordloom.dev',
    displayName: 'admin-user',
  },
  owner: {
    email: 'owner@wordloom.dev',
    displayName: 'owner-user',
  },
};

export function LocalActorSwitcher({ className = '' }: LocalActorSwitcherProps) {
  const router = useRouter();
  const { session, currentTenantId, signIn } = useAuth();
  const [selectedRole, setSelectedRole] = useState<AuthRole>(session?.role || 'member');

  const targetTenantId = useMemo(() => currentTenantId || session?.libraryId || '', [currentTenantId, session]);

  if (!session) {
    return null;
  }

  const handleApply = () => {
    if (!targetTenantId) {
      return;
    }

    const profile = actorProfiles[selectedRole];
    const nextSession = signIn({
      email: profile.email,
      displayName: profile.displayName,
      role: selectedRole,
      libraryId: targetTenantId,
    });

    router.replace(buildLandingPath(nextSession));
  };

  return (
    <div className={[styles.container, className].filter(Boolean).join(' ')} data-testid="local-actor-switcher">
      <span className={styles.label}>Local actor</span>
      <select
        value={selectedRole}
        onChange={(event) => setSelectedRole(event.target.value as AuthRole)}
        className={styles.select}
        aria-label="Local actor role"
      >
        <option value="member">member</option>
        <option value="admin">admin</option>
        <option value="owner">owner</option>
      </select>
      <Button
        size="sm"
        variant="secondary"
        onClick={handleApply}
        disabled={!targetTenantId || selectedRole === session.role}
      >
        Switch
      </Button>
    </div>
  );
}