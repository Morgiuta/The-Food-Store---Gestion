import { ShoppingCart, Trash2 } from 'lucide-react';
import { Button } from '@/shared/ui/button';
import { CartItemComponent } from '@/features/carrito/components/cart-item';
import { CartSummary } from '@/features/carrito/components/cart-summary';
import { useCart } from '@/features/carrito/hooks/use-cart';
import { useNavigate } from 'react-router-dom';

export default function ShoppingCartPage() {
  const navigate = useNavigate();
  const { items, removeItem, updateQuantity, clearCart, totalItems, totalPrice } = useCart();

  const handleUpdateQuantity = (
    productoId: number,
    cantidad: number,
    personalizacion?: { ingredientesExcluidos: number[] },
  ) => {
    updateQuantity(productoId, cantidad, personalizacion);
  };

  const handleRemove = (
    productoId: number,
    personalizacion?: { ingredientesExcluidos: number[] },
  ) => {
    removeItem(productoId, personalizacion);
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Carrito de Compras</h1>
          <p className="text-gray-600 mt-1">
            {totalItems} {totalItems === 1 ? 'producto' : 'productos'} en tu carrito
          </p>
        </div>

        {items.length > 0 && (
          <Button
            variant="outline"
            onClick={clearCart}
            className="text-red-600 hover:text-red-700 hover:bg-red-50"
          >
            <Trash2 className="w-4 h-4 mr-2" />
            Vaciar Carrito
          </Button>
        )}
      </div>

      {items.length === 0 ? (
        <div className="text-center py-16 bg-gray-50 rounded-lg">
          <ShoppingCart className="w-16 h-16 mx-auto text-gray-300 mb-4" />
          <h2 className="text-xl font-medium text-gray-900 mb-2">
            Tu carrito está vacío
          </h2>
          <p className="text-gray-500 mb-6">
            ¿Qué esperas para agregar algunos productos?
          </p>
          <Button onClick={() => navigate('/productos')}>
            Ver Catálogo
          </Button>
        </div>
      ) : (
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Lista de items */}
          <div className="flex-1 space-y-4">
            {items.map((item, index) => (
              <CartItemComponent
                key={`${item.producto.id}-${JSON.stringify(item.personalizacion)}-${index}`}
                item={item}
                onUpdateQuantity={(cantidad) =>
                  handleUpdateQuantity(
                    item.producto.id,
                    cantidad,
                    item.personalizacion ?? undefined,
                  )
                }
                onRemove={() =>
                  handleRemove(item.producto.id, item.personalizacion ?? undefined)
                }
              />
            ))}
          </div>

          {/* Resumen */}
          <div className="lg:w-80">
            <div className="bg-gray-50 rounded-lg p-6 sticky top-4">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Resumen del Pedido
              </h2>
              <CartSummary totalItems={totalItems} totalPrice={totalPrice} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}