export const API_PREFIX = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1';

export const ROLES = {
  ADMIN: 'ADMIN' as const,
  STOCK: 'STOCK' as const,
  PEDIDOS: 'PEDIDOS' as const,
  CLIENT: 'CLIENT' as const,
} as const;

export const ESTADOS_PEDIDO = {
  PENDIENTE: 'PENDIENTE',
  CONFIRMADO: 'CONFIRMADO',
  PREPARACION: 'PREPARACION',
  ENVIADO: 'ENVIADO',
  ENTREGADO: 'ENTREGADO',
  CANCELADO: 'CANCELADO',
  RECHAZADO: 'RECHAZADO',
} as const;

export const STORAGE_KEYS = {
  AUTH: 'auth-store',
  CART: 'cart-store',
} as const;
