import { useMutation } from '@tanstack/react-query';
import { useAuthStore } from '@/app/store/auth-store';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';
import type { ApiResponse, AuthTokens, Rol, User } from '@/shared/types';

interface LoginCredentials {
  email: string;
  password: string;
}

interface LoginResponse {
  user: User;
  access_token: string;
  refresh_token: string;
  token_type: string;
}

interface RegisterData {
  nombre: string;
  email: string;
  password: string;
  telefono?: string;
}

type AuthResponse = LoginResponse | ApiResponse<LoginResponse>;

function unwrapAuthResponse(response: AuthResponse): LoginResponse {
  if ('data' in response) {
    return response.data;
  }
  return response;
}

export function useAuth() {
  const { user, isAuthenticated, setAuth, logout: storeLogout } = useAuthStore();

  const loginMutation = useMutation({
    mutationFn: async (credentials: LoginCredentials) => {
      const { data } = await apiClient.post<AuthResponse>(
        ENDPOINTS.AUTH.LOGIN,
        credentials,
      );
      return unwrapAuthResponse(data);
    },
    onSuccess: (response) => {
      const tokens: AuthTokens = {
        access_token: response.access_token,
        refresh_token: response.refresh_token,
        token_type: response.token_type,
      };
      setAuth(response.user, tokens);
    },
  });

  const registerMutation = useMutation({
    mutationFn: async (registerData: RegisterData) => {
      const { data } = await apiClient.post<AuthResponse>(
        ENDPOINTS.AUTH.REGISTER,
        registerData,
      );
      return unwrapAuthResponse(data);
    },
    onSuccess: (response) => {
      const tokens: AuthTokens = {
        access_token: response.access_token,
        refresh_token: response.refresh_token,
        token_type: response.token_type,
      };
      setAuth(response.user, tokens);
    },
  });

  const logoutMutation = useMutation({
    mutationFn: async () => {
      const refreshToken = useAuthStore.getState().refreshToken;
      if (refreshToken) {
        await apiClient.post(ENDPOINTS.AUTH.LOGOUT, { refresh_token: refreshToken });
      }
    },
    onSettled: () => {
      storeLogout();
    },
  });

  const logout = () => {
    logoutMutation.mutate();
  };

  const hasRole = (role: Rol): boolean => {
    if (!user?.roles) return false;
    return user.roles.includes(role);
  };

  const hasAnyRole = (roles: Rol[]): boolean => {
    if (!user?.roles) return false;
    return roles.some((role) => user.roles?.includes(role));
  };

  return {
    user,
    isAuthenticated,
    login: loginMutation.mutate,
    loginAsync: loginMutation.mutateAsync,
    isLoggingIn: loginMutation.isPending,
    loginError: loginMutation.error,
    register: registerMutation.mutate,
    registerAsync: registerMutation.mutateAsync,
    isRegistering: registerMutation.isPending,
    registerError: registerMutation.error,
    logout,
    isLoggingOut: logoutMutation.isPending,
    hasRole,
    hasAnyRole,
  };
}
