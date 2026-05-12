import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';

export interface Ingrediente {
  id: number;
  nombre: string;
  descripcion?: string;
  es_alergeno: boolean;
}

export interface IngredienteCreate {
  nombre: string;
  descripcion?: string;
  es_alergeno?: boolean;
}

interface IngredientesParams {
  es_alergeno?: boolean;
}

export function useIngredientes(params?: IngredientesParams) {
  return useQuery<Ingrediente[]>({
    queryKey: ['ingredientes', params],
    queryFn: () =>
      apiClient
        .get(ENDPOINTS.INGREDIENTES.BASE, { params })
        .then((r) => r.data),
  });
}

export function useCreateIngrediente() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: IngredienteCreate) =>
      apiClient.post(ENDPOINTS.INGREDIENTES.BASE, data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['ingredientes'] }),
  });
}

export function useUpdateIngrediente() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<IngredienteCreate> }) =>
      apiClient.put(ENDPOINTS.INGREDIENTES.BY_ID(id), data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['ingredientes'] }),
  });
}

export function useDeleteIngrediente() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) =>
      apiClient.delete(ENDPOINTS.INGREDIENTES.BY_ID(id)),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['ingredientes'] }),
  });
}
