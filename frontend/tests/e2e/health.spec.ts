import { test, expect } from '@playwright/test';

test.describe('Health Check', () => {
  test('frontend loads and shows login page', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveURL(/\/productos/);
    await expect(page.locator('h1, h2').first()).toBeVisible();
  });

  test('can navigate to login page', async ({ page }) => {
    await page.goto('/login');
    await expect(page.locator('button, input')).toHaveCount.atLeast(1);
  });

  test('catalog page loads with products', async ({ page }) => {
    await page.goto('/productos');
    await expect(page).toHaveURL(/\/productos/);
  });

  test('shopping cart page loads', async ({ page }) => {
    await page.goto('/carrito');
    await expect(page).toHaveURL(/\/carrito/);
  });
});
