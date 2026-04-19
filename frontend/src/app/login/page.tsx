'use client';

import React, { FormEvent, useMemo, useState } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { buildLandingPath, useAuth } from '@/shared/auth';
import { Button, Card, CardContent, CardHeader, Input } from '@/shared/ui';
import styles from './page.module.css';

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { signIn, session } = useAuth();
  const [email, setEmail] = useState(session?.email || '');
  const [displayName, setDisplayName] = useState(session?.displayName || 'Wordloom User');
  const [libraryId, setLibraryId] = useState(session?.libraryId || '');

  const nextPath = useMemo(() => searchParams.get('next'), [searchParams]);

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    const nextSession = signIn({
      email,
      displayName,
      libraryId,
    });
    router.replace(buildLandingPath(nextSession, nextPath));
  };

  return (
    <main className={styles.page}>
      <section className={styles.shell}>
        <Card className={styles.card}>
          <CardHeader className={styles.header}>
            <p className={styles.eyebrow}>Shared auth shell</p>
            <h1>Log in to Wordloom</h1>
            <p>
              This shared auth shell now treats identity entry separately from tenant standing. Sign in
              first, then complete local admission if the identity has not yet claimed tenant access.
            </p>
          </CardHeader>
          <CardContent>
            <form className={styles.form} onSubmit={handleSubmit}>
              <Input label="Email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required fullWidth />
              <Input label="Display name" value={displayName} onChange={(event) => setDisplayName(event.target.value)} required fullWidth />
              <Input label="Tenant target" value={libraryId} onChange={(event) => setLibraryId(event.target.value)} required fullWidth helperText="Use an existing library UUID as the tenant target. Standing is claimed later through admission." />
              <div className={styles.actions}>
                <Button type="submit">Log in</Button>
                <Link href="/register" className={styles.inlineLink}>
                  Create an account
                </Link>
              </div>
            </form>
            <p className={styles.helperText}>Local admission codes are claimed after sign-in on the onboarding page: `MEMBER-DEMO`, `ADMIN-DEMO`, `OWNER-DEMO`.</p>
          </CardContent>
        </Card>
      </section>
    </main>
  );
}