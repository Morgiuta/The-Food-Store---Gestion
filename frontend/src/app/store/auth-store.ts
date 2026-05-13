import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: number;
  nombre: string;
  email: string;
  telefono?: string;
  roles: string[];
}

interface Tokens {
  access_token: string;
  refresh_token: string;
  token_type?: string;
}

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  user: User | null;
  isAuthenticated: boolean;

  setAuth: (user: User, tokens: Tokens) => void;
  logout: () => void;
  updateUser: (user: User) => void;
  setTokens: (tokens: Tokens) => void;
  hasRole: (role: string) => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      accessToken: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,

      setAuth: (user, tokens) => set({
        accessToken: tokens.access_token,
        refreshToken: tokens.refresh_token,
        user,
        isAuthenticated: true,
      }),
      logout: () => set({ accessToken: null, refreshToken: null, user: null, isAuthenticated: false }),
      updateUser: (user) => set({ user }),
      setTokens: (tokens) => set({ accessToken: tokens.access_token, refreshToken: tokens.refresh_token }),
      hasRole: (role) => get().user?.roles?.includes(role) ?? false,
    }),
    {
      name: 'food-store-auth',
      partialize: (state) => ({ accessToken: state.accessToken }),
    }
  )
);
