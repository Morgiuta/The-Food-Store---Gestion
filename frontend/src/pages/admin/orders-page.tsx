import { useState, useCallback, type FormEvent } from 'react';
import { useSearchParams } from 'react-router-dom';
import { usePedidosAdmin } from '@/features/pedidos/hooks/useOrders';
import { OrderStatusBadge } from '@/features/pedidos/components/order-status-badge';
import { OrderDetailModal } from '@/features/pedidos/components/order-detail-modal';
import { CancelOrderModal } from '@/features/pedidos/components/cancel-order-modal';
import { ChangeStatusModal } from '@/features/pedidos/components/change-status-modal';
import { Button } from '@/shared/ui/button';
import { Spinner } from '@/shared/ui/spinner';

const ESTADOS = [
  { value: '', label: 'Todos' },
  { value: '1', label: 'Pendiente' },
  { value: '2', label: 'Confirmado' },
  { value: '3', label: 'En Preparación' },
  { value: '4', label: 'En Camino' },
  { value: '5', label: 'Entregado' },
  { value: '6', label: 'Cancelado' },
];

export default function AdminOrdersPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialSearch = searchParams.get('search') ?? '';
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState(initialSearch);
  const [appliedSearch, setAppliedSearch] = useState(initialSearch);
  const [estadoId, setEstadoId] = useState<string>('');
  const [fechaDesde, setFechaDesde] = useState('');
  const [fechaHasta, setFechaHasta] = useState('');
  const [selectedOrderId, setSelectedOrderId] = useState<number | null>(null);
  const [detailOpen, setDetailOpen] = useState(false);
  const [cancelOpen, setCancelOpen] = useState(false);
  const [changeStatusOpen, setChangeStatusOpen] = useState(false);
  const [selectedEstado, setSelectedEstado] = useState('');

  const estadoIdNum = estadoId ? parseInt(estadoId) : undefined;
  const fechaDesdeDate = fechaDesde ? new Date(fechaDesde) : undefined;
  const fechaHastaDate = fechaHasta ? new Date(fechaHasta + 'T23:59:59') : undefined;

  const { data, isLoading, error } = usePedidosAdmin(
    page, 20, estadoIdNum, fechaDesdeDate, fechaHastaDate, appliedSearch || undefined
  );

  const handleViewDetail = (id: number) => {
    setSelectedOrderId(id);
    setDetailOpen(true);
  };

  const handleCancel = (id: number) => {
    setSelectedOrderId(id);
    setCancelOpen(true);
  };

  const handleChangeStatus = (id: number, estado: string) => {
    setSelectedOrderId(id);
    setSelectedEstado(estado);
    setChangeStatusOpen(true);
  };

  const handleFilter = useCallback((event?: FormEvent) => {
    event?.preventDefault();
    setPage(1);
    const q = search.trim();
    setAppliedSearch(q);
    setSearchParams(q ? { search: q } : {});
  }, [search, setSearchParams]);

  const handleClearFilters = () => {
    setSearch('');
    setAppliedSearch('');
    setEstadoId('');
    setFechaDesde('');
    setFechaHasta('');
    setPage(1);
    setSearchParams({});
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('es-AR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatCurrency = (value: number) => {
    return `$${value.toLocaleString('es-AR', { minimumFractionDigits: 2 })}`;
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Gestión de Pedidos</h1>
        <p className="text-sm text-gray-500 mt-1">
          Administrá los pedidos del sistema: avanzá estados, cancelá pedidos y consultá el historial.
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <form onSubmit={handleFilter} className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Buscar pedido</label>
            <input
              type="search"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="ID, cliente, email, producto o dirección"
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Estado</label>
            <select
              value={estadoId}
              onChange={(e) => setEstadoId(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
            >
              {ESTADOS.map((e) => (
                <option key={e.value} value={e.value}>{e.label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Fecha desde</label>
            <input
              type="date"
              value={fechaDesde}
              onChange={(e) => setFechaDesde(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Fecha hasta</label>
            <input
              type="date"
              value={fechaHasta}
              onChange={(e) => setFechaHasta(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
            />
          </div>
          <div className="flex items-end gap-2 md:col-span-5">
            <Button type="submit" variant="outline">
              Filtrar
            </Button>
            {(search || estadoId || fechaDesde || fechaHasta) && (
              <Button type="button" variant="outline" onClick={handleClearFilters}>
                Limpiar
              </Button>
            )}
          </div>
        </form>
      </div>

      {/* Loading */}
      {isLoading && (
        <div className="flex justify-center py-12">
          <Spinner size="lg" />
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4 text-red-700 text-sm">
          Error al cargar los pedidos. Intente de nuevo más tarde.
        </div>
      )}

      {/* Table */}
      {data && (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          {data.items.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <p>No se encontraron pedidos con los filtros seleccionados.</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Usuario</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {data.items.map((order) => (
                    <tr key={order.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">#{order.id}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">
                        {order.usuario_id || '—'}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {formatDate(order.creado_en)}
                      </td>
                      <td className="px-4 py-3">
                        <OrderStatusBadge estado={order.estado} />
                      </td>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">
                        {formatCurrency(Number(order.total))}
                      </td>
                      <td className="px-4 py-3 text-right">
                        <div className="flex items-center justify-end gap-1">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleViewDetail(order.id)}
                          >
                            Ver
                          </Button>
                          {['CONFIRMADO', 'EN_PREPARACION', 'EN_CAMINO'].includes(order.estado) && (
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleChangeStatus(order.id, order.estado)}
                            >
                              Avanzar
                            </Button>
                          )}
                          {['PENDIENTE', 'CONFIRMADO', 'EN_PREPARACION'].includes(order.estado) && (
                            <Button
                              variant="outline"
                              size="sm"
                              className="text-red-600 border-red-300 hover:bg-red-50"
                              onClick={() => handleCancel(order.id)}
                            >
                              Cancelar
                            </Button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Pagination */}
          {data.pages > 1 && (
            <div className="flex items-center justify-between px-4 py-3 bg-white border-t border-gray-200">
              <p className="text-sm text-gray-600">
                Página {data.page} de {data.pages} ({data.total} pedidos)
              </p>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  disabled={page <= 1}
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                >
                  Anterior
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={page >= data.pages}
                  onClick={() => setPage((p) => p + 1)}
                >
                  Siguiente
                </Button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Modals */}
      <OrderDetailModal
        pedidoId={selectedOrderId}
        isOpen={detailOpen}
        onClose={() => { setDetailOpen(false); setSelectedOrderId(null); }}
      />
      <CancelOrderModal
        pedidoId={selectedOrderId || 0}
        isOpen={cancelOpen}
        onClose={() => { setCancelOpen(false); setSelectedOrderId(null); }}
      />
      <ChangeStatusModal
        pedidoId={selectedOrderId || 0}
        estadoActual={selectedEstado}
        isOpen={changeStatusOpen}
        onClose={() => { setChangeStatusOpen(false); setSelectedOrderId(null); }}
      />
    </div>
  );
}
