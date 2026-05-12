import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/shared/ui/dialog';
import { Button } from '@/shared/ui/button';
import type { CartItem } from '@/shared/types';
import type { Direccion } from '@/features/direcciones/hooks/use-direcciones';

interface ReviewOrderModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  items: CartItem[];
  direccion: Direccion | undefined;
  subtotal: number;
  costoEnvio: number;
  total: number;
  isLoading?: boolean;
}

export function ReviewOrderModal({
  isOpen,
  onClose,
  onConfirm,
  items,
  direccion,
  subtotal,
  costoEnvio,
  total,
  isLoading,
}: ReviewOrderModalProps) {
  if (!direccion) return null;

  const fullAddress = [
    direccion.calle,
    direccion.numero,
    direccion.piso && `Piso ${direccion.piso}`,
    direccion.departamento && `Depto ${direccion.departamento}`,
  ]
    .filter(Boolean)
    .join(', ');

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Revisar tu Pedido</DialogTitle>
          <DialogDescription>
            Verifica los detalles antes de confirmar
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          {/* Dirección de entrega */}
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-medium text-gray-900 mb-2">Dirección de entrega</h3>
            <p className="text-sm text-gray-600">
              {fullAddress}, {direccion.ciudad}, {direccion.codigo_postal}
            </p>
            {direccion.referencia && (
              <p className="text-sm text-gray-500 mt-1">Ref: {direccion.referencia}</p>
            )}
          </div>

          {/* Items */}
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-medium text-gray-900 mb-2">Productos</h3>
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {items.map((item) => (
                <div key={`${item.producto.id}-${JSON.stringify(item.personalizacion)}`} className="flex justify-between text-sm">
                  <span className="text-gray-600">
                    {item.producto.nombre} x{item.cantidad}
                  </span>
                  <span className="text-gray-900">
                    ${(item.producto.precio * item.cantidad).toFixed(2)}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Totales */}
          <div className="border-t pt-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Subtotal</span>
              <span className="text-gray-900">${subtotal.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Envío</span>
              <span className="text-gray-900">${costoEnvio.toFixed(2)}</span>
            </div>
            <div className="flex justify-between font-bold text-lg">
              <span className="text-gray-900">Total</span>
              <span className="text-amber-600">${total.toFixed(2)}</span>
            </div>
          </div>
        </div>

        <div className="flex justify-end gap-2 pt-4">
          <Button variant="outline" onClick={onClose}>
            Cancelar
          </Button>
          <Button onClick={onConfirm} disabled={isLoading}>
            {isLoading ? 'Confirmando...' : 'Confirmar Pedido'}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}