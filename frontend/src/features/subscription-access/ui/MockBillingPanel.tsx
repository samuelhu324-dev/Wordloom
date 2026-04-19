'use client';

import React, { useState } from 'react';
import { Button, Card, CardContent, CardHeader } from '@/shared/ui';
import { useApplyPaymentEvent, useSubscriptionState } from '../model/hooks';
import type { PaymentEventType } from '../model/api';
import styles from './MockBillingPanel.module.css';

type MockBillingPanelProps = {
  libraryId: string;
};

const EVENT_OPTIONS: { value: PaymentEventType; label: string }[] = [
  { value: 'upgrade_success', label: 'upgrade_success' },
  { value: 'renewal_failed', label: 'renewal_failed' },
  { value: 'admin_correction', label: 'admin_correction' },
];

const formatLabel = (value: string) => value.replace(/_/g, ' ');

export function MockBillingPanel({ libraryId }: MockBillingPanelProps) {
  const [lastApplied, setLastApplied] = useState<PaymentEventType | null>(null);
  const [pendingEvent, setPendingEvent] = useState<PaymentEventType | null>(null);
  const [localError, setLocalError] = useState<string | null>(null);
  const applyEvent = useApplyPaymentEvent(libraryId);
  const { data: state } = useSubscriptionState(libraryId);

  const handleApply = async (eventType: PaymentEventType) => {
    setLocalError(null);
    setPendingEvent(eventType);
    try {
      await applyEvent.mutateAsync(eventType);
      setLastApplied(eventType);
    } catch (error) {
      setLocalError((error as Error)?.message || 'Failed to emit billing event.');
    } finally {
      setPendingEvent(null);
    }
  };

  return (
    <Card>
      <CardHeader className={styles.panel}>
        <strong>Mock billing interaction</strong>
        <p className={styles.description}>
          These buttons emit bounded backend events only. The browser does not derive lifecycle
          transitions locally; it re-renders from the updated backend payload.
        </p>
      </CardHeader>
      <CardContent className={styles.panel}>
        <div className={styles.buttonRow}>
          {EVENT_OPTIONS.map((option) => (
            <Button
              key={option.value}
              size="sm"
              variant={option.value === 'renewal_failed' ? 'danger' : 'secondary'}
              onClick={() => handleApply(option.value)}
              loading={applyEvent.isPending && pendingEvent === option.value}
            >
              Emit {option.label}
            </Button>
          ))}
        </div>

        {localError && <div className={styles.error}>{localError}</div>}

        <div className={styles.resultBox}>
          <span className={styles.resultLabel}>Latest backend standing</span>
          <span className={styles.resultValue}>
            {state ? `${formatLabel(state.plan_code)} / ${formatLabel(state.subscription_state)}` : 'Waiting for state'}
          </span>
        </div>

        {lastApplied && (
          <div className={styles.resultBox}>
            <span className={styles.resultLabel}>Last emitted event</span>
            <span className={styles.resultValue}>{lastApplied}</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}