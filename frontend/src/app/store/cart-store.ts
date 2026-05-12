import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { CartItem, Product } from '@/shared/types';

interface CartState {
  items: CartItem[];
  addItem: (
    producto: Product,
    cantidad?: number,
    personalizacion?: { ingredientesExcluidos: number[] },
  ) => void;
  removeItem: (productoId: number, personalizacion?: { ingredientesExcluidos: number[] }) => void;
  updateQuantity: (productoId: number, cantidad: number, personalizacion?: { ingredientesExcluidos: number[] }) => void;
  clearCart: () => void;
  getTotalPrice: () => number;
  totalItems: () => number;
  totalPrice: () => number;
  canExcludeIngredient: (productoId: number, ingredienteId: number) => boolean;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (producto, cantidad = 1, personalizacion) =>
        set((state) => {
          // Buscar item existente con mismo producto Y misma personalización
          const existingIndex = state.items.findIndex(
            (item) =>
              item.producto.id === producto.id &&
              JSON.stringify(item.personalizacion) === JSON.stringify(personalizacion),
          );

          if (existingIndex >= 0) {
            // Actualizar cantidad del item existente
            const newItems = [...state.items];
            newItems[existingIndex] = {
              ...newItems[existingIndex],
              cantidad: newItems[existingIndex].cantidad + cantidad,
            };
            return { items: newItems };
          }

          // Agregar nuevo item
          return {
            items: [...state.items, { producto, cantidad, personalizacion: personalizacion || null }],
          };
        }),

      removeItem: (productoId, personalizacion) =>
        set((state) => ({
          items: state.items.filter(
            (item) =>
              !(
                item.producto.id === productoId &&
                JSON.stringify(item.personalizacion) === JSON.stringify(personalizacion)
              ),
          ),
        })),

      updateQuantity: (productoId, cantidad, personalizacion) =>
        set((state) => {
          if (cantidad <= 0) {
            return {
              items: state.items.filter(
                (item) =>
                  !(
                    item.producto.id === productoId &&
                    JSON.stringify(item.personalizacion) === JSON.stringify(personalizacion)
                  ),
              ),
            };
          }

          return {
            items: state.items.map((item) =>
              item.producto.id === productoId &&
              JSON.stringify(item.personalizacion) === JSON.stringify(personalizacion)
                ? { ...item, cantidad }
                : item,
            ),
          };
        }),

      clearCart: () => set({ items: [] }),

      getTotalPrice: () =>
        get().items.reduce((sum, item) => sum + item.producto.precio * item.cantidad, 0),

      totalItems: () => get().items.reduce((sum, item) => sum + item.cantidad, 0),

      totalPrice: () =>
        get().items.reduce((sum, item) => sum + item.producto.precio * item.cantidad, 0),

      canExcludeIngredient: (productoId, ingredienteId) => {
        const producto = get().items.find((item) => item.producto.id === productoId)?.producto;
        if (!producto) return false;
        // Verificar que el ingrediente existe en el producto
        return producto.ingredientes?.some((ing) => ing.id === ingredienteId) ?? false;
      },
    }),
    {
      name: 'cart-store',
    },
  ),
);