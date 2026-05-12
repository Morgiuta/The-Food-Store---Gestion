import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';

interface AdminUsuariosParams {
  skip?: number;
  limit?: number;
  search?: string;
  rol?: string;
}

export function useAdminUsuarios(params: AdminUsuariosParams) {
  return useQuery({
    queryKey: ['admin', 'usuarios', params],
    queryFn: () =>
      apiClient.get(ENDPOINTS.ADMIN.USUARIOS, { params }).then((r) => r.data),
  });
}

export function useUpdateUsuario() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Record<string, unknown> }) =>
      apiClient.put(ENDPOINTS.ADMIN.USUARIO_BY_ID(id), data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin', 'usuarios'] });
    },
  });
}

export function useToggleEstado() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) =>
      apiClient.patch(ENDPOINTS.ADMIN.USUARIO_ESTADO(id)).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin', 'usuarios'] });
    },
  });
}
