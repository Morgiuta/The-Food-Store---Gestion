import type { CartItem } from '@/shared/types';

interface OrderSummaryProps {
  items: CartItem[];
  subtotal: number;
  costoEnvio: number;
  total: number;
}

export function OrderSummary({ items, subtotal, costoEnvio, total }: OrderSummaryProps) {
  return (
    <div className="bg-gray-50 rounded-lg p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Resumen del Pedido</h2>

      {/* Lista de items */}
      <div className="space-y-3 mb-6">
        {items.map((item) => {
          const subtotalItem = item.producto.precio * item.cantidad;
          const personalization = item.personalizacion?.ingredientesExcluidos;

          return (
            <div key={`${item.producto.id}-${JSON.stringify(personalization)}`} className="flex justify-between items-start">
              <div className="flex-1">
                <p className="font-medium text-gray-900">{item.producto.nombre}</p>
                <p className="text-sm text-gray-500">
                  ${item.producto.precio.toFixed(2)} x {item.cantidad}
                </p>
                {personalization && personalization.length > 0 && (
                  <p className="text-xs text-gray-400 mt-1">
                    Sin: {personalization.map((id) => {
                      const ing = item.producto.ingredientes?.find((i) => i.id === id);
                      return ing?.nombre;
                    }).filter(Boolean).join(', ')}
                  </p>
                )}
              </div>
              <p className="font-medium text-gray-900">${subtotalItem.toFixed(2)}</p>
            </div>
          );
        })}
      </div>

      {/* Totales */}
      <div className="border-t pt-4 space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">Subtotal</span>
          <span className="text-gray-900">${subtotal.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">Costo de envío</span>
          <span className="text-gray-900">${costoEnvio.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-lg font-bold pt-2 border-t">
          <span className="text-gray-900">Total</span>
          <span className="text-amber-600">${total.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
}