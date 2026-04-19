'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '@/shared/ui';
import { useI18n } from '@/i18n/useI18n';
import styles from './page.module.css';

const quickLinks = [
  { href: '/workbox/subscription', label: 'Open Workbox', variant: 'primary' as const },
  { href: '/test', label: 'Open Test Route', variant: 'secondary' as const },
  { href: '/login', label: 'Open Login', variant: 'secondary' as const },
];

export default function HomePage() {
  const { t } = useI18n();

  return (
    <main className={styles.page}>
      <section className={styles.shell}>
        <div className={styles.hero}>
          <p className={styles.kicker}>Portfolio entry</p>
          <h1 className={styles.title}>Wordloom</h1>
          <p className={styles.subtitle}>
            {t('home.subtitle')}
          </p>
          <p className={styles.summary}>
            A backend-heavy knowledge platform focused on search, async workflows, observability, and safe system evolution.
          </p>
          <div className={styles.primaryActions}>
            <Link href="/demo">
              <Button variant="primary" size="lg">
                View Demo
              </Button>
            </Link>
            <a
              className={styles.githubLink}
              href="https://github.com/samuelhu324-dev/Wordloom"
              target="_blank"
              rel="noreferrer"
            >
              View GitHub
            </a>
          </div>
          <div className={styles.tags}>
            <span>Search</span>
            <span>Outbox workflows</span>
            <span>Observability</span>
            <span>System evolution</span>
          </div>
        </div>

        <div className={styles.panel}>
          <div className={styles.panelSection}>
            <p className={styles.panelLabel}>What to open first</p>
            <h2 className={styles.panelTitle}>Start with the demo page.</h2>
            <p className={styles.panelBody}>
              The demo route is the formal portfolio-style front door. It is designed to be shareable without the backend API and gives a cleaner first read than the internal product routes.
            </p>
          </div>

          <div className={styles.panelSection}>
            <p className={styles.panelLabel}>Internal routes</p>
            <div className={styles.quickActions}>
              {quickLinks.map((item) => (
                <Link key={item.href} href={item.href} className={styles.quickActionLink}>
                  <Button variant={item.variant} size="md">
                    {item.label}
                  </Button>
                </Link>
              ))}
            </div>
          </div>

          <div className={styles.panelFooter}>
            <p>{t('home.notice.admin404')}</p>
            <p>{t('home.footer.version')}</p>
          </div>
        </div>
      </section>
    </main>
  );
}
