import { lazy, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { MainLayout } from '@/app/layouts/main-layout';
import { AdminLayout } from '@/app/layouts/admin-layout';
import { ProtectedRoute, RoleProtectedRoute } from '@/features/auth/components/protected-route';
import { Spinner } from '@/shared/ui/spinner';

const LoginPage = lazy(() => import('@/pages/auth/login-page'));
const RegisterPage = lazy(() => import('@/pages/auth/register-page'));
const ProfilePage = lazy(() => import('@/pages/auth/profile-page'));
const AdminUsersPage = lazy(() => import('@/pages/admin/users-page'));
const AdminProductosPage = lazy(() => import('@/pages/admin/productos-page'));
const CategoriasPage = lazy(() => import('@/pages/admin/categorias-page'));
const IngredientesPage = lazy(() => import('@/pages/admin/ingredientes-page'));
const AdminOrdersPage = lazy(() => import('@/pages/admin/orders-page'));
const CatalogPage = lazy(() => import('@/pages/productos/catalog-page'));
const ShoppingCartPage = lazy(() => import('@/pages/carrito/shopping-cart-page'));
const CheckoutPage = lazy(() => import('@/pages/checkout/checkout-page'));
const DireccionesPage = lazy(() => import('@/features/direcciones/pages/direcciones-page'));
const OrderListPage = lazy(() => import('@/pages/pedidos/order-list-page'));
const OrderConfirmationPage = lazy(() => import('@/pages/pedidos/order-confirmation-page'));
const NotFoundPage = lazy(() => import('@/pages/dashboard/not-found-page'));
const ForbiddenPage = lazy(() => import('@/pages/dashboard/forbidden-page'));
const UnauthorizedPage = lazy(() => import('@/pages/dashboard/unauthorized-page'));

function SuspenseWrapper({ children }: { children: React.ReactNode }) {
  return (
    <Suspense fallback={<div className="flex items-center justify-center min-h-screen"><Spinner size="lg" /></div>}>
      {children}
    </Suspense>
  );
}

export function AppRouter() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<Navigate to="/productos" replace />} />
        <Route path="/login" element={<SuspenseWrapper><LoginPage /></SuspenseWrapper>} />
        <Route path="/register" element={<SuspenseWrapper><RegisterPage /></SuspenseWrapper>} />
        <Route path="/productos" element={<SuspenseWrapper><CatalogPage /></SuspenseWrapper>} />
        <Route path="/carrito" element={<SuspenseWrapper><ShoppingCartPage /></SuspenseWrapper>} />
        <Route path="/checkout" element={
          <ProtectedRoute>
            <SuspenseWrapper><CheckoutPage /></SuspenseWrapper>
          </ProtectedRoute>
        } />
        <Route
          path="/mis-pedidos"
          element={
            <ProtectedRoute>
              <SuspenseWrapper><OrderListPage /></SuspenseWrapper>
            </ProtectedRoute>
          }
        />
        <Route
          path="/pedidos/confirmacion/:id"
          element={
            <ProtectedRoute>
              <SuspenseWrapper><OrderConfirmationPage /></SuspenseWrapper>
            </ProtectedRoute>
          }
        />
        <Route
          path="/perfil"
          element={
            <ProtectedRoute>
              <SuspenseWrapper><ProfilePage /></SuspenseWrapper>
            </ProtectedRoute>
          }
        />
        <Route
          path="/mis-direcciones"
          element={
            <ProtectedRoute>
              <SuspenseWrapper><DireccionesPage /></SuspenseWrapper>
            </ProtectedRoute>
          }
        />
        <Route path="/401" element={<SuspenseWrapper><UnauthorizedPage /></SuspenseWrapper>} />
        <Route path="/403" element={<SuspenseWrapper><ForbiddenPage /></SuspenseWrapper>} />
        <Route path="*" element={<SuspenseWrapper><NotFoundPage /></SuspenseWrapper>} />
      </Route>

      <Route
        path="/admin"
        element={
          <RoleProtectedRoute requiredRole="ADMIN">
            <AdminLayout />
          </RoleProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/admin/dashboard" replace />} />
        <Route path="dashboard" element={<div className="p-8 text-gray-500">Panel de administración — próximamente</div>} />
        <Route path="usuarios" element={<SuspenseWrapper><AdminUsersPage /></SuspenseWrapper>} />
        <Route path="productos" element={<SuspenseWrapper><AdminProductosPage /></SuspenseWrapper>} />
        <Route path="categorias" element={<SuspenseWrapper><CategoriasPage /></SuspenseWrapper>} />
        <Route path="pedidos" element={<SuspenseWrapper><AdminOrdersPage /></SuspenseWrapper>} />
        <Route path="ingredientes" element={<SuspenseWrapper><IngredientesPage /></SuspenseWrapper>} />
      </Route>
    </Routes>
  );
}
