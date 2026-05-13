import { describe, it, expect, beforeEach } from 'vitest';
import { useCartStore } from '@/app/store/cart-store';
import type { Product } from '@/shared/types';

const mockProduct: Product = {
  id: 1,
  nombre: 'Test Product',
  descripcion: 'Test',
  precio: 100,
  stock_cantidad: 10,
  disponible: true,
  categorias: [],
  ingredientes: [
    { id: 1, nombre: 'Ing A', es_alergeno: false, descripcion: '' },
    { id: 2, nombre: 'Ing B', es_alergeno: true, descripcion: '' },
  ],
};

const mockProduct2: Product = { ...mockProduct, id: 2, nombre: 'Product 2', precio: 50 };

describe('cartStore', () => {
  beforeEach(() => {
    useCartStore.setState({ items: [] });
    localStorage.clear();
  });

  it('should start with empty cart', () => {
    expect(useCartStore.getState().items).toEqual([]);
  });

  it('should add item to cart', () => {
    useCartStore.getState().addItem(mockProduct);
    const items = useCartStore.getState().items;
    expect(items).toHaveLength(1);
    expect(items[0].producto.id).toBe(1);
    expect(items[0].cantidad).toBe(1);
  });

  it('should increment quantity when adding existing item', () => {
    useCartStore.getState().addItem(mockProduct);
    useCartStore.getState().addItem(mockProduct);
    const items = useCartStore.getState().items;
    expect(items).toHaveLength(1);
    expect(items[0].cantidad).toBe(2);
  });

  it('should add separate items for different products', () => {
    useCartStore.getState().addItem(mockProduct);
    useCartStore.getState().addItem(mockProduct2);
    expect(useCartStore.getState().items).toHaveLength(2);
  });

  it('should remove item from cart', () => {
    useCartStore.getState().addItem(mockProduct);
    useCartStore.getState().removeItem(1, null);
    expect(useCartStore.getState().items).toHaveLength(0);
  });

  it('should update quantity', () => {
    useCartStore.getState().addItem(mockProduct);
    useCartStore.getState().updateQuantity(1, 5, null);
    expect(useCartStore.getState().items[0].cantidad).toBe(5);
  });

  it('should remove item if quantity set to 0', () => {
    useCartStore.getState().addItem(mockProduct);
    useCartStore.getState().updateQuantity(1, 0, null);
    expect(useCartStore.getState().items).toHaveLength(0);
  });

  it('should clear cart', () => {
    useCartStore.getState().addItem(mockProduct);
    useCartStore.getState().addItem(mockProduct2);
    useCartStore.getState().clearCart();
    expect(useCartStore.getState().items).toHaveLength(0);
  });

  it('should calculate total price', () => {
    useCartStore.getState().addItem(mockProduct, 2);
    useCartStore.getState().addItem(mockProduct2, 3);
    expect(useCartStore.getState().totalPrice()).toBe(100 * 2 + 50 * 3);
  });

  it('should count total items', () => {
    useCartStore.getState().addItem(mockProduct, 2);
    useCartStore.getState().addItem(mockProduct2, 3);
    expect(useCartStore.getState().totalItems()).toBe(5);
  });

  it('should check if ingredient can be excluded', () => {
    useCartStore.getState().addItem(mockProduct);
    expect(useCartStore.getState().canExcludeIngredient(1, 1)).toBe(true);
    expect(useCartStore.getState().canExcludeIngredient(1, 999)).toBe(false);
  });
});
