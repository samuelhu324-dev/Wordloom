'use client';

import React, { useEffect, useState } from 'react';
import { AccessContextPanel } from '@/features/subscription-access';
import { useAuth } from '@/shared/auth';
import { Breadcrumb, Button, Card, CardContent, CardHeader, Input } from '@/shared/ui';
import styles from './page.module.css';

export default function MySubscriptionPage() {
  const { session, isAdmin, currentTenantId, setCurrentTenantContext } = useAuth();
  const [libraryId, setLibraryId] = useState('');

  useEffect(() => {
    const nextTenantId = currentTenantId || session?.libraryId || '';
    setLibraryId(nextTenantId);
  }, [currentTenantId, session]);

  const handleSaveLibrary = () => {
    const trimmed = libraryId.trim();
    if (!trimmed) {
      return;
    }
    setCurrentTenantContext(trimmed, 'manual');
  };

  return (
    <main className={styles.page}>
      <div className={styles.container}>
        <Breadcrumb
          items={[
            { label: 'Workbox', href: '/workbox/subscription' },
            { label: 'My Subscription', active: true },
          ]}
        />

        <section className={styles.hero}>
          <div>
            <p className={styles.eyebrow}>User-facing subscription entry</p>
            <h1>My Subscription</h1>
            <p>
              Review your current plan, standing, and gated capabilities without exposing tenant-wide
              event history or admin-only operational controls.
            </p>
          </div>
          {session ? (
            <div className={styles.identityCard}>
              <strong>{session.displayName}</strong>
              <span>{session.email}</span>
              <span>{session.role}</span>
            </div>
          ) : null}
        </section>

        <Card>
          <CardHeader>
            <strong>Current library scope</strong>
          </CardHeader>
          <CardContent className={styles.cardStack}>
            <Input
              label="Library ID"
              value={libraryId}
              onChange={(event) => setLibraryId(event.target.value)}
              helperText="This local-first auth shell uses an explicit current tenant context to scope access-context requests."
              fullWidth
            />
            <div className={styles.actions}>
              <Button onClick={handleSaveLibrary}>Save library scope</Button>
              {isAdmin ? (
                <Button variant="secondary" onClick={() => (window.location.href = '/admin/subscriptions')}>
                  Open Subscription Console
                </Button>
              ) : null}
            </div>
          </CardContent>
        </Card>

        {libraryId.trim() ? <AccessContextPanel libraryId={libraryId.trim()} /> : null}
      </div>
    </main>
  );
}