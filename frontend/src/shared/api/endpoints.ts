const AUTH = '/auth';
const USUARIOS = '/usuarios';
const PRODUCTOS = '/productos';
const CATEGORIAS = '/categorias';
const INGREDIENTES = '/ingredientes';
const PEDIDOS = '/pedidos';
const PAGOS = '/pagos';
const ADMIN = '/admin';
const DIRECCIONES = '/direcciones';

const PERFIL = '/perfil';

export const ENDPOINTS = {
  AUTH: {
    LOGIN: `${AUTH}/login`,
    REGISTER: `${AUTH}/register`,
    ME: `${AUTH}/me`,
    REFRESH: `${AUTH}/refresh`,
    LOGOUT: `${AUTH}/logout`,
  },
  USUARIOS: {
    BASE: USUARIOS,
    BY_ID: (id: number) => `${USUARIOS}/${id}`,
  },
  PRODUCTOS: {
    BASE: PRODUCTOS,
    ADMIN: `${PRODUCTOS}/admin`,
    BY_ID: (id: number) => `${PRODUCTOS}/${id}`,
  },
  CATEGORIAS: {
    BASE: CATEGORIAS,
    BY_ID: (id: number) => `${CATEGORIAS}/${id}`,
  },
  INGREDIENTES: {
    BASE: INGREDIENTES,
    BY_ID: (id: number) => `${INGREDIENTES}/${id}`,
  },
  PEDIDOS: {
    BASE: PEDIDOS,
    BY_ID: (id: number) => `${PEDIDOS}/${id}`,
    HISTORY: (id: number) => `${PEDIDOS}/${id}/historial`,
    VALIDAR: `${PEDIDOS}/validar`,
    CALCULAR_TOTAL: `${PEDIDOS}/calcular-total`,
    CHANGE_STATUS: (id: number) => `${PEDIDOS}/${id}/estado`,
    CANCEL: (id: number) => `${PEDIDOS}/${id}/cancelar`,
    ADMIN_ALL: `${PEDIDOS}/admin/all`,
  },
  PAGOS: {
    CREATE: `${PAGOS}/crear`,
    BY_PEDIDO: (pedidoId: number) => `${PAGOS}/${pedidoId}`,
    WEBHOOK: `${PAGOS}/webhook`,
  },
  ADMIN: {
    DASHBOARD: `${ADMIN}/dashboard`,
    METRICS: `${ADMIN}/metricas`,
    USUARIOS: `${ADMIN}/usuarios`,
    USUARIO_BY_ID: (id: number) => `${ADMIN}/usuarios/${id}`,
    USUARIO_ESTADO: (id: number) => `${ADMIN}/usuarios/${id}/estado`,
    PAGOS: `${ADMIN}/pagos`,
    PAGO_BY_ID: (id: number) => `${ADMIN}/pagos/${id}`,
    REEMBOLSAR: (id: number) => `${ADMIN}/pagos/${id}/reembolsar`,
    STATS: `${ADMIN}/stats`,
    STATS_REVENUE: `${ADMIN}/stats/revenue`,
    STATS_ORDERS: `${ADMIN}/stats/orders`,
    STATS_PRODUCTS: `${ADMIN}/stats/products`,
    AUDIT: `${ADMIN}/audit`,
    CONFIG: `${ADMIN}/config`,
    FORMAS_PAGO: `${ADMIN}/formas-pago`,
    FORMA_PAGO_BY_ID: (id: number) => `${ADMIN}/formas-pago/${id}`,
  },
  PERFIL: {
    BASE: PERFIL,
    PASSWORD: `${PERFIL}/password`,
  },
  DIRECCIONES: {
    BASE: DIRECCIONES,
    BY_ID: (id: number) => `${DIRECCIONES}/${id}`,
    SET_DEFAULT: (id: number) => `${DIRECCIONES}/${id}/predeterminada`,
  },
} as const;
