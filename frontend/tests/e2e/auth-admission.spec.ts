import { test, expect } from '@playwright/test';

const LIBRARY_ID = '11111111-1111-1111-1111-111111111111';

test.describe('Auth admission flow', () => {
  test('identity entry remains pending until admission is claimed', async ({ page }) => {
    await page.goto('/login?next=%2Fadmin%2Fsubscriptions%2F11111111-1111-1111-1111-111111111111');

    const textboxes = page.getByRole('textbox');

    await textboxes.nth(0).fill('pending-user@wordloom.dev');
    await textboxes.nth(1).fill('pending-user');
    await textboxes.nth(2).fill(LIBRARY_ID);
    await page.getByRole('button', { name: 'Log in' }).click();

    await expect(page).toHaveURL(new RegExp(`/onboarding/admission\\?next=%2Fadmin%2Fsubscriptions%2F${LIBRARY_ID}$`));
    await expect(page.getByRole('heading', { name: 'Claim tenant access' })).toBeVisible();

    await page.getByRole('textbox').nth(1).fill('ADMIN-DEMO');
    await page.getByRole('button', { name: 'Claim admission' }).click();

    await expect(page).toHaveURL(new RegExp(`/admin/subscriptions/${LIBRARY_ID}$`));
    await expect(page.getByRole('heading', { name: 'Subscription detail' })).toBeVisible();

    const storage = await page.evaluate(() =>
      ({
        authSession: JSON.parse(window.localStorage.getItem('wl_auth_session') || 'null'),
        currentTenantContext: JSON.parse(window.localStorage.getItem('wl_current_tenant_context') || 'null'),
      })
    );

    expect(storage.authSession?.admissionStatus).toBe('admitted');
    expect(storage.authSession?.admissionSource).toBe('code');
    expect(storage.authSession?.role).toBe('admin');
    expect(storage.authSession?.libraryId).toBe(LIBRARY_ID);
    expect(storage.currentTenantContext?.tenantId).toBe(LIBRARY_ID);
    expect(storage.currentTenantContext?.source).toBe('route');
  });
});