const AUTH = '/auth';
const USUARIOS = '/usuarios';
const PRODUCTOS = '/productos';
const CATEGORIAS = '/categorias';
const INGREDIENTES = '/ingredientes';
const PEDIDOS = '/pedidos';
const PAGOS = '/pagos';
const ADMIN = '/admin';

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
  },
  PAGOS: {
    CREATE: `${PAGOS}/create`,
    CALLBACK: `${PAGOS}/callback`,
    WEBHOOK: `${PAGOS}/webhook`,
  },
  ADMIN: {
    DASHBOARD: `${ADMIN}/dashboard`,
    METRICS: `${ADMIN}/metricas`,
    USUARIOS: `${ADMIN}/usuarios`,
    USUARIO_BY_ID: (id: number) => `${ADMIN}/usuarios/${id}`,
    USUARIO_ESTADO: (id: number) => `${ADMIN}/usuarios/${id}/estado`,
  },
  PERFIL: {
    BASE: PERFIL,
    PASSWORD: `${PERFIL}/password`,
  },
} as const;
