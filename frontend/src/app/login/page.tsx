'use client';

import React, { FormEvent, useMemo, useState } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { AuthRole, buildLandingPath, useAuth } from '@/shared/auth';
import { Button, Card, CardContent, CardHeader, Input } from '@/shared/ui';
import styles from './page.module.css';

const roleOptions: AuthRole[] = ['member', 'admin', 'owner'];

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { signIn, session } = useAuth();
  const [email, setEmail] = useState(session?.email || '');
  const [displayName, setDisplayName] = useState(session?.displayName || 'Wordloom User');
  const [libraryId, setLibraryId] = useState(session?.libraryId || '');
  const [role, setRole] = useState<AuthRole>(session?.role || 'member');

  const nextPath = useMemo(() => searchParams.get('next'), [searchParams]);

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    const nextSession = signIn({
      email,
      displayName,
      libraryId,
      role,
    });
    router.replace(nextPath || buildLandingPath(nextSession));
  };

  return (
    <main className={styles.page}>
      <section className={styles.shell}>
        <Card className={styles.card}>
          <CardHeader className={styles.header}>
            <p className={styles.eyebrow}>Shared auth shell</p>
            <h1>Log in to Wordloom</h1>
            <p>
              This local-first auth shell writes a lightweight session to browser storage so `9E/P1`
              can validate Workbox entry and route gating before real provider integration.
            </p>
          </CardHeader>
          <CardContent>
            <form className={styles.form} onSubmit={handleSubmit}>
              <Input label="Email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required fullWidth />
              <Input label="Display name" value={displayName} onChange={(event) => setDisplayName(event.target.value)} required fullWidth />
              <Input label="Library ID" value={libraryId} onChange={(event) => setLibraryId(event.target.value)} required fullWidth helperText="Use an existing library UUID so access-context queries remain scoped." />
              <label className={styles.selectWrapper}>
                <span className={styles.selectLabel}>Role</span>
                <select value={role} onChange={(event) => setRole(event.target.value as AuthRole)} className={styles.select}>
                  {roleOptions.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </label>
              <div className={styles.actions}>
                <Button type="submit">Log in</Button>
                <Link href="/register" className={styles.inlineLink}>
                  Create an account
                </Link>
              </div>
            </form>
          </CardContent>
        </Card>
      </section>
    </main>
  );
}