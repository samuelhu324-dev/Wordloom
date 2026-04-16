'use client';

import React, { useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { MockBillingPanel, useSubscriptionHistory, useSubscriptionState } from '@/features/subscription-access';
import { LibraryAccessWidget } from '@/widgets/library';
import { Breadcrumb, Button, Card, CardContent, CardHeader, Spinner } from '@/shared/ui';
import styles from './page.module.css';

const formatLabel = (value: string) => value.replace(/_/g, ' ');

export default function AdminSubscriptionDetailPage() {
  const params = useParams();
  const router = useRouter();
  const libraryId = (params.libraryId as string) || '';
  const stateQuery = useSubscriptionState(libraryId);
  const historyQuery = useSubscriptionHistory(libraryId);

  useEffect(() => {
    if (!libraryId) {
      return;
    }
    try {
      localStorage.setItem('wl_active_library_id', libraryId);
    } catch {}
  }, [libraryId]);

  return (
    <main className={styles.page}>
      <div className={styles.container}>
        <Breadcrumb
          items={[
            { label: 'Admin', href: '/admin/libraries' },
            { label: 'Subscriptions', href: '/admin/subscriptions' },
            { label: libraryId, active: true },
          ]}
        />

        <section className={styles.hero}>
          <div>
            <h1>Subscription detail</h1>
            <p>
              Inspect backend-derived state and history for one library, then emit mock billing events
              through the bounded admin endpoint.
            </p>
          </div>
          <div className={styles.heroActions}>
            <Button variant="secondary" onClick={() => router.push('/admin/subscriptions')}>
              Change library
            </Button>
            <Button variant="secondary" onClick={() => stateQuery.refetch()} loading={stateQuery.isFetching}>
              Refresh admin state
            </Button>
          </div>
        </section>

        <section className={styles.grid}>
          <div className={styles.stack}>
            <LibraryAccessWidget libraryId={libraryId} />

            <Card className={styles.summaryCard}>
              <CardHeader>
                <strong>Admin subscription state</strong>
              </CardHeader>
              <CardContent className={styles.summaryCard}>
                {stateQuery.isLoading ? (
                  <Spinner />
                ) : stateQuery.isError || !stateQuery.data ? (
                  <div className={styles.error}>
                    {(stateQuery.error as Error | undefined)?.message || 'Failed to load subscription state.'}
                  </div>
                ) : (
                  <>
                    <div className={styles.summaryGrid}>
                      <div className={styles.summaryMetric}>
                        <span className={styles.summaryLabel}>Plan</span>
                        <span className={styles.summaryValue}>{formatLabel(stateQuery.data.plan_code)}</span>
                      </div>
                      <div className={styles.summaryMetric}>
                        <span className={styles.summaryLabel}>Standing</span>
                        <span className={styles.summaryValue}>{formatLabel(stateQuery.data.subscription_state)}</span>
                      </div>
                      <div className={styles.summaryMetric}>
                        <span className={styles.summaryLabel}>Entitlements</span>
                        <span className={styles.summaryValue}>{stateQuery.data.entitlements.length}</span>
                      </div>
                    </div>
                    <div className={styles.status}>
                      {stateQuery.data.entitlements.map((item) => formatLabel(item)).join(', ')}
                    </div>
                  </>
                )}
              </CardContent>
            </Card>
          </div>

          <div className={styles.stack}>
            <MockBillingPanel libraryId={libraryId} />

            <Card className={styles.summaryCard}>
              <CardHeader>
                <strong>Applied event history</strong>
              </CardHeader>
              <CardContent className={styles.summaryCard}>
                {historyQuery.isLoading ? (
                  <Spinner />
                ) : historyQuery.isError ? (
                  <div className={styles.error}>
                    {(historyQuery.error as Error | undefined)?.message || 'Failed to load subscription history.'}
                  </div>
                ) : (
                  <div className={styles.historyList}>
                    {(historyQuery.data?.items || []).length === 0 ? (
                      <div className={styles.historyMeta}>No applied events yet.</div>
                    ) : (
                      historyQuery.data?.items.map((item) => (
                        <div key={item.id} className={styles.historyItem}>
                          <strong>{formatLabel(item.event_type)}</strong>
                          <div className={styles.historyMeta}>{new Date(item.created_at).toLocaleString()}</div>
                          <div className={styles.historyMeta}>subscription {item.subscription_id}</div>
                        </div>
                      ))
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </section>
      </div>
    </main>
  );
}