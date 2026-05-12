import { useMutation } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';
import { useAuthStore } from '@/app/store/auth-store';

export function useUpdatePerfil() {
  return useMutation({
    mutationFn: (data: Record<string, unknown>) =>
      apiClient.put(ENDPOINTS.PERFIL.BASE, data).then((r) => r.data),
    onSuccess: (data) => {
      useAuthStore.getState().updateUser(data);
    },
  });
}

export function useChangePassword() {
  return useMutation({
    mutationFn: (data: { password_actual: string; password_nueva: string }) =>
      apiClient.put(ENDPOINTS.PERFIL.PASSWORD, data),
  });
}
