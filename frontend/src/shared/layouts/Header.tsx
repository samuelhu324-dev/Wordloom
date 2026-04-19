"use client";
import React from 'react';
import Link from 'next/link';
import { useI18n } from '@/i18n/useI18n';
import { Button } from '@/shared/ui';
import { buildLandingPath, useAuth } from '@/shared/auth';
import { WorkboxMenu } from './WorkboxMenu';
import { ThemeMenu } from './ThemeMenu';
import { LanguageMenu } from './LanguageMenu';
import { LocalActorSwitcher } from './LocalActorSwitcher';
import styles from './Header.module.css';

export const Header: React.FC = () => {
  const { t } = useI18n();
  const { hydrated, session, currentTenantId, signOut } = useAuth();

  const handleSignOut = () => {
    signOut();
    window.location.href = '/';
  };

  const sessionLandingPath =
    session && currentTenantId
      ? buildLandingPath({
          role: session.role,
          libraryId: currentTenantId,
          admissionStatus: session.admissionStatus,
        })
      : session
        ? buildLandingPath(session)
        : '/';

  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <Link href="/" className={styles.logo}>
          <h1>{t('app.title')}</h1>
        </Link>
        <nav className={styles.nav}>
          <ThemeMenu />
          <LanguageMenu />
          {/* Workbox 下拉菜单 */}
          <WorkboxMenu />
          {hydrated && session ? (
            <>
              <LocalActorSwitcher className={styles.actorSwitcher} />
              <Link href={sessionLandingPath} className={styles.sessionBadge}>
                {session.displayName} · {session.role}
              </Link>
              <Button variant="secondary" size="sm" onClick={handleSignOut}>
                Sign out
              </Button>
            </>
          ) : (
            <div className={styles.authLinks}>
              <Link href="/login" className={styles.sessionBadge}>
                Log in
              </Link>
              <Link href="/register" className={styles.sessionBadge}>
                Register
              </Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
};