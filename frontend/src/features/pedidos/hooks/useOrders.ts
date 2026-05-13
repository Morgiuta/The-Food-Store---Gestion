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

export function usePedidosAdmin(
  page: number = 1,
  size: number = 20,
  estadoId?: number,
  fechaDesde?: Date,
  fechaHasta?: Date,
) {
  return useQuery<PaginatedResponse<Order>>({
    queryKey: ['pedidos-admin', page, size, estadoId, fechaDesde, fechaHasta],
    queryFn: async () => {
      const params: Record<string, string | number> = { page, size };
      if (estadoId !== undefined) params.estado_id = estadoId;
      if (fechaDesde) params.fecha_desde = fechaDesde.toISOString();
      if (fechaHasta) params.fecha_hasta = fechaHasta.toISOString();
      const { data } = await apiClient.get(ENDPOINTS.PEDIDOS.ADMIN_ALL, { params });
      return data;
    },
  });
}

export function useAvanzarEstado() {
  const queryClient = useQueryClient();

  return useMutation<OrderFull, Error, { pedidoId: number; nuevoEstado: string; observacion?: string }>({
    mutationFn: async ({ pedidoId, nuevoEstado, observacion }) => {
      const { data } = await apiClient.patch(ENDPOINTS.PEDIDOS.CHANGE_STATUS(pedidoId), {
        nuevo_estado: nuevoEstado,
        observacion,
      });
      return data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['pedido', data.id] });
      queryClient.invalidateQueries({ queryKey: ['mis-pedidos'] });
      queryClient.invalidateQueries({ queryKey: ['pedidos-admin'] });
    },
  });
}

export function useCancelarPedido() {
  const queryClient = useQueryClient();

  return useMutation<OrderFull, Error, { pedidoId: number; motivo: string }>({
    mutationFn: async ({ pedidoId, motivo }) => {
      const { data } = await apiClient.patch(ENDPOINTS.PEDIDOS.CANCEL(pedidoId), { motivo });
      return data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['pedido', data.id] });
      queryClient.invalidateQueries({ queryKey: ['mis-pedidos'] });
      queryClient.invalidateQueries({ queryKey: ['pedidos-admin'] });
    },
  });
}
