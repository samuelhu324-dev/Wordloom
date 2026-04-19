import { test, expect } from '@playwright/test';

const LIBRARY_ID = '11111111-1111-1111-1111-111111111111';

test.describe('Identity to membership to entry closure', () => {
  test('registration closes into admitted member entry under explicit tenant scope', async ({ page }) => {
    await page.goto('/register');

    const textboxes = page.getByRole('textbox');

    await textboxes.nth(0).fill('member-closure-user');
    await textboxes.nth(1).fill('member-closure@wordloom.dev');
    await textboxes.nth(2).fill(LIBRARY_ID);
    await page.getByRole('button', { name: 'Register' }).click();

    await expect(page).toHaveURL(/\/onboarding\/admission$/);
    await expect(page.getByRole('heading', { name: 'Claim tenant access' })).toBeVisible();

    await page.getByRole('textbox').nth(1).fill('MEMBER-DEMO');
    await page.getByRole('button', { name: 'Claim admission' }).click();

    await expect(page).toHaveURL(/\/workbox\/subscription$/);
    await expect(page.getByRole('heading', { name: 'My Subscription' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Open Subscription Console' })).toHaveCount(0);

    await page.goto(`/admin/subscriptions/${LIBRARY_ID}`);
    await expect(page).toHaveURL(/\/workbox\/subscription$/);

    const storage = await page.evaluate(() => ({
      authSession: JSON.parse(window.localStorage.getItem('wl_auth_session') || 'null'),
      currentTenantContext: JSON.parse(window.localStorage.getItem('wl_current_tenant_context') || 'null'),
    }));

    expect(storage.authSession?.admissionStatus).toBe('admitted');
    expect(storage.authSession?.admissionSource).toBe('code');
    expect(storage.authSession?.role).toBe('member');
    expect(storage.authSession?.libraryId).toBe(LIBRARY_ID);
    expect(storage.currentTenantContext?.tenantId).toBe(LIBRARY_ID);
    expect(storage.currentTenantContext?.source).toBe('session');
  });
});