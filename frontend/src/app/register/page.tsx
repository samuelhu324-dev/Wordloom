'use client';

import React, { FormEvent, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { AuthRole, buildLandingPath, useAuth } from '@/shared/auth';
import { Button, Card, CardContent, CardHeader, Input } from '@/shared/ui';
import styles from '../login/page.module.css';

const roleOptions: AuthRole[] = ['member', 'admin', 'owner'];

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuth();
  const [email, setEmail] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [libraryId, setLibraryId] = useState('');
  const [role, setRole] = useState<AuthRole>('member');

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    const nextSession = register({
      email,
      displayName,
      libraryId,
      role,
    });
    router.replace(buildLandingPath(nextSession));
  };

  return (
    <main className={styles.page}>
      <section className={styles.shell}>
        <Card className={styles.card}>
          <CardHeader className={styles.header}>
            <p className={styles.eyebrow}>Shared auth shell</p>
            <h1>Create a local-first account</h1>
            <p>
              Registration in `9E/P1` creates a browser-local session only. It exists to validate the
              first role-aware entry and protected-route flow before real auth-provider work begins.
            </p>
          </CardHeader>
          <CardContent>
            <form className={styles.form} onSubmit={handleSubmit}>
              <Input label="Display name" value={displayName} onChange={(event) => setDisplayName(event.target.value)} required fullWidth />
              <Input label="Email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required fullWidth />
              <Input label="Library ID" value={libraryId} onChange={(event) => setLibraryId(event.target.value)} required fullWidth helperText="A first library scope is required so access-context requests know which tenant/library to target." />
              <label className={styles.selectWrapper}>
                <span className={styles.selectLabel}>Starting role</span>
                <select value={role} onChange={(event) => setRole(event.target.value as AuthRole)} className={styles.select}>
                  {roleOptions.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </label>
              <div className={styles.actions}>
                <Button type="submit">Register</Button>
                <Link href="/login" className={styles.inlineLink}>
                  Already have a session?
                </Link>
              </div>
            </form>
          </CardContent>
        </Card>
      </section>
    </main>
  );
}