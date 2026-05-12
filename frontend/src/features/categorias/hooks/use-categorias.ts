import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';

export interface Categoria {
  id: number;
  nombre: string;
  descripcion?: string;
  imagen_url?: string;
  padre_id?: number | null;
  subcategorias?: Categoria[];
}

export interface CategoriaCreate {
  nombre: string;
  descripcion?: string;
  imagen_url?: string;
  padre_id?: number | null;
}

export function useCategorias() {
  return useQuery<Categoria[]>({
    queryKey: ['categorias'],
    queryFn: () => apiClient.get(ENDPOINTS.CATEGORIAS.BASE).then(r => r.data),
  });
}

export function useCategoria(id: number) {
  return useQuery<Categoria>({
    queryKey: ['categorias', id],
    queryFn: () => apiClient.get(ENDPOINTS.CATEGORIAS.BY_ID(id)).then(r => r.data),
    enabled: !!id,
  });
}

export function useCreateCategoria() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: CategoriaCreate) =>
      apiClient.post(ENDPOINTS.CATEGORIAS.BASE, data).then(r => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['categorias'] }),
  });
}

export function useUpdateCategoria() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<CategoriaCreate> }) =>
      apiClient.put(ENDPOINTS.CATEGORIAS.BY_ID(id), data).then(r => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['categorias'] }),
  });
}

export function useDeleteCategoria() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) =>
      apiClient.delete(ENDPOINTS.CATEGORIAS.BY_ID(id)),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['categorias'] }),
  });
}
