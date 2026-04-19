import { test, expect } from '@playwright/test';

async function getLibraryId(request: Parameters<typeof test>[0]['request']) {
  const response = await request.get('/api/v1/libraries');
  expect(response.ok()).toBeTruthy();
  const libraries = (await response.json()) as Array<{ id: string }>;
  expect(libraries.length).toBeGreaterThan(0);
  return libraries[0].id;
}

test.describe('Auth admission flow', () => {
  test('identity entry remains pending until admission is claimed', async ({ page, request }) => {
    const libraryId = await getLibraryId(request);

    await page.goto(`/login?next=${encodeURIComponent(`/admin/subscriptions/${libraryId}`)}`);

    const textboxes = page.getByRole('textbox');

    await textboxes.nth(0).fill('pending-user@wordloom.dev');
    await textboxes.nth(1).fill('pending-user');
    await textboxes.nth(2).fill(libraryId);
    await page.getByRole('button', { name: 'Log in' }).click();

    await expect(page).toHaveURL(new RegExp(`/onboarding/admission\\?next=%2Fadmin%2Fsubscriptions%2F${libraryId}$`));
    await expect(page.getByRole('heading', { name: 'Claim tenant access' })).toBeVisible();

    await page.getByRole('textbox').nth(1).fill('ADMIN-DEMO');
    await page.getByRole('button', { name: 'Claim admission' }).click();

    await expect(page).toHaveURL(new RegExp(`/admin/subscriptions/${libraryId}$`));
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
    expect(storage.authSession?.libraryId).toBe(libraryId);
    expect(storage.currentTenantContext?.tenantId).toBe(libraryId);
    expect(storage.currentTenantContext?.source).toBe('route');
  });
});