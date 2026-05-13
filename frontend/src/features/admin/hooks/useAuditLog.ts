import { useQuery } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';

interface AuditEntry {
  id: number;
  usuario_id: number | null;
  accion: string;
  tabla: string;
  registro_id: number | null;
  valor_anterior: string | null;
  valor_nuevo: string | null;
  ip_address: string | null;
  created_at: string;
}

interface PaginatedAudit {
  items: AuditEntry[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

interface AuditFilters {
  page?: number;
  size?: number;
  tabla?: string;
  accion?: string;
  usuario_id?: number;
  fecha_desde?: string;
  fecha_hasta?: string;
}

export function useAuditLog(filters: AuditFilters = {}) {
  return useQuery<PaginatedAudit>({
    queryKey: ['admin-audit', filters],
    queryFn: async () => {
      const params: Record<string, string | number> = { page: filters.page || 1, size: filters.size || 50 };
      if (filters.tabla) params.tabla = filters.tabla;
      if (filters.accion) params.accion = filters.accion;
      if (filters.usuario_id) params.usuario_id = filters.usuario_id;
      if (filters.fecha_desde) params.fecha_desde = filters.fecha_desde;
      if (filters.fecha_hasta) params.fecha_hasta = filters.fecha_hasta;
      const { data } = await apiClient.get(ENDPOINTS.ADMIN.AUDIT, { params });
      return data;
    },
  });
}
