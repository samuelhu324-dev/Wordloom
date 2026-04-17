import { test, expect } from '@playwright/test';

const LIBRARY_ID = '11111111-1111-1111-1111-111111111111';

function session(role: 'member' | 'admin') {
  return {
    email: `${role}@wordloom.dev`,
    displayName: `${role}-user`,
    role,
    libraryId: LIBRARY_ID,
    token: `wl-dev-${role}-local-switch`,
  };
}

async function seedSession(page: Parameters<typeof test>[0]['page'], role: 'member' | 'admin') {
  await page.addInitScript(({ authSession, libraryId }) => {
    window.localStorage.setItem('wl_auth_session', JSON.stringify(authSession));
    window.localStorage.setItem('wl_token', authSession.token);
    window.localStorage.setItem('wl_active_library_id', libraryId);
    window.localStorage.setItem(
      'wl_current_tenant_context',
      JSON.stringify({
        tenantId: libraryId,
        source: 'manual',
        updatedAt: '2026-04-17T00:00:00.000Z',
      })
    );
  }, { authSession: session(role), libraryId: LIBRARY_ID });
}

test.describe('Local actor switching', () => {
  test('switches between admin and member without manual storage edits', async ({ page }) => {
    await seedSession(page, 'admin');
    await page.goto(`/admin/subscriptions/${LIBRARY_ID}`);

    await expect(page.getByRole('heading', { name: 'Subscription detail' })).toBeVisible();
    await expect(page.getByTestId('local-actor-switcher')).toBeVisible();
    await expect(page.getByText('Tenant membership management')).toBeVisible();

    await page.getByLabel('Local actor role').selectOption('member');
    await page.getByRole('button', { name: 'Switch' }).click();

    await expect(page).toHaveURL(/\/workbox\/subscription/);
    await expect(page.getByRole('heading', { name: 'My Subscription' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Open Subscription Console' })).toHaveCount(0);
    await expect(page.getByRole('link', { name: 'member-user · member' })).toHaveAttribute('href', '/workbox/subscription');
    await expect(page.getByText('Tenant membership management')).toHaveCount(0);

    await page.getByLabel('Local actor role').selectOption('admin');
    await page.getByRole('button', { name: 'Switch' }).click();

    await expect(page).toHaveURL(/\/admin\/subscriptions/);
    await expect(page.getByRole('heading', { name: 'Subscription Console' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'admin-user · admin' })).toHaveAttribute('href', '/admin/subscriptions');

    await page.goto(`/admin/subscriptions/${LIBRARY_ID}`);
    await expect(page.getByText('Tenant membership management')).toBeVisible();

    const storage = await page.evaluate(() => ({
      authSession: JSON.parse(window.localStorage.getItem('wl_auth_session') || 'null'),
      currentTenantContext: JSON.parse(window.localStorage.getItem('wl_current_tenant_context') || 'null'),
    }));

    expect(storage.authSession?.role).toBe('admin');
    expect(storage.authSession?.libraryId).toBe(LIBRARY_ID);
    expect(storage.currentTenantContext?.tenantId).toBe(LIBRARY_ID);
  });
});