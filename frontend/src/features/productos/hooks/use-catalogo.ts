import { useQuery } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';
import type { Product } from '@/shared/types';

interface CatalogoParams {
  categoria_id?: number;
  page?: number;
  per_page?: number;
}

export function useCatalogo(params?: CatalogoParams) {
  return useQuery<Product[]>({
    queryKey: ['catalogo', params],
    queryFn: () =>
      apiClient.get(ENDPOINTS.PRODUCTOS.BASE, { params }).then((r) => r.data),
  });
}
