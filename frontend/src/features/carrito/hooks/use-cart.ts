import { useCartStore } from '@/app/store/cart-store';
import type { Product } from '@/shared/types';

export function useCart() {
  const items = useCartStore((state) => state.items);
  const addItem = useCartStore((state) => state.addItem);
  const removeItem = useCartStore((state) => state.removeItem);
  const updateQuantity = useCartStore((state) => state.updateQuantity);
  const clearCart = useCartStore((state) => state.clearCart);
  const getTotalPrice = useCartStore((state) => state.getTotalPrice);
  const totalItems = useCartStore((state) => state.totalItems);
  const totalPrice = useCartStore((state) => state.totalPrice);
  const canExcludeIngredient = useCartStore((state) => state.canExcludeIngredient);

  // Helper para agregar con manejo de personalización
  const addItemWithPersonalization = (
    producto: Product,
    cantidad: number = 1,
    ingredientesExcluidos?: number[],
  ) => {
    if (ingredientesExcluidos && ingredientesExcluidos.length > 0) {
      addItem(producto, cantidad, { ingredientesExcluidos });
    } else {
      addItem(producto, cantidad, undefined);
    }
  };

  // Helper para remover considerando personalización
  const removeItemWithPersonalization = (
    productoId: number,
    personalizacion?: { ingredientesExcluidos: number[] },
  ) => {
    removeItem(productoId, personalizacion);
  };

  // Helper para actualizar cantidad considerando personalización
  const updateQuantityWithPersonalization = (
    productoId: number,
    cantidad: number,
    personalizacion?: { ingredientesExcluidos: number[] },
  ) => {
    updateQuantity(productoId, cantidad, personalizacion);
  };

  return {
    items,
    addItem: addItemWithPersonalization,
    removeItem: removeItemWithPersonalization,
    updateQuantity: updateQuantityWithPersonalization,
    clearCart,
    getTotalPrice,
    totalItems,
    totalPrice,
    canExcludeIngredient,
    // También exponer los métodos base del store
    addItemRaw: addItem,
    removeItemRaw: removeItem,
    updateQuantityRaw: updateQuantity,
  };
}