import { usePedidoDetail } from '../hooks/useOrders';
import { OrderStatusBadge } from './order-status-badge';
import { Modal } from '@/shared/ui/modal';
import { Spinner } from '@/shared/ui/spinner';

interface Props {
  pedidoId: number | null;
  isOpen: boolean;
  onClose: () => void;
}

export function OrderDetailModal({ pedidoId, isOpen, onClose }: Props) {
  const { data: pedido, isLoading, error } = usePedidoDetail(pedidoId);

  return (
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

          {/* History */}
          {pedido.historial && pedido.historial.length > 0 && (
            <div className="border-t border-gray-200 pt-4">
              <h4 className="font-medium text-gray-900 mb-2">Historial de estados</h4>
              <div className="space-y-2">
                {pedido.historial.map((h) => (
                  <div key={h.id} className="flex items-start gap-2 text-sm">
                    <div className="w-2 h-2 rounded-full bg-gray-400 mt-1.5 flex-shrink-0" />
                    <div>
                      <p className="text-gray-700">
                        {h.estado_anterior ? `${h.estado_anterior} → ` : ''}
                        <span className="font-medium">{h.estado_nuevo}</span>
                      </p>
                      <p className="text-xs text-gray-400">
                        {new Date(h.timestamp).toLocaleString('es-AR')}
                        {h.observacion && ` — ${h.observacion}`}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </Modal>
  );
}
