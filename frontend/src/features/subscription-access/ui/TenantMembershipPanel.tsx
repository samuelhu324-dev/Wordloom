'use client';

import React, { useState } from 'react';
import { Button, Card, CardContent, CardHeader, Input, Spinner } from '@/shared/ui';
import {
  useGrantLibraryMembership,
  useLibraryMemberships,
  useRevokeLibraryMembership,
  type MembershipRole,
} from '../model/hooks';
import styles from './TenantMembershipPanel.module.css';

type TenantMembershipPanelProps = {
  libraryId: string;
};

const roleOptions: MembershipRole[] = ['member', 'admin', 'owner'];

const formatTimestamp = (value: string) => {
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }
  return parsed.toLocaleString();
};

export function TenantMembershipPanel({ libraryId }: TenantMembershipPanelProps) {
  const membershipsQuery = useLibraryMemberships(libraryId);
  const grantMembership = useGrantLibraryMembership(libraryId);
  const revokeMembership = useRevokeLibraryMembership(libraryId);
  const [userId, setUserId] = useState('');
  const [role, setRole] = useState<MembershipRole>('member');
  const [localError, setLocalError] = useState<string | null>(null);

  const handleGrant = async () => {
    const trimmedUserId = userId.trim();
    if (!trimmedUserId) {
      return;
    }

    setLocalError(null);
    try {
      await grantMembership.mutateAsync({ userId: trimmedUserId, role });
      setUserId('');
      setRole('member');
    } catch (error) {
      setLocalError((error as Error)?.message || 'Failed to grant membership.');
    }
  };

  const handleRevoke = async (memberUserId: string) => {
    setLocalError(null);
    try {
      await revokeMembership.mutateAsync(memberUserId);
    } catch (error) {
      setLocalError((error as Error)?.message || 'Failed to revoke membership.');
    }
  };

  return (
    <Card>
      <CardHeader className={styles.panel}>
        <strong>Tenant membership management</strong>
        <p className={styles.description}>
          This first bounded management surface stays scoped to the selected tenant and reuses the
          same backend membership authority instead of inventing browser-local role state.
        </p>
      </CardHeader>
      <CardContent className={styles.panel}>
        <div className={styles.formRow}>
          <Input
            label="User ID"
            value={userId}
            onChange={(event) => setUserId(event.target.value)}
            placeholder="Paste the member user UUID"
            fullWidth
          />
          <label className={styles.selectWrapper}>
            <span className={styles.selectLabel}>Role</span>
            <select value={role} onChange={(event) => setRole(event.target.value as MembershipRole)} className={styles.select}>
              {roleOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>
          <Button onClick={handleGrant} loading={grantMembership.isPending}>Grant or update</Button>
        </div>

        {localError ? <div className={styles.error}>{localError}</div> : null}

        {membershipsQuery.isLoading ? (
          <Spinner />
        ) : membershipsQuery.isError ? (
          <div className={styles.error}>
            {(membershipsQuery.error as Error | undefined)?.message || 'Failed to load tenant memberships.'}
          </div>
        ) : (
          <div className={styles.list}>
            {(membershipsQuery.data?.items || []).length === 0 ? (
              <div className={styles.empty}>No tenant memberships recorded yet.</div>
            ) : (
              membershipsQuery.data?.items.map((item) => (
                <div key={item.id} className={styles.item}>
                  <div className={styles.itemMain}>
                    <strong>{item.user_id}</strong>
                    <span className={styles.roleBadge} data-role={item.role}>{item.role}</span>
                  </div>
                  <div className={styles.meta}>added {formatTimestamp(item.created_at)}</div>
                  <div className={styles.actions}>
                    <Button
                      size="sm"
                      variant="danger"
                      onClick={() => handleRevoke(item.user_id)}
                      loading={revokeMembership.isPending}
                    >
                      Revoke
                    </Button>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}