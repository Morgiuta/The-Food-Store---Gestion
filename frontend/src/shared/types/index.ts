export type Rol = 'ADMIN' | 'STOCK' | 'PEDIDOS' | 'CLIENT';

export interface User {
  id: number;
  nombre: string;
  email: string;
  telefono: string;
  roles: Rol[];
  activo: boolean;
  creado_en: string;
  actualizado_en: string;
}

export interface Categoria {
  id: number;
  nombre: string;
  descripcion: string;
  padre_id: number | null;
  hijos?: Categoria[];
}

export interface Ingrediente {
  id: number;
  nombre: string;
  es_alergeno: boolean;
  descripcion: string;
}

export interface Product {
  id: number;
  nombre: string;
  descripcion: string;
  precio: number;
  stock_cantidad: number;
  disponible: boolean;
  categorias: Categoria[];
  ingredientes: Ingrediente[];
  imagen_url?: string;
}

export interface CartItem {
  producto: Product;
  cantidad: number;
  personalizacion?: {
    ingredientesExcluidos: number[];
  };
}

export interface Address {
  id: number;
  calle: string;
  numero: string;
  ciudad: string;
  provincia: string;
  codigo_postal: string;
  referencia?: string;
}

export type EstadoPedido =
  | 'PENDIENTE'
  | 'CONFIRMADO'
  | 'PREPARACION'
  | 'ENVIADO'
  | 'ENTREGADO'
  | 'CANCELADO'
  | 'RECHAZADO';

export interface Order {
  id: number;
  usuario_id: number;
  estado: EstadoPedido;
  total: number;
  direccion: Address;
  detalles: OrderDetail[];
  creado_en: string;
  actualizado_en: string;
}

export interface OrderDetail {
  id: number;
  producto_id: number;
  producto_nombre: string;
  cantidad: number;
  precio_unitario: number;
  subtotal: number;
  personalizacion?: string;
}

export interface OrderHistory {
  id: number;
  pedido_id: number;
  estado_anterior: EstadoPedido;
  estado_nuevo: EstadoPedido;
  cambiado_por: string;
  creado_en: string;
}

export interface Payment {
  id: number;
  pedido_id: number;
  mp_payment_id: string;
  status: string;
  status_detail: string;
  creado_en: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}
