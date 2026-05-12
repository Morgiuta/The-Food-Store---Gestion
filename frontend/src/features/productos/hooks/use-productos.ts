import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';
import type { Product, PaginatedResponse } from '@/shared/types';

export interface ProductCreate {
  nombre: string;
  descripcion?: string;
  imagen_url?: string;
  precio: number;
  stock_cantidad: number;
  disponible: boolean;
  categoria_ids?: number[];
  ingrediente_ids?: number[];
}

export interface ProductUpdate extends Partial<ProductCreate> {}

interface ProductosAdminParams {
  page?: number;
  per_page?: number;
  search?: string;
  disponible?: boolean;
}

export function useProductosAdmin(params?: ProductosAdminParams) {
  return useQuery<PaginatedResponse<Product>>({
    queryKey: ['productos', 'admin', params],
    queryFn: () =>
      apiClient.get(ENDPOINTS.PRODUCTOS.ADMIN, { params }).then((r) => r.data),
  });
}

export function useProducto(id: number) {
  return useQuery<Product>({
    queryKey: ['productos', id],
    queryFn: () =>
      apiClient.get(ENDPOINTS.PRODUCTOS.BY_ID(id)).then((r) => r.data),
    enabled: !!id,
  });
}

export function useCreateProducto() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: ProductCreate) =>
      apiClient.post(ENDPOINTS.PRODUCTOS.ADMIN, data).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['productos'] });
      qc.invalidateQueries({ queryKey: ['catalogo'] });
    },
  });
}

export function useUpdateProducto() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: ProductUpdate }) =>
      apiClient.put(ENDPOINTS.PRODUCTOS.BY_ID(id), data).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['productos'] });
      qc.invalidateQueries({ queryKey: ['catalogo'] });
    },
  });
}

export function useDeleteProducto() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) =>
      apiClient.delete(ENDPOINTS.PRODUCTOS.BY_ID(id)),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['productos'] });
      qc.invalidateQueries({ queryKey: ['catalogo'] });
    },
  });
}
