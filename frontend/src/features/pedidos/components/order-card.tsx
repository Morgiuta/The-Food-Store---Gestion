import { Card, CardContent, CardFooter } from '@/shared/ui/card';
import { Button } from '@/shared/ui/button';
import { OrderStatusBadge } from './order-status-badge';
import type { Order } from '@/shared/types';

interface Props {
  order: Order;
  onViewDetail: (id: number) => void;
}

export function OrderCard({ order, onViewDetail }: Props) {
  const fecha = new Date(order.creado_en).toLocaleDateString('es-AR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-medium text-gray-500">
            Pedido #{order.id}
          </h3>
          <OrderStatusBadge estado={order.estado} />
        </div>
        <div className="text-sm text-gray-600 mb-1">{fecha}</div>
        <div className="text-lg font-semibold text-gray-900">
          ${Number(order.total).toLocaleString('es-AR', { minimumFractionDigits: 2 })}
        </div>
        {order.costo_envio > 0 && (
          <div className="text-xs text-gray-400">
            Incluye envío: ${Number(order.costo_envio).toLocaleString('es-AR', { minimumFractionDigits: 2 })}
          </div>
        )}
      </CardContent>
      <CardFooter className="px-4 pb-4 pt-0">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onViewDetail(order.id)}
        >
          Ver detalle
        </Button>
      </CardFooter>
    </Card>
  );
}
