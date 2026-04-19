'use client';

import React, { FormEvent, useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { useLibraries } from '@/features/library';
import { buildLandingPath, useAuth } from '@/shared/auth';
import { Button, Card, CardContent, CardHeader, Input } from '@/shared/ui';
import styles from '../login/page.module.css';

export default function RegisterPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { register } = useAuth();
  const librariesQuery = useLibraries({});
  const [email, setEmail] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [libraryId, setLibraryId] = useState('');

  const nextPath = useMemo(() => searchParams.get('next'), [searchParams]);
  const availableLibraries = librariesQuery.data || [];
  const suggestedLibrary = availableLibraries[0];
  const hasKnownLibrary = availableLibraries.some((library) => library.id === libraryId.trim());

  useEffect(() => {
    if (!libraryId && suggestedLibrary?.id) {
      setLibraryId(suggestedLibrary.id);
    }
  }, [libraryId, suggestedLibrary?.id]);

  const tenantWarning = useMemo(() => {
    if (!libraryId.trim() || availableLibraries.length === 0 || hasKnownLibrary) {
      return undefined;
    }

    return 'This tenant target is not in the current backend library list. Using the suggested library is safer for local demo flows.';
  }, [availableLibraries.length, hasKnownLibrary, libraryId]);

  const tenantHelperText = useMemo(() => {
    if (suggestedLibrary) {
      return `A first tenant target is still required. Suggested: ${suggestedLibrary.name} (${suggestedLibrary.id}).`;
    }

    return 'A first tenant target is still required so onboarding knows which tenant admission to claim.';
  }, [suggestedLibrary]);

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    const normalizedLibraryId = libraryId.trim();

    const nextSession = register({
      email,
      displayName,
      libraryId: normalizedLibraryId,
    });
    router.replace(buildLandingPath(nextSession, nextPath));
  };

  return (
    <main className={styles.page}>
      <section className={styles.shell}>
        <Card className={styles.card}>
          <CardHeader className={styles.header}>
            <p className={styles.eyebrow}>Shared auth shell</p>
            <h1>Create a local-first account</h1>
            <p>
              Registration now creates identity first and leaves tenant standing to an explicit
              admission step, so role truth no longer starts from form selection alone.
            </p>
          </CardHeader>
          <CardContent>
            <form className={styles.form} onSubmit={handleSubmit}>
              <Input label="Display name" value={displayName} onChange={(event) => setDisplayName(event.target.value)} required fullWidth />
              <Input label="Email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required fullWidth />
              <Input
                label="Tenant target"
                value={libraryId}
                onChange={(event) => setLibraryId(event.target.value)}
                required
                fullWidth
                error={tenantWarning}
                helperText={tenantHelperText}
              />
              <div className={styles.actions}>
                <Button type="submit">Register</Button>
                <Link href="/login" className={styles.inlineLink}>
                  Already have a session?
                </Link>
              </div>
            </form>
            <p className={styles.helperText}>After registration, claim one local admission code on the onboarding page to derive member/admin/owner standing.</p>
          </CardContent>
        </Card>
      </section>
    </main>
  );
}