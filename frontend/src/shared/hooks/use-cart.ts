import { useCartStore } from '@/app/store/cart-store';
import type { Product } from '@/shared/types';

export function useCart() {
  const {
    items,
    addItem,
    removeItem,
    updateQuantity,
    clearCart,
    totalItems,
    totalPrice,
    getTotalPrice,
  } = useCartStore();

  const addProduct = (
    producto: Product,
    cantidad = 1,
    personalizacion?: { ingredientesExcluidos: number[] },
  ) => {
    addItem(producto, cantidad, personalizacion);
  };

  const removeProduct = (productoId: number) => {
    removeItem(productoId);
  };

  const changeQuantity = (productoId: number, cantidad: number) => {
    updateQuantity(productoId, cantidad);
  };

  const isEmpty = items.length === 0;

  return {
    items,
    isEmpty,
    addProduct,
    removeProduct,
    changeQuantity,
    clearCart,
    totalItems: totalItems(),
    totalPrice: totalPrice(),
    getTotalPrice,
  };
}
