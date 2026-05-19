import { useQuery } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';

interface AdminStats {
  total_ventas: number;
  pedidos_hoy: number;
  usuarios_activos: number;
  stock_bajo: number;
}

interface RevenueEntry {
  fecha: string;
  ingresos: number | string;
}

export interface RevenueChartEntry {
  fecha: string;
  fechaLabel: string;
  ingresos: number;
}

interface OrderStatusCount {
  estado: string;
  cantidad: number;
}

interface ProductoStockBajo {
  id: number;
  nombre: string;
  stock_cantidad: number;
  disponible: boolean;
}

interface ProductoMasVendido {
  id: number;
  nombre: string;
  total_vendido: number;
}

interface ProductsStats {
  stock_bajo: ProductoStockBajo[];
  mas_vendidos: ProductoMasVendido[];
}

export function useAdminStats() {
  return useQuery<AdminStats>({
    queryKey: ['admin-stats'],
    queryFn: async () => {
      const { data } = await apiClient.get(ENDPOINTS.ADMIN.STATS);
      return {
        ...data,
        total_ventas: Number(data.total_ventas),
      };
    },
    refetchInterval: 5 * 60 * 1000,
  });
}

function formatRevenueDate(fecha: string, periodo: string) {
  const date = new Date(fecha);
  if (Number.isNaN(date.getTime())) return fecha;

  if (periodo === 'month') {
    return date.toLocaleDateString('es-AR', { month: 'short', year: '2-digit' });
  }

  if (periodo === 'week') {
    return `Sem. ${date.toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit' })}`;
  }

  return date.toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit' });
}

export function useRevenue(periodo: string = 'day') {
  return useQuery<RevenueChartEntry[]>({
    queryKey: ['admin-revenue', periodo],
    queryFn: async () => {
      const { data } = await apiClient.get(ENDPOINTS.ADMIN.STATS_REVENUE, { params: { periodo } });
      return (data as RevenueEntry[]).map((entry) => ({
        fecha: entry.fecha,
        fechaLabel: formatRevenueDate(entry.fecha, periodo),
        ingresos: Number(entry.ingresos),
      }));
    },
  });
}

export function useOrdersByStatus() {
  return useQuery<OrderStatusCount[]>({
    queryKey: ['admin-orders-status'],
    queryFn: async () => {
      const { data } = await apiClient.get(ENDPOINTS.ADMIN.STATS_ORDERS);
      return data;
    },
  });
}

export function useProductsStats() {
  return useQuery<ProductsStats>({
    queryKey: ['admin-products-stats'],
    queryFn: async () => {
      const { data } = await apiClient.get(ENDPOINTS.ADMIN.STATS_PRODUCTS);
      return data;
    },
  });
}
