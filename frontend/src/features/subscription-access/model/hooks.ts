'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  applyPaymentEvent,
  getAccessContext,
  getSubscriptionHistory,
  getSubscriptionState,
  type PaymentEventType,
} from './api';

const accessContextKey = (libraryId?: string) => ['subscription-access', 'access-context', libraryId ?? 'active'];
const subscriptionStateKey = (libraryId?: string) => ['subscription-access', 'admin-state', libraryId ?? 'none'];
const subscriptionHistoryKey = (libraryId?: string) => ['subscription-access', 'admin-history', libraryId ?? 'none'];

export function useAccessContext(libraryId?: string) {
  return useQuery({
    queryKey: accessContextKey(libraryId),
    queryFn: () => getAccessContext(libraryId),
    enabled: Boolean(libraryId),
  });
}

export function useSubscriptionState(libraryId?: string) {
  return useQuery({
    queryKey: subscriptionStateKey(libraryId),
    queryFn: () => getSubscriptionState(libraryId!),
    enabled: Boolean(libraryId),
  });
}

export function useSubscriptionHistory(libraryId?: string) {
  return useQuery({
    queryKey: subscriptionHistoryKey(libraryId),
    queryFn: () => getSubscriptionHistory(libraryId!),
    enabled: Boolean(libraryId),
  });
}

export function useApplyPaymentEvent(libraryId?: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (eventType: PaymentEventType) => applyPaymentEvent(libraryId!, eventType),
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: accessContextKey(libraryId) }),
        queryClient.invalidateQueries({ queryKey: subscriptionStateKey(libraryId) }),
        queryClient.invalidateQueries({ queryKey: subscriptionHistoryKey(libraryId) }),
      ]);
    },
  });
}