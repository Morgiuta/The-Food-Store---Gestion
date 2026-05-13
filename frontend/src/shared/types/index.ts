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
  | 'EN_PREPARACION'
  | 'EN_CAMINO'
  | 'ENTREGADO'
  | 'CANCELADO';

export interface Order {
  id: number;
  usuario_id: number;
  estado: string;
  total: number;
  costo_envio: number;
  creado_en: string;
}

export interface OrderDetail {
  id: number;
  producto_id: number | null;
  producto_nombre: string | null;
  cantidad: number;
  precio_unitario: number;
  subtotal: number;
  personalizacion: number[];
}

export interface OrderHistoryEntry {
  id: number;
  estado_anterior: string | null;
  estado_nuevo: string;
  usuario_id: number | null;
  observacion: string | null;
  timestamp: string;
}

export interface OrderFull extends Order {
  detalles: OrderDetail[];
  historial: OrderHistoryEntry[];
}

export interface CreateOrderPayload {
  items: {
    producto_id: number;
    cantidad: number;
    personalizacion?: number[];
  }[];
  direccion_id?: number;
  forma_pago_id?: number;
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

export interface PagoInfo {
  id: number;
  pedido_id: number;
  monto: number;
  mp_status: string | null;
  external_reference: string | null;
  creado_en: string;
}

export interface PagoDetail extends PagoInfo {
  mp_payment_id: string | null;
  idempotency_key: string | null;
  actualizado_en: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}
