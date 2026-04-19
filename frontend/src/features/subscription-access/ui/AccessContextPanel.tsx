'use client';

import React from 'react';
import { Button, Card, CardContent, CardHeader, Spinner } from '@/shared/ui';
import { useAccessContext } from '../model/hooks';
import styles from './AccessContextPanel.module.css';

type AccessContextPanelProps = {
  libraryId: string;
};

const formatLabel = (value: string) => value.replace(/_/g, ' ');

export function AccessContextPanel({ libraryId }: AccessContextPanelProps) {
  const { data, isLoading, isError, error, refetch, isFetching } = useAccessContext(libraryId);

  if (isLoading) {
    return (
      <Card>
        <CardContent>
          <Spinner />
        </CardContent>
      </Card>
    );
  }

  if (isError || !data) {
    return (
      <Card className={styles.errorCard}>
        <CardHeader>
          <strong>Access context unavailable</strong>
        </CardHeader>
        <CardContent className={styles.errorCard}>
          <span>{(error as Error | undefined)?.message || 'Failed to load access context.'}</span>
          <div>
            <Button size="sm" variant="secondary" onClick={() => refetch()}>
              Retry
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  const gates = [
    {
      title: 'Read library',
      description: 'Core library access comes directly from backend entitlement snapshots.',
      enabled: data.entitlements.includes('read_library'),
    },
    {
      title: 'Cross-book copy',
      description: 'Unlocked only when backend plan and state widen this capability.',
      enabled: data.entitlements.includes('copy_block_cross_book'),
    },
    {
      title: 'Export book',
      description: 'Reserved for widened internal access only when returned by the backend.',
      enabled: data.entitlements.includes('export_book'),
    },
  ];

  return (
    <Card>
      <CardHeader className={styles.panel}>
        <div className={styles.header}>
          <div className={styles.titleBlock}>
            <p className={styles.eyebrow}>User-facing access context</p>
            <h2 className={styles.title}>Backend-derived access snapshot</h2>
            <p className={styles.description}>
              This panel renders plan, standing, roles, and gated capabilities from
              {' '}
              <code>/access-context/me</code>
              .
            </p>
          </div>
          <span className={styles.statusBadge} data-state={data.subscription_state}>
            {formatLabel(data.subscription_state)}
          </span>
        </div>
      </CardHeader>
      <CardContent className={styles.panel}>
        <div className={styles.grid}>
          <div className={styles.metric}>
            <span className={styles.metricLabel}>Plan</span>
            <span className={styles.metricValue}>{formatLabel(data.plan_code)}</span>
          </div>
          <div className={styles.metric}>
            <span className={styles.metricLabel}>Roles</span>
            <span className={styles.metricValue}>{data.roles.map(formatLabel).join(', ') || 'member'}</span>
          </div>
          <div className={styles.metric}>
            <span className={styles.metricLabel}>Tenant</span>
            <span className={styles.metricValue}>{data.tenant_id}</span>
          </div>
          <div className={styles.metric}>
            <span className={styles.metricLabel}>Request</span>
            <span className={styles.metricValue}>{data.request_id}</span>
          </div>
        </div>

        <div>
          <div className={styles.metricLabel}>Entitlements</div>
          <div className={styles.chips}>
            {data.entitlements.map((item) => (
              <span key={item} className={styles.chip}>{formatLabel(item)}</span>
            ))}
          </div>
        </div>

        <div className={styles.gates}>
          {gates.map((gate) => (
            <div key={gate.title} className={styles.gateRow}>
              <div className={styles.gateCopy}>
                <span className={styles.gateTitle}>{gate.title}</span>
                <span className={styles.gateDescription}>{gate.description}</span>
              </div>
              <span className={styles.gateStatus} data-enabled={gate.enabled ? 'true' : 'false'}>
                {gate.enabled ? 'Enabled' : 'Locked'}
              </span>
            </div>
          ))}
        </div>

        <div>
          <Button size="sm" variant="secondary" onClick={() => refetch()} loading={isFetching}>
            Refresh access snapshot
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}