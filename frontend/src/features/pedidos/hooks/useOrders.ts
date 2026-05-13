import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';
import type { Order, OrderFull, CreateOrderPayload, PaginatedResponse } from '@/shared/types';

export function useMisPedidos(page: number = 1, size: number = 20) {
  return useQuery<PaginatedResponse<Order>>({
    queryKey: ['mis-pedidos', page, size],
    queryFn: async () => {
      const { data } = await apiClient.get(ENDPOINTS.PEDIDOS.BASE, { params: { page, size } });
      return data;
    },
  });
}

export function usePedidoDetail(id: number | null) {
  return useQuery<OrderFull>({
    queryKey: ['pedido', id],
    queryFn: async () => {
      const { data } = await apiClient.get(ENDPOINTS.PEDIDOS.BY_ID(id!));
      return data;
    },
    enabled: id !== null,
  });
}

export function useCrearPedido() {
  const queryClient = useQueryClient();

  return useMutation<OrderFull, Error, CreateOrderPayload>({
    mutationFn: async (payload) => {
      const { data } = await apiClient.post(ENDPOINTS.PEDIDOS.BASE, payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['mis-pedidos'] });
    },
  });
}

export function usePedidosAdmin(page: number = 1, size: number = 20, estadoId?: number) {
  return useQuery<PaginatedResponse<Order>>({
    queryKey: ['pedidos-admin', page, size, estadoId],
    queryFn: async () => {
      const params: Record<string, number> = { page, size };
      if (estadoId !== undefined) params.estado_id = estadoId;
      const { data } = await apiClient.get(ENDPOINTS.PEDIDOS.ADMIN_ALL, { params });
      return data;
    },
  });
}
