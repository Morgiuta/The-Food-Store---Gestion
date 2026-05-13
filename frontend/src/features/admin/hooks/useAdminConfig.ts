import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';

interface ConfigItem {
  clave: string;
  valor: string;
  descripcion: string | null;
}

interface FormaPago {
  id: number;
  nombre: string;
  activo: boolean;
}

export function useConfig() {
  return useQuery<ConfigItem[]>({
    queryKey: ['admin-config'],
    queryFn: async () => {
      const { data } = await apiClient.get(ENDPOINTS.ADMIN.CONFIG);
      return data;
    },
  });
}

export function useUpdateConfig() {
  const queryClient = useQueryClient();
  return useMutation<ConfigItem[], Error, ConfigItem[]>({
    mutationFn: async (configuraciones) => {
      const { data } = await apiClient.put(ENDPOINTS.ADMIN.CONFIG, { configuraciones });
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-config'] });
    },
  });
}

export function useFormasPago() {
  return useQuery<FormaPago[]>({
    queryKey: ['admin-formas-pago'],
    queryFn: async () => {
      const { data } = await apiClient.get(ENDPOINTS.ADMIN.FORMAS_PAGO);
      return data;
    },
  });
}

export function useToggleFormaPago() {
  const queryClient = useQueryClient();
  return useMutation<FormaPago, Error, { id: number; activo: boolean }>({
    mutationFn: async ({ id, activo }) => {
      const { data } = await apiClient.patch(ENDPOINTS.ADMIN.FORMA_PAGO_BY_ID(id), { activo });
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-formas-pago'] });
    },
  });
}
