import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { CartItem, Product } from '@/shared/types';

interface CartState {
  items: CartItem[];
  addItem: (producto: Product, cantidad?: number, personalizacion?: string) => void;
  removeItem: (productoId: number) => void;
  updateQuantity: (productoId: number, cantidad: number) => void;
  clearCart: () => void;
  getTotalPrice: () => number;
  totalItems: () => number;
  totalPrice: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (producto, cantidad = 1, personalizacion) =>
        set((state) => {
          const existing = state.items.find((item) => item.producto.id === producto.id);
          if (existing) {
            return {
              items: state.items.map((item) =>
                item.producto.id === producto.id
                  ? { ...item, cantidad: item.cantidad + cantidad }
                  : item,
              ),
            };
          }
          return { items: [...state.items, { producto, cantidad, personalizacion }] };
        }),

      removeItem: (productoId) =>
        set((state) => ({
          items: state.items.filter((item) => item.producto.id !== productoId),
        })),

      updateQuantity: (productoId, cantidad) =>
        set((state) => {
          if (cantidad <= 0) {
            return { items: state.items.filter((item) => item.producto.id !== productoId) };
          }
          return {
            items: state.items.map((item) =>
              item.producto.id === productoId ? { ...item, cantidad } : item,
            ),
          };
        }),

      clearCart: () => set({ items: [] }),

      getTotalPrice: () =>
        get().items.reduce((sum, item) => sum + item.producto.precio * item.cantidad, 0),

      totalItems: () => get().items.reduce((sum, item) => sum + item.cantidad, 0),

      totalPrice: () =>
        get().items.reduce((sum, item) => sum + item.producto.precio * item.cantidad, 0),
    }),
    {
      name: 'cart-store',
    },
  ),
);
