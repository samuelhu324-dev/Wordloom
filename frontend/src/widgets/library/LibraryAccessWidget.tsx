'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/shared/ui';
import { AccessContextPanel } from '@/features/subscription-access';
import styles from './LibraryAccessWidget.module.css';

type LibraryAccessWidgetProps = {
  libraryId: string;
};

export function LibraryAccessWidget({ libraryId }: LibraryAccessWidgetProps) {
  const router = useRouter();

  return (
    <section className={styles.shell}>
      <AccessContextPanel libraryId={libraryId} />
      <div className={styles.actions}>
        <Button size="sm" variant="secondary" onClick={() => router.push(`/admin/subscriptions/${libraryId}`)}>
          Open subscription admin view
        </Button>
      </div>
    </section>
  );
}