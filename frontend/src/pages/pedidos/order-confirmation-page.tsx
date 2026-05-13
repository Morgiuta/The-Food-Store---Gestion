import { useParams, useNavigate } from 'react-router-dom';
import { usePedidoDetail } from '@/features/pedidos/hooks/useOrders';
import { OrderStatusBadge } from '@/features/pedidos/components/order-status-badge';
import { Button } from '@/shared/ui/button';
import { Spinner } from '@/shared/ui/spinner';

export default function OrderConfirmationPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const pedidoId = id ? parseInt(id) : null;
  const { data: pedido, isLoading, error } = usePedidoDetail(pedidoId);

  if (isLoading) {
    return (
      <div className="flex justify-center py-16">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error || !pedido) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Pedido no encontrado</h1>
        <p className="text-gray-500 mb-6">El pedido que buscás no existe o no tenés acceso.</p>
        <Button onClick={() => navigate('/mis-pedidos')}>Mis Pedidos</Button>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h1 className="text-2xl font-bold text-gray-900">¡Pedido confirmado!</h1>
        <p className="text-gray-500 mt-2">Tu pedido fue creado con éxito.</p>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <p className="text-sm text-gray-500">Pedido #{pedido.id}</p>
            <p className="text-xs text-gray-400">
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

        <div className="border-t border-gray-200 pt-4">
          <h3 className="font-medium text-gray-900 mb-2">Resumen</h3>
          {pedido.detalles.map((det) => (
            <div key={det.id} className="flex justify-between text-sm py-1">
              <span className="text-gray-600">
                {det.producto_nombre || `Producto #${det.producto_id}`} × {det.cantidad}
              </span>
              <span className="text-gray-900 font-medium">
                ${Number(det.subtotal).toLocaleString('es-AR', { minimumFractionDigits: 2 })}
              </span>
            </div>
          ))}
        </div>

        <div className="border-t border-gray-200 mt-4 pt-4 space-y-1">
          <div className="flex justify-between text-sm text-gray-600">
            <span>Envío</span>
            <span>${Number(pedido.costo_envio).toLocaleString('es-AR', { minimumFractionDigits: 2 })}</span>
          </div>
          <div className="flex justify-between text-lg font-bold text-gray-900">
            <span>Total</span>
            <span>${Number(pedido.total).toLocaleString('es-AR', { minimumFractionDigits: 2 })}</span>
          </div>
        </div>
      </div>

      <div className="flex justify-center gap-4">
        <Button variant="outline" onClick={() => navigate('/mis-pedidos')}>
          Ver mis pedidos
        </Button>
        <Button onClick={() => navigate('/productos')}>
          Seguir comprando
        </Button>
      </div>
    </div>
  );
}
