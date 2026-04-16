'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { AccessContextPanel } from '@/features/subscription-access';
import { Breadcrumb, Button, Card, CardContent, CardHeader, Input } from '@/shared/ui';
import styles from './page.module.css';

export default function AdminSubscriptionsPage() {
  const router = useRouter();
  const [libraryId, setLibraryId] = useState('');
  const [activeLibraryId, setActiveLibraryId] = useState('');

  useEffect(() => {
    try {
      const stored = localStorage.getItem('wl_active_library_id') || '';
      setLibraryId(stored);
      setActiveLibraryId(stored);
    } catch {}
  }, []);

  const handleOpen = () => {
    const trimmed = libraryId.trim();
    if (!trimmed) {
      return;
    }
    try {
      localStorage.setItem('wl_active_library_id', trimmed);
    } catch {}
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
          <h1>Subscription admin consumer lane</h1>
          <p>
            Open a library-scoped admin view, inspect current backend subscription standing, and run
            the bounded mock-billing loop without recreating lifecycle rules in the browser.
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
              Active library from local storage: {activeLibraryId || 'not set'}
            </div>
          </CardContent>
        </Card>

        {activeLibraryId && <AccessContextPanel libraryId={activeLibraryId} />}
      </div>
    </main>
  );
}