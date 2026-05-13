import { useState } from 'react';
import { usePedidoDetail } from '../hooks/useOrders';
import { OrderStatusBadge } from './order-status-badge';
import { OrderHistoryTimeline } from './order-history-timeline';
import { CancelOrderModal } from './cancel-order-modal';
import { ChangeStatusModal } from './change-status-modal';
import { Modal } from '@/shared/ui/modal';
import { Spinner } from '@/shared/ui/spinner';
import { Button } from '@/shared/ui/button';
import { useAuthStore } from '@/app/store/auth-store';

interface Props {
  pedidoId: number | null;
  isOpen: boolean;
  onClose: () => void;
}

const ESTADOS_CANCELABLES = ['PENDIENTE', 'CONFIRMADO', 'EN_PREPARACION'];
const ESTADOS_AVANZABLES = ['CONFIRMADO', 'EN_PREPARACION', 'EN_CAMINO'];

export function OrderDetailModal({ pedidoId, isOpen, onClose }: Props) {
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [showChangeStatus, setShowChangeStatus] = useState(false);
  const { data: pedido, isLoading, error } = usePedidoDetail(pedidoId);
  const userRoles = useAuthStore((state) => state.user?.roles || []);

  const isAdmin = userRoles.includes('ADMIN') || userRoles.includes('PEDIDOS');
  const estadoActual = pedido?.estado || '';
  const canCancel = ESTADOS_CANCELABLES.includes(estadoActual);
  const canAdvance = ESTADOS_AVANZABLES.includes(estadoActual) && isAdmin;

  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose} title={`Pedido #${pedidoId}`}>
        {isLoading && (
          <div className="flex justify-center py-8">
            <Spinner />
          </div>
        )}

        {error && (
          <div className="text-red-500 text-center py-4">
            Error al cargar el pedido
          </div>
        )}

        {pedido && (
          <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">
                  {new Date(pedido.creado_en).toLocaleDateString('es-AR', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </p>
              </div>
              <OrderStatusBadge estado={pedido.estado} />
            </div>

            {/* Items */}
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Productos</h4>
              <div className="space-y-2">
                {pedido.detalles.map((det) => (
                  <div key={det.id} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0">
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {det.producto_nombre || `Producto #${det.producto_id}`}
                      </p>
                      <p className="text-xs text-gray-500">
                        Cantidad: {det.cantidad} × ${Number(det.precio_unitario).toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                      </p>
                      {det.personalizacion && det.personalizacion.length > 0 && (
                        <p className="text-xs text-gray-400">
                          Ingredientes excluidos: {det.personalizacion.join(', ')}
                        </p>
                      )}
                    </div>
                    <p className="text-sm font-semibold">
                      ${Number(det.subtotal).toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Totals */}
            <div className="border-t border-gray-200 pt-4 space-y-1">
              <div className="flex justify-between text-sm text-gray-600">
                <span>Subtotal</span>
                <span>${(Number(pedido.total) - Number(pedido.costo_envio)).toLocaleString('es-AR', { minimumFractionDigits: 2 })}</span>
              </div>
              <div className="flex justify-between text-sm text-gray-600">
                <span>Envío</span>
                <span>${Number(pedido.costo_envio).toLocaleString('es-AR', { minimumFractionDigits: 2 })}</span>
              </div>
              <div className="flex justify-between text-base font-semibold text-gray-900 pt-1">
                <span>Total</span>
                <span>${Number(pedido.total).toLocaleString('es-AR', { minimumFractionDigits: 2 })}</span>
              </div>
            </div>

            {/* Action buttons */}
            {(canCancel || canAdvance) && (
              <div className="flex gap-2 border-t border-gray-200 pt-4">
                {canAdvance && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setShowChangeStatus(true)}
                  >
                    Avanzar estado
                  </Button>
                )}
                {canCancel && (
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => setShowCancelModal(true)}
                  >
                    Cancelar pedido
                  </Button>
                )}
              </div>
            )}

            {/* History Timeline */}
            {pedido.historial && pedido.historial.length > 0 && (
              <div className="border-t border-gray-200 pt-4">
                <h4 className="font-medium text-gray-900 mb-4">Historial de estados</h4>
                <OrderHistoryTimeline historial={pedido.historial} />
              </div>
            )}
          </div>
        )}
      </Modal>

      {/* Nested modals */}
      {pedidoId && (
        <>
          <CancelOrderModal
            pedidoId={pedidoId}
            isOpen={showCancelModal}
            onClose={() => setShowCancelModal(false)}
          />
          <ChangeStatusModal
            pedidoId={pedidoId}
            estadoActual={estadoActual}
            isOpen={showChangeStatus}
            onClose={() => setShowChangeStatus(false)}
          />
        </>
      )}
    </>
  );
}
