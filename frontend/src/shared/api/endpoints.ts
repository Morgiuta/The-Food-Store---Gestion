const AUTH = '/auth';
const USUARIOS = '/usuarios';
const PRODUCTOS = '/productos';
const CATEGORIAS = '/categorias';
const INGREDIENTES = '/ingredientes';
const PEDIDOS = '/pedidos';
const PAGOS = '/pagos';
const ADMIN = '/admin';

export const ENDPOINTS = {
  AUTH: {
    LOGIN: `${AUTH}/login`,
    REGISTER: `${AUTH}/register`,
    ME: `${AUTH}/me`,
    REFRESH: `${AUTH}/refresh`,
  },
  USUARIOS: {
    BASE: USUARIOS,
    BY_ID: (id: number) => `${USUARIOS}/${id}`,
  },
  PRODUCTOS: {
    BASE: PRODUCTOS,
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
  },
  PAGOS: {
    CREATE: `${PAGOS}/create`,
    CALLBACK: `${PAGOS}/callback`,
    WEBHOOK: `${PAGOS}/webhook`,
  },
  ADMIN: {
    DASHBOARD: `${ADMIN}/dashboard`,
    METRICS: `${ADMIN}/metricas`,
  },
} as const;
