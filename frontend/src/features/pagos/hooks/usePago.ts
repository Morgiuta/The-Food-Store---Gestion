import { useQuery, useMutation } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';

interface CrearPagoResponse {
  preference_id: string;
  init_point: string;
}

interface PagoInfo {
  id: number;
  pedido_id: number;
  monto: number;
  mp_status: string | null;
  external_reference: string | null;
  creado_en: string;
}

export function useCrearPago() {
  return useMutation<CrearPagoResponse, Error, { pedido_id: number }>({
    mutationFn: async ({ pedido_id }) => {
      const { data } = await apiClient.post(ENDPOINTS.PAGOS.CREATE, { pedido_id });
      return data;
    },
  });
}

export function useEstadoPago(pedidoId: number | null) {
  return useQuery<PagoInfo | null>({
    queryKey: ['pago', pedidoId],
    queryFn: async () => {
      if (!pedidoId) return null;
      const { data } = await apiClient.get(ENDPOINTS.PAGOS.BY_PEDIDO(pedidoId));
      return data;
    },
    enabled: pedidoId !== null,
    refetchInterval: (query) => {
      const estado = query.state.data?.mp_status;
      if (estado === 'pending' || estado === 'in_process') {
        return 3000;
      }
      return false;
    },
  });
}
