import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';
import { Button } from '@/shared/ui/button';
import { Spinner } from '@/shared/ui/spinner';
import { Modal } from '@/shared/ui/modal';
import type { PaginatedResponse, PagoInfo, PagoDetail } from '@/shared/types';

const STATUS_OPTIONS = [
  { value: '', label: 'Todos' },
  { value: 'pending', label: 'Pendiente' },
  { value: 'approved', label: 'Aprobado' },
  { value: 'rejected', label: 'Rechazado' },
  { value: 'in_process', label: 'En proceso' },
  { value: 'refunded', label: 'Reembolsado' },
  { value: 'cancelled', label: 'Cancelado' },
];

const STATUS_STYLES: Record<string, string> = {
  approved: 'bg-green-100 text-green-800',
  pending: 'bg-yellow-100 text-yellow-800',
  in_process: 'bg-blue-100 text-blue-800',
  rejected: 'bg-red-100 text-red-800',
  refunded: 'bg-purple-100 text-purple-800',
  cancelled: 'bg-gray-100 text-gray-800',
};

function StatusBadge({ status }: { status: string | null }) {
  const s = status || 'unknown';
  const styles = STATUS_STYLES[s] || 'bg-gray-100 text-gray-800';
  const labels: Record<string, string> = {
    approved: 'Aprobado',
    pending: 'Pendiente',
    in_process: 'En proceso',
    rejected: 'Rechazado',
    refunded: 'Reembolsado',
    cancelled: 'Cancelado',
  };
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${styles}`}>
      {labels[s] || s}
    </span>
  );
}

export default function AdminPagosPage() {
  const [page, setPage] = useState(1);
  const [mpStatus, setMpStatus] = useState('');
  const [fechaDesde, setFechaDesde] = useState('');
  const [fechaHasta, setFechaHasta] = useState('');
  const [selectedPagoId, setSelectedPagoId] = useState<number | null>(null);
  const [detailOpen, setDetailOpen] = useState(false);
  const [refundOpen, setRefundOpen] = useState(false);
  const [refundMotivo, setRefundMotivo] = useState('');
  const queryClient = useQueryClient();

  const { data, isLoading, error } = useQuery<PaginatedResponse<PagoInfo>>({
    queryKey: ['admin-pagos', page, mpStatus, fechaDesde, fechaHasta],
    queryFn: async () => {
      const params: Record<string, string | number> = { page, size: 20 };
      if (mpStatus) params.mp_status = mpStatus;
      if (fechaDesde) params.fecha_desde = new Date(fechaDesde).toISOString();
      if (fechaHasta) params.fecha_hasta = new Date(fechaHasta + 'T23:59:59').toISOString();
      const { data } = await apiClient.get(ENDPOINTS.ADMIN.PAGOS, { params });
      return data;
    },
  });

  const { data: pagoDetail, isLoading: detailLoading } = useQuery<PagoDetail>({
    queryKey: ['admin-pago-detail', selectedPagoId],
    queryFn: async () => {
      if (!selectedPagoId) return null;
      const { data } = await apiClient.get(ENDPOINTS.ADMIN.PAGO_BY_ID(selectedPagoId));
      return data;
    },
    enabled: selectedPagoId !== null && detailOpen,
  });

  const refundMutation = useMutation({
    mutationFn: async ({ pagoId, motivo }: { pagoId: number; motivo: string }) => {
      const { data } = await apiClient.post(ENDPOINTS.ADMIN.REEMBOLSAR(pagoId), { motivo });
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-pagos'] });
      setRefundOpen(false);
      setRefundMotivo('');
      setDetailOpen(false);
    },
  });

  const handleRefund = async () => {
    if (!selectedPagoId || !refundMotivo.trim() || refundMotivo.trim().length < 5) return;
    refundMutation.mutate({ pagoId: selectedPagoId, motivo: refundMotivo.trim() });
  };

  const formatDate = (d: string) => new Date(d).toLocaleDateString('es-AR', {
    year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Gesti&oacute;n de Pagos</h1>
        <p className="text-sm text-gray-500 mt-1">Visualiz&aacute; y gestion&aacute; los pagos del sistema.</p>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Estado</label>
            <select value={mpStatus} onChange={(e) => { setMpStatus(e.target.value); setPage(1); }}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm">
              {STATUS_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Fecha desde</label>
            <input type="date" value={fechaDesde} onChange={(e) => setFechaDesde(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Fecha hasta</label>
            <input type="date" value={fechaHasta} onChange={(e) => setFechaHasta(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm" />
          </div>
          <div className="flex items-end">
            <Button variant="outline" className="w-full" onClick={() => setPage(1)}>Filtrar</Button>
          </div>
        </div>
      </div>

      {isLoading && <div className="flex justify-center py-12"><Spinner size="lg" /></div>}
      {error && <div className="bg-red-50 border border-red-200 rounded-md p-4 text-red-700 text-sm">Error al cargar pagos.</div>}

      {data && (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          {data.items.length === 0 ? (
            <div className="text-center py-12 text-gray-500">No se encontraron pagos.</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Pedido</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monto</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {data.items.map(pago => (
                    <tr key={pago.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm text-gray-900">#{pago.id}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">#{pago.pedido_id}</td>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">
                        ${Number(pago.monto).toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                      </td>
                      <td className="px-4 py-3"><StatusBadge status={pago.mp_status} /></td>
                      <td className="px-4 py-3 text-sm text-gray-500">{formatDate(pago.creado_en)}</td>
                      <td className="px-4 py-3 text-right">
                        <div className="flex justify-end gap-1">
                          <Button variant="outline" size="sm"
                            onClick={() => { setSelectedPagoId(pago.id); setDetailOpen(true); }}>
                            Detalle
                          </Button>
                          {pago.mp_status === 'approved' && (
                            <Button variant="outline" size="sm"
                              className="text-purple-600 border-purple-300 hover:bg-purple-50"
                              onClick={() => { setSelectedPagoId(pago.id); setRefundOpen(true); }}>
                              Reembolsar
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

          {data.pages > 1 && (
            <div className="flex items-center justify-between px-4 py-3 border-t">
              <span className="text-sm text-gray-600">P&aacute;g {data.page} de {data.pages} ({data.total} pagos)</span>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage(p => p - 1)}>Anterior</Button>
                <Button variant="outline" size="sm" disabled={page >= data.pages} onClick={() => setPage(p => p + 1)}>Siguiente</Button>
              </div>
            </div>
          )}
        </div>
      )}

      <Modal isOpen={detailOpen} onClose={() => setDetailOpen(false)} title={`Pago #${selectedPagoId}`}>
        {detailLoading ? <div className="flex justify-center py-8"><Spinner /></div> :
         pagoDetail ? (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div><span className="text-gray-500">Pedido:</span> <span className="font-medium">#{pagoDetail.pedido_id}</span></div>
              <div><span className="text-gray-500">Monto:</span> <span className="font-medium">${Number(pagoDetail.monto).toLocaleString('es-AR', { minimumFractionDigits: 2 })}</span></div>
              <div><span className="text-gray-500">Estado MP:</span> <StatusBadge status={pagoDetail.mp_status} /></div>
              <div><span className="text-gray-500">MP Payment ID:</span> <span className="font-medium">{pagoDetail.mp_payment_id || '—'}</span></div>
              <div><span className="text-gray-500">External Ref:</span> <span className="font-medium">{pagoDetail.external_reference || '—'}</span></div>
              <div><span className="text-gray-500">Idempotency Key:</span> <span className="font-medium text-xs">{pagoDetail.idempotency_key || '—'}</span></div>
              <div><span className="text-gray-500">Creado:</span> <span>{formatDate(pagoDetail.creado_en)}</span></div>
              <div><span className="text-gray-500">Actualizado:</span> <span>{formatDate(pagoDetail.actualizado_en)}</span></div>
            </div>
            {pagoDetail.mp_status === 'approved' && (
              <div className="pt-4 border-t">
                <Button variant="outline" className="text-purple-600 border-purple-300"
                  onClick={() => { setDetailOpen(false); setTimeout(() => setRefundOpen(true), 100); }}>
                  Reembolsar pago
                </Button>
              </div>
            )}
          </div>
         ) : <p className="text-gray-500 text-center py-4">No se encontr&oacute; el pago</p>}
      </Modal>

      <Modal isOpen={refundOpen} onClose={() => { setRefundOpen(false); setRefundMotivo(''); }}
        title="Reembolsar pago">
        <div className="space-y-4">
          <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
            <p className="text-sm text-yellow-700">
              <strong>Advertencia:</strong> Se procesar&aacute; un reembolso a trav&eacute;s de MercadoPago. Esta acci&oacute;n no se puede deshacer.
            </p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Motivo del reembolso *</label>
            <textarea rows={3} value={refundMotivo} onChange={(e) => setRefundMotivo(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
              placeholder="Indic&aacute; el motivo del reembolso..." disabled={refundMutation.isPending} />
            {refundMotivo.length > 0 && refundMotivo.length < 5 && (
              <p className="text-xs text-red-500 mt-1">M&iacute;nimo 5 caracteres</p>
            )}
          </div>
          {refundMutation.error && (
            <div className="bg-red-50 border border-red-200 rounded-md p-3 text-sm text-red-700">
              {refundMutation.error instanceof Error ? refundMutation.error.message : 'Error al reembolsar'}
            </div>
          )}
          <div className="flex justify-end gap-3">
            <Button variant="outline" onClick={() => { setRefundOpen(false); setRefundMotivo(''); }}
              disabled={refundMutation.isPending}>Cancelar</Button>
            <Button onClick={handleRefund}
              disabled={!refundMotivo.trim() || refundMotivo.trim().length < 5 || refundMutation.isPending}>
              {refundMutation.isPending ? 'Procesando...' : 'Confirmar reembolso'}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
