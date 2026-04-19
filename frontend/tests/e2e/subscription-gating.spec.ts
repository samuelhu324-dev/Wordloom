import { test, expect } from '@playwright/test';

const LIBRARY_ID = '11111111-1111-1111-1111-111111111111';

type SessionRole = 'member' | 'admin' | 'owner';

function session(role: SessionRole) {
  return {
    email: `${role}@wordloom.dev`,
    displayName: `${role}-user`,
    role,
    libraryId: LIBRARY_ID,
    token: `wl-dev-${role}-playwright`,
    admissionStatus: 'admitted' as const,
    admissionSource: 'code' as const,
  };
}

async function seedSession(page: Parameters<typeof test>[0]['page'], role: SessionRole) {
  await page.addInitScript(({ authSession, libraryId }) => {
    window.localStorage.setItem('wl_auth_session', JSON.stringify(authSession));
    window.localStorage.setItem('wl_token', authSession.token);
    window.localStorage.setItem('wl_active_library_id', libraryId);
  }, { authSession: session(role), libraryId: LIBRARY_ID });
}

test.describe('Subscription gating', () => {
  test('anonymous user is redirected to shared login shell', async ({ page }) => {
    await page.goto('/workbox/subscription');

    await expect(page).toHaveURL(/\/login\?next=%2Fworkbox%2Fsubscription/);
    await expect(page.getByRole('heading', { name: 'Log in to Wordloom' })).toBeVisible();
  });

  test('member only sees My Subscription and is redirected away from admin console', async ({ page }) => {
    await seedSession(page, 'member');
    await page.goto('/workbox/subscription');

    await expect(page.getByRole('heading', { name: 'My Subscription' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'member-user · member' })).toHaveAttribute('href', '/workbox/subscription');
    await expect(page.getByRole('button', { name: 'Open Subscription Console' })).toHaveCount(0);

    await page.goto('/admin/subscriptions');
    await expect(page).toHaveURL(/\/workbox\/subscription/);
    await expect(page.getByRole('heading', { name: 'My Subscription' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Open Subscription Console' })).toHaveCount(0);
  });

  test('admin sees Subscription Console and can open admin route', async ({ page }) => {
    await seedSession(page, 'admin');
    await page.goto('/workbox/subscription');

    await expect(page.getByRole('heading', { name: 'My Subscription' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'admin-user · admin' })).toHaveAttribute('href', `/admin/subscriptions/${LIBRARY_ID}`);
    await expect(page.getByRole('button', { name: 'Open Subscription Console' })).toBeVisible();

    await page.getByRole('link', { name: 'admin-user · admin' }).click();
    await expect(page).toHaveURL(new RegExp(`/admin/subscriptions/${LIBRARY_ID}$`));
    await expect(page.getByRole('heading', { name: 'Subscription detail' })).toBeVisible();
  });
});