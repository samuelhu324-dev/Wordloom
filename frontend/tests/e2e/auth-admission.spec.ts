import { test, expect } from '@playwright/test';

const LIBRARY_ID = '11111111-1111-1111-1111-111111111111';

test.describe('Auth admission flow', () => {
  test('identity entry remains pending until admission is claimed', async ({ page }) => {
    await page.goto('/login');

    const textboxes = page.getByRole('textbox');

    await textboxes.nth(0).fill('pending-user@wordloom.dev');
    await textboxes.nth(1).fill('pending-user');
    await textboxes.nth(2).fill(LIBRARY_ID);
    await page.getByRole('button', { name: 'Log in' }).click();

    await expect(page).toHaveURL(/\/onboarding\/admission/);
    await expect(page.getByRole('heading', { name: 'Claim tenant access' })).toBeVisible();

    await page.goto('/workbox/subscription');
    await expect(page).toHaveURL(/\/onboarding\/admission/);

    await page.getByRole('textbox').nth(1).fill('ADMIN-DEMO');
    await page.getByRole('button', { name: 'Claim admission' }).click();

    await expect(page).toHaveURL(/\/admin\/subscriptions/);
    await expect(page.getByRole('heading', { name: 'Subscription Console' })).toBeVisible();

    const storage = await page.evaluate(() =>
      JSON.parse(window.localStorage.getItem('wl_auth_session') || 'null')
    );

    expect(storage?.admissionStatus).toBe('admitted');
    expect(storage?.admissionSource).toBe('code');
    expect(storage?.role).toBe('admin');
    expect(storage?.libraryId).toBe(LIBRARY_ID);
  });
});