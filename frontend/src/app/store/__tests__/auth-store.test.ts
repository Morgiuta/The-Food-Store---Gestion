import { describe, it, expect, beforeEach } from 'vitest';
import { useAuthStore } from '@/app/store/auth-store';

describe('authStore', () => {
  beforeEach(() => {
    useAuthStore.setState({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
    });
    localStorage.clear();
  });

  it('should start unauthenticated', () => {
    const state = useAuthStore.getState();
    expect(state.isAuthenticated).toBe(false);
    expect(state.user).toBeNull();
    expect(state.accessToken).toBeNull();
  });

  it('should set auth on login', () => {
    const mockUser = { id: 1, nombre: 'Test', email: 'test@test.com', roles: ['CLIENT'] };
    useAuthStore.getState().setAuth(mockUser as any, {
      access_token: 'access123',
      refresh_token: 'refresh123',
      token_type: 'bearer',
    });

    const state = useAuthStore.getState();
    expect(state.isAuthenticated).toBe(true);
    expect(state.user?.nombre).toBe('Test');
    expect(state.accessToken).toBe('access123');
    expect(state.refreshToken).toBe('refresh123');
  });

  it('should clear auth on logout', () => {
    const mockUser = { id: 1, nombre: 'Test', email: 'test@test.com', roles: ['CLIENT'] };
    useAuthStore.getState().setAuth(mockUser as any, {
      access_token: 'access123',
      refresh_token: 'refresh123',
      token_type: 'bearer',
    });
    useAuthStore.getState().logout();

    const state = useAuthStore.getState();
    expect(state.isAuthenticated).toBe(false);
    expect(state.user).toBeNull();
    expect(state.accessToken).toBeNull();
    expect(state.refreshToken).toBeNull();
  });

  it('should update tokens on refresh', () => {
    useAuthStore.getState().setAuth({} as any, { access_token: 'old_access', refresh_token: 'old_refresh', token_type: 'bearer' });
    useAuthStore.getState().setTokens({ access_token: 'new_access', refresh_token: 'new_refresh', token_type: 'bearer' });

    const state = useAuthStore.getState();
    expect(state.accessToken).toBe('new_access');
    expect(state.refreshToken).toBe('new_refresh');
  });
});
