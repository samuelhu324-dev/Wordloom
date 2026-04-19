'use client';

import React, { FormEvent, useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { buildLandingPath, useAuth } from '@/shared/auth';
import { Button, Card, CardContent, CardHeader, Input } from '@/shared/ui';
import styles from '../../login/page.module.css';

const sampleCodes = ['MEMBER-DEMO', 'ADMIN-DEMO', 'OWNER-DEMO'];

export default function AdmissionOnboardingPage() {
  const router = useRouter();
  const { hydrated, isAuthenticated, session, claimAdmission } = useAuth();
  const [code, setCode] = useState('');
  const [error, setError] = useState('');

  const canSubmit = useMemo(() => !!code.trim(), [code]);

  useEffect(() => {
    if (!hydrated) {
      return;
    }

    if (!isAuthenticated || !session) {
      router.replace('/login?next=%2Fonboarding%2Fadmission');
      return;
    }

    if (session.admissionStatus === 'admitted') {
      router.replace(buildLandingPath(session));
    }
  }, [hydrated, isAuthenticated, router, session]);

  if (!hydrated) {
    return null;
  }

  if (!isAuthenticated || !session || session.admissionStatus === 'admitted') {
    return null;
  }

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    const nextSession = claimAdmission(code);
    if (!nextSession) {
      setError('Admission code did not resolve to standing for the selected tenant.');
      return;
    }

    setError('');
    router.replace(buildLandingPath(nextSession));
  };

  return (
    <main className={styles.page}>
      <section className={styles.shell}>
        <Card className={styles.card}>
          <CardHeader className={styles.header}>
            <p className={styles.eyebrow}>Membership admission</p>
            <h1>Claim tenant access</h1>
            <p>
              Identity is already authenticated for <strong>{session.email}</strong>. Claim tenant
              standing explicitly before entering protected member or admin surfaces.
            </p>
          </CardHeader>
          <CardContent>
            <form className={styles.form} onSubmit={handleSubmit}>
              <Input label="Tenant target" value={session.libraryId} readOnly fullWidth helperText="The first 9H slice keeps tenant target from the shared auth shell and derives standing from admission." />
              <Input label="Admission code" value={code} onChange={(event) => setCode(event.target.value)} required fullWidth helperText="Use one local-first demo code to claim standing for this tenant." />
              {error ? <p className={styles.helperText}>{error}</p> : null}
              <div className={styles.actions}>
                <Button type="submit" disabled={!canSubmit}>Claim admission</Button>
                <Link href="/login" className={styles.inlineLink}>
                  Back to login
                </Link>
              </div>
            </form>
            <p className={styles.helperText}>Available local-first codes: {sampleCodes.join(', ')}.</p>
          </CardContent>
        </Card>
      </section>
    </main>
  );
}