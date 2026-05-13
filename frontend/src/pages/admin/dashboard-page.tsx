import { useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend,
} from 'recharts';
import { useAdminStats, useRevenue, useOrdersByStatus, useProductsStats } from '@/features/admin/hooks/useAdminStats';
import { Button } from '@/shared/ui/button';
import { Spinner } from '@/shared/ui/spinner';

const PIE_COLORS: Record<string, string> = {
  PENDIENTE: '#F59E0B',
  CONFIRMADO: '#3B82F6',
  EN_PREPARACION: '#F97316',
  EN_CAMINO: '#06B6D4',
  ENTREGADO: '#10B981',
  CANCELADO: '#EF4444',
};

function formatCurrency(value: number) {
  return `$${value.toLocaleString('es-AR', { minimumFractionDigits: 2 })}`;
}

function StatCard({ title, value, subtitle, color }: { title: string; value: string | number; subtitle?: string; color: string }) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <p className="text-sm text-gray-500 mb-1">{title}</p>
      <p className={`text-2xl font-bold ${color}`}>{value}</p>
      {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
    </div>
  );
}

export default function AdminDashboardPage() {
  const [periodo, setPeriodo] = useState('day');
  const { data: stats, isLoading: statsLoading } = useAdminStats();
  const { data: revenue, isLoading: revenueLoading } = useRevenue(periodo);
  const { data: ordersByStatus, isLoading: ordersLoading } = useOrdersByStatus();
  const { data: productsStats, isLoading: productsLoading } = useProductsStats();

  const isLoading = statsLoading || revenueLoading || ordersLoading || productsLoading;

  if (isLoading) {
    return <div className="flex justify-center py-16"><Spinner size="lg" /></div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-sm text-gray-500 mt-1">Resumen de métricas y actividad del sistema.</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Ventas totales"
          value={stats ? formatCurrency(stats.total_ventas) : '—'}
          color="text-green-600"
        />
        <StatCard
          title="Pedidos hoy"
          value={stats?.pedidos_hoy ?? '—'}
          color="text-blue-600"
        />
        <StatCard
          title="Usuarios activos"
          value={stats?.usuarios_activos ?? '—'}
          color="text-amber-600"
        />
        <StatCard
          title="Stock bajo"
          value={stats?.stock_bajo ?? '—'}
          color={stats && stats.stock_bajo > 0 ? 'text-red-600' : 'text-gray-600'}
          subtitle={stats && stats.stock_bajo > 0 ? 'Productos con stock < 5' : 'Sin alertas'}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue Chart */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Ingresos</h2>
            <div className="flex gap-1">
              {(['day', 'week', 'month'] as const).map((p) => (
                <Button
                  key={p}
                  variant={periodo === p ? 'primary' : 'outline'}
                  size="sm"
                  onClick={() => setPeriodo(p)}
                >
                  {p === 'day' ? '7 días' : p === 'week' ? '4 semanas' : '6 meses'}
                </Button>
              ))}
            </div>
          </div>
          {revenue && revenue.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={revenue}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="fecha" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip formatter={(value) => formatCurrency(value as number)} />
                <Bar dataKey="ingresos" fill="#F59E0B" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-64 text-gray-400">
              Sin datos de ingresos
            </div>
          )}
        </div>

        {/* Orders by Status Pie */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Pedidos por estado</h2>
          {ordersByStatus && ordersByStatus.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={ordersByStatus}
                  dataKey="cantidad"
                  nameKey="estado"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={(entry: any) => `${entry.estado}: ${entry.cantidad}`}
                >
                  {ordersByStatus.map((entry) => (
                    <Cell key={entry.estado} fill={PIE_COLORS[entry.estado] || '#9CA3AF'} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-64 text-gray-400">
              Sin pedidos registrados
            </div>
          )}
        </div>
      </div>

      {/* Low Stock + Top Products */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Low Stock */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Stock bajo</h2>
          {productsStats && productsStats.stock_bajo.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Producto</th>
                    <th className="px-3 py-2 text-right text-xs font-medium text-gray-500 uppercase">Stock</th>
                    <th className="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase">Disponible</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {productsStats.stock_bajo.map((p) => (
                    <tr key={p.id} className="hover:bg-gray-50">
                      <td className="px-3 py-2 text-sm text-gray-900">{p.nombre}</td>
                      <td className="px-3 py-2 text-sm text-right font-medium text-red-600">{p.stock_cantidad}</td>
                      <td className="px-3 py-2 text-sm text-center">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                          p.disponible ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {p.disponible ? 'Sí' : 'No'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-400">No hay productos con stock bajo.</div>
          )}
        </div>

        {/* Top Products */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Más vendidos</h2>
          {productsStats && productsStats.mas_vendidos.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">#</th>
                    <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Producto</th>
                    <th className="px-3 py-2 text-right text-xs font-medium text-gray-500 uppercase">Vendidos</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {productsStats.mas_vendidos.map((p, i) => (
                    <tr key={p.id} className="hover:bg-gray-50">
                      <td className="px-3 py-2 text-sm text-gray-400">{i + 1}</td>
                      <td className="px-3 py-2 text-sm text-gray-900">{p.nombre}</td>
                      <td className="px-3 py-2 text-sm text-right font-medium text-gray-900">{p.total_vendido}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-400">No hay datos de ventas.</div>
          )}
        </div>
      </div>
    </div>
  );
}
