import { test, expect } from '@playwright/test';

const SESSION_LIBRARY_ID = '11111111-1111-1111-1111-111111111111';
const EXPLICIT_TENANT_ID = '22222222-2222-2222-2222-222222222222';
const STALE_LIBRARY_ID = '33333333-3333-3333-3333-333333333333';
const ROUTE_LIBRARY_ID = '44444444-4444-4444-4444-444444444444';

function adminSession() {
  return {
    email: 'admin@wordloom.dev',
    displayName: 'admin-user',
    role: 'admin' as const,
    libraryId: SESSION_LIBRARY_ID,
    token: 'wl-dev-admin-tenant-context',
  };
}

async function seedAdminContext(
  page: Parameters<typeof test>[0]['page'],
  options?: {
    currentTenantId?: string;
    activeLibraryId?: string;
  }
) {
  await page.addInitScript(
    ({ authSession, currentTenantId, activeLibraryId }) => {
      window.localStorage.setItem('wl_auth_session', JSON.stringify(authSession));
      window.localStorage.setItem('wl_token', authSession.token);

      if (currentTenantId) {
        window.localStorage.setItem(
          'wl_current_tenant_context',
          JSON.stringify({
            tenantId: currentTenantId,
            source: 'manual',
            updatedAt: '2026-04-17T00:00:00.000Z',
          })
        );
      }

      if (activeLibraryId) {
        window.localStorage.setItem('wl_active_library_id', activeLibraryId);
      }
    },
    {
      authSession: adminSession(),
      currentTenantId: options?.currentTenantId,
      activeLibraryId: options?.activeLibraryId,
    }
  );
}

test.describe('Tenant context runtime', () => {
  test('explicit current tenant context is preferred over stale active library fallback', async ({ page }) => {
    await seedAdminContext(page, {
      currentTenantId: EXPLICIT_TENANT_ID,
      activeLibraryId: STALE_LIBRARY_ID,
    });

    await page.goto('/admin/subscriptions');

    await expect(page.getByRole('heading', { name: 'Subscription Console' })).toBeVisible();
    await expect(page.getByText(`Current tenant context: ${EXPLICIT_TENANT_ID}`)).toBeVisible();

    const storage = await page.evaluate(() => ({
      currentTenantContext: window.localStorage.getItem('wl_current_tenant_context'),
      activeLibraryId: window.localStorage.getItem('wl_active_library_id'),
    }));

    expect(storage.currentTenantContext).toContain(EXPLICIT_TENANT_ID);
    expect(storage.activeLibraryId).toBe(STALE_LIBRARY_ID);
  });

  test('route-bound admin detail corrects stale tenant context and compatibility storage', async ({ page }) => {
    await seedAdminContext(page, {
      currentTenantId: EXPLICIT_TENANT_ID,
      activeLibraryId: STALE_LIBRARY_ID,
    });

    await page.goto(`/admin/subscriptions/${ROUTE_LIBRARY_ID}`);

    await expect(page.getByRole('heading', { name: 'Subscription detail' })).toBeVisible();
    await expect(page.getByText(ROUTE_LIBRARY_ID)).toBeVisible();

    await expect
      .poll(async () =>
        page.evaluate(() => ({
          currentTenantContext: JSON.parse(window.localStorage.getItem('wl_current_tenant_context') || 'null'),
          activeLibraryId: window.localStorage.getItem('wl_active_library_id'),
        }))
      )
      .toMatchObject({
        currentTenantContext: {
          tenantId: ROUTE_LIBRARY_ID,
          source: 'route',
        },
        activeLibraryId: ROUTE_LIBRARY_ID,
      });
  });
});