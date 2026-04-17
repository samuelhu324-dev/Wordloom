'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { AccessContextPanel } from '@/features/subscription-access';
import { useAuth } from '@/shared/auth';
import { Breadcrumb, Button, Card, CardContent, CardHeader, Input } from '@/shared/ui';
import styles from './page.module.css';

export default function AdminSubscriptionsPage() {
  const router = useRouter();
  const { currentTenantId, setCurrentTenantContext } = useAuth();
  const [libraryId, setLibraryId] = useState('');

  useEffect(() => {
    setLibraryId(currentTenantId);
  }, [currentTenantId]);

  const handleOpen = () => {
    const trimmed = libraryId.trim();
    if (!trimmed) {
      return;
    }
    setCurrentTenantContext(trimmed, 'manual');
    router.push(`/admin/subscriptions/${trimmed}`);
  };

  return (
    <main className={styles.page}>
      <div className={styles.container}>
        <Breadcrumb
          items={[
            { label: 'Admin', href: '/admin/libraries' },
            { label: 'Subscriptions', active: true },
          ]}
        />

        <section className={styles.hero}>
          <h1>Subscription Console</h1>
          <p>
            Open a library-scoped admin view, inspect current backend subscription standing, and run
            the bounded mock-billing loop without exposing tenant-wide history or mutation controls to ordinary users.
          </p>
        </section>

        <Card className={styles.card}>
          <CardHeader>
            <strong>Choose a library</strong>
          </CardHeader>
          <CardContent className={styles.card}>
            <div className={styles.actions}>
              <Input
                label="Library ID"
                value={libraryId}
                onChange={(event) => setLibraryId(event.target.value)}
                placeholder="Paste the target library UUID"
                fullWidth
              />
              <Button onClick={handleOpen}>Open admin subscription page</Button>
            </div>
            <div className={styles.hint}>
              Current tenant context: {currentTenantId || 'not set'}
            </div>
          </CardContent>
        </Card>

        {currentTenantId && <AccessContextPanel libraryId={currentTenantId} />}
      </div>
    </main>
  );
}