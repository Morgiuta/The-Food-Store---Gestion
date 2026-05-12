import { Trash2 } from 'lucide-react';
import { Button } from '@/shared/ui/button';
import { QuantityControl } from './quantity-control';
import type { CartItem } from '@/shared/types';

interface CartItemProps {
  item: CartItem;
  onUpdateQuantity: (cantidad: number) => void;
  onRemove: () => void;
}

export function CartItemComponent({ item, onUpdateQuantity, onRemove }: CartItemProps) {
  const { producto, cantidad, personalizacion } = item;
  const subtotal = producto.precio * cantidad;

  // Obtener nombres de ingredientes excluidos
  const excludedIngredients = personalizacion?.ingredientesExcluidos ?? [];

  return (
    <div className="flex gap-4 p-4 border rounded-lg bg-white">
      {/* Imagen del producto */}
      <div className="w-20 h-20 flex-shrink-0 bg-gray-100 rounded-md overflow-hidden">
        {producto.imagen_url ? (
          <img
            src={producto.imagen_url}
            alt={producto.nombre}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            Sin imagen
          </div>
        )}
      </div>

      {/* Información del producto */}
      <div className="flex-1 min-w-0">
        <h3 className="font-medium text-gray-900 truncate">{producto.nombre}</h3>
        <p className="text-sm text-gray-500">${producto.precio.toFixed(2)} c/u</p>

        {/* Ingredientes excluidos */}
        {excludedIngredients.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1">
            {excludedIngredients.map((id) => {
              const ingrediente = producto.ingredientes?.find((i) => i.id === id);
              return ingrediente ? (
                <span
                  key={id}
                  className="inline-flex items-center px-2 py-0.5 rounded text-xs bg-red-50 text-red-700"
                >
                  Sin {ingrediente.nombre}
                </span>
              ) : null;
            })}
          </div>
        )}
      </div>

      {/* Controles */}
      <div className="flex flex-col items-end justify-between">
        <div className="text-right">
          <p className="font-medium text-gray-900">${subtotal.toFixed(2)}</p>
        </div>

        <div className="flex items-center gap-3">
          <QuantityControl
            cantidad={cantidad}
            onChange={onUpdateQuantity}
            min={1}
            max={producto.stock_cantidad || 99}
          />

          <Button
            variant="ghost"
            size="icon"
            onClick={onRemove}
            className="text-red-600 hover:text-red-700 hover:bg-red-50"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}