import { Navigate } from 'react-router-dom';
import { useAuthStore } from '@/app/store/auth-store';
import type { Rol } from '@/shared/types';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

interface RoleProtectedRouteProps {
  children: React.ReactNode;
  requiredRole: Rol;
}

export function RoleProtectedRoute({ children, requiredRole }: RoleProtectedRouteProps) {
  const { isAuthenticated, user } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (!user?.roles?.includes(requiredRole)) {
    return <Navigate to="/403" replace />;
  }

  return <>{children}</>;
}
