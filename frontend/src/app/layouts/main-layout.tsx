import { Link, Outlet, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/app/store/auth-store';

export function MainLayout() {
  const { isAuthenticated, user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-gray-800 text-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/" className="text-xl font-bold text-amber-400">
            The Food Store
          </Link>

          <nav className="flex items-center gap-6">
            <Link to="/productos" className="hover:text-amber-400 transition-colors">
              Productos
            </Link>
            <Link to="/carrito" className="hover:text-amber-400 transition-colors">
              Carrito
            </Link>
            {isAuthenticated ? (
              <>
                <Link to="/mis-pedidos" className="hover:text-amber-400 transition-colors">
                  Mis Pedidos
                </Link>
                {user?.roles?.includes('ADMIN') && (
                  <Link to="/admin" className="hover:text-amber-400 transition-colors">
                    Admin
                  </Link>
                )}
                <span className="text-sm text-gray-300">{user?.nombre}</span>
                <button onClick={handleLogout} className="text-sm text-red-300 hover:text-red-100 transition-colors">
                  Cerrar sesión
                </button>
              </>
            ) : (
              <Link to="/login" className="hover:text-amber-400 transition-colors">
                Iniciar sesión
              </Link>
            )}
          </nav>
        </div>
      </header>

      <main className="flex-1">
        <Outlet />
      </main>

      <footer className="bg-gray-100 border-t py-4 text-center text-sm text-gray-500">
        &copy; {new Date().getFullYear()} The Food Store — Todos los derechos reservados
      </footer>
    </div>
  );
}
