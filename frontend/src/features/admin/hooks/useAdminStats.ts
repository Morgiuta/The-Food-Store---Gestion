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
      return data;
    },
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useRevenue(periodo: string = 'day') {
  return useQuery<RevenueEntry[]>({
    queryKey: ['admin-revenue', periodo],
    queryFn: async () => {
      const { data } = await apiClient.get(ENDPOINTS.ADMIN.STATS_REVENUE, { params: { periodo } });
      return data;
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
