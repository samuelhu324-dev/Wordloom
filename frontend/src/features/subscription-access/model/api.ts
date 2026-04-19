'use client';

import { api } from '@/shared/api/client';

export type PaymentEventType = 'upgrade_success' | 'renewal_failed' | 'admin_correction';

export type AccessContextDto = {
  user_id: string;
  tenant_id: string;
  roles: string[];
  plan_code: string;
  subscription_state: string;
  entitlements: string[];
  request_id: string;
};

export type SubscriptionStateDto = {
  library_id: string;
  plan_code: string;
  subscription_state: string;
  entitlements: string[];
};

export type PaymentEventDto = {
  id: string;
  subscription_id: string;
  library_id: string;
  event_type: PaymentEventType | string;
  created_at: string;
};

export type SubscriptionHistoryDto = {
  items: PaymentEventDto[];
};

export type LibraryMembershipDto = {
  id: string;
  library_id: string;
  user_id: string;
  role: string;
  created_at: string;
  updated_at: string;
};

export type LibraryMembershipListDto = {
  items: LibraryMembershipDto[];
};

export type MembershipRole = 'owner' | 'admin' | 'member';

const withLibraryHeader = (libraryId?: string) => (
  libraryId
    ? {
        headers: {
          'X-Library-Id': libraryId,
        },
      }
    : undefined
);

export async function getAccessContext(libraryId?: string): Promise<AccessContextDto> {
  const response = await api.get<AccessContextDto>('/access-context/me', withLibraryHeader(libraryId));
  return response.data;
}

export async function getSubscriptionState(libraryId: string): Promise<SubscriptionStateDto> {
  const response = await api.get<SubscriptionStateDto>(
    `/admin/subscriptions/${libraryId}`,
    withLibraryHeader(libraryId)
  );
  return response.data;
}

export async function getSubscriptionHistory(libraryId: string): Promise<SubscriptionHistoryDto> {
  const response = await api.get<SubscriptionHistoryDto>(
    `/admin/subscriptions/${libraryId}/history`,
    withLibraryHeader(libraryId)
  );
  return response.data;
}

export async function applyPaymentEvent(
  libraryId: string,
  eventType: PaymentEventType
): Promise<SubscriptionStateDto> {
  const response = await api.post<SubscriptionStateDto>(
    `/admin/subscriptions/${libraryId}/events`,
    { event_type: eventType },
    withLibraryHeader(libraryId)
  );
  return response.data;
}

export async function getLibraryMemberships(libraryId: string): Promise<LibraryMembershipListDto> {
  const response = await api.get<LibraryMembershipListDto>(
    `/libraries/${libraryId}/memberships`,
    withLibraryHeader(libraryId)
  );
  return response.data;
}

export async function grantLibraryMembership(
  libraryId: string,
  payload: { userId: string; role: MembershipRole }
): Promise<void> {
  await api.post(
    `/libraries/${libraryId}/memberships`,
    { user_id: payload.userId, role: payload.role },
    withLibraryHeader(libraryId)
  );
}

export async function revokeLibraryMembership(libraryId: string, userId: string): Promise<void> {
  await api.delete(`/libraries/${libraryId}/memberships/${userId}`, withLibraryHeader(libraryId));
}