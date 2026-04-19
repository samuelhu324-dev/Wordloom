import { test, expect } from '@playwright/test';

async function getLibraryId(request: Parameters<typeof test>[0]['request']) {
  const response = await request.get('/api/v1/libraries');
  expect(response.ok()).toBeTruthy();
  const libraries = (await response.json()) as Array<{ id: string }>;
  expect(libraries.length).toBeGreaterThan(0);
  return libraries[0].id;
}

test.describe('Identity to membership to entry closure', () => {
  test('registration closes into admitted member entry under explicit tenant scope', async ({ page, request }) => {
    const libraryId = await getLibraryId(request);

    await page.goto('/register');

    const textboxes = page.getByRole('textbox');

    await textboxes.nth(0).fill('member-closure-user');
    await textboxes.nth(1).fill('member-closure@wordloom.dev');
    await textboxes.nth(2).fill(libraryId);
    await page.getByRole('button', { name: 'Register' }).click();

    await expect(page).toHaveURL(/\/onboarding\/admission$/);
    await expect(page.getByRole('heading', { name: 'Claim tenant access' })).toBeVisible();

    await page.getByRole('textbox').nth(1).fill('MEMBER-DEMO');
    await page.getByRole('button', { name: 'Claim admission' }).click();

    await expect(page).toHaveURL(/\/workbox\/subscription$/);
    await expect(page.getByRole('heading', { name: 'My Subscription' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Open Subscription Console' })).toHaveCount(0);

    await page.goto(`/admin/subscriptions/${libraryId}`);
    await expect(page).toHaveURL(/\/workbox\/subscription$/);

    const storage = await page.evaluate(() => ({
      authSession: JSON.parse(window.localStorage.getItem('wl_auth_session') || 'null'),
      currentTenantContext: JSON.parse(window.localStorage.getItem('wl_current_tenant_context') || 'null'),
    }));

    expect(storage.authSession?.admissionStatus).toBe('admitted');
    expect(storage.authSession?.admissionSource).toBe('code');
    expect(storage.authSession?.role).toBe('member');
    expect(storage.authSession?.libraryId).toBe(libraryId);
    expect(storage.currentTenantContext?.tenantId).toBe(libraryId);
    expect(storage.currentTenantContext?.source).toBe('session');
  });
});