'use client';

import React, { useEffect, useState } from 'react';
import { useLibraries } from '@/features/library';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/shared/auth';
import { Breadcrumb, Button, Card, CardContent, CardHeader, Input } from '@/shared/ui';
import styles from './page.module.css';

export default function AdminSubscriptionsPage() {
  const router = useRouter();
  const librariesQuery = useLibraries({});
  const { currentTenantId, setCurrentTenantContext } = useAuth();
  const [libraryId, setLibraryId] = useState('');
  const availableLibraries = librariesQuery.data || [];
  const suggestedLibrary = availableLibraries[0];
  const resolvedCurrentTenantId =
    currentTenantId && availableLibraries.some((library) => library.id === currentTenantId)
      ? currentTenantId
      : suggestedLibrary?.id || '';

  useEffect(() => {
    if (resolvedCurrentTenantId) {
      setLibraryId(resolvedCurrentTenantId);
    }
  }, [resolvedCurrentTenantId]);

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
            <strong>What makes this admin-only</strong>
          </CardHeader>
          <CardContent className={styles.card}>
            <div className={styles.roleGrid}>
              <div className={styles.roleItem}>
                <span className={styles.roleLabel}>Audience</span>
                <strong>Admin, owner only</strong>
              </div>
              <div className={styles.roleItem}>
                <span className={styles.roleLabel}>Blocked for members</span>
                <strong>Redirected back to My Subscription</strong>
              </div>
              <div className={styles.roleItem}>
                <span className={styles.roleLabel}>Admin tools</span>
                <strong>Membership, billing, event history</strong>
              </div>
            </div>
            <p className={styles.explainer}>
              This landing page is intentionally not the shared subscription view. It is the admin entry point that lets you
              choose a library and then open the tenant-scoped detail surface with operational controls.
            </p>
          </CardContent>
        </Card>

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

        <Card className={styles.card}>
          <CardHeader>
            <strong>Admin detail surface</strong>
          </CardHeader>
          <CardContent className={styles.card}>
            <p className={styles.explainer}>
              After you open a library, the admin detail page adds the backend access snapshot plus the admin-only controls:
              mock billing, tenant membership management, and applied event history.
            </p>
            <div className={styles.hint}>
              Suggested library: {resolvedCurrentTenantId || 'waiting for library list'}
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}