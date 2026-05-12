import { useState } from 'react';
import { Link, Outlet, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/app/store/auth-store';

type NavItem = { label: string; path: string };

const navItems: Record<string, NavItem[]> = {
  public: [
    { label: 'Catálogo', path: '/productos' },
  ],
  client: [
    { label: 'Catálogo', path: '/productos' },
    { label: 'Mi Carrito', path: '/carrito' },
    { label: 'Mis Pedidos', path: '/mis-pedidos' },
    { label: 'Mis Direcciones', path: '/mis-direcciones' },
    { label: 'Mi Perfil', path: '/perfil' },
  ],
  stock: [
    { label: 'Dashboard', path: '/admin/dashboard' },
    { label: 'Productos', path: '/admin/productos' },
    { label: 'Categorías', path: '/admin/categorias' },
    { label: 'Ingredientes', path: '/admin/ingredientes' },
  ],
  pedidos: [
    { label: 'Dashboard', path: '/admin/dashboard' },
    { label: 'Pedidos', path: '/admin/pedidos' },
  ],
  admin: [
    { label: 'Dashboard', path: '/admin/dashboard' },
    { label: 'Usuarios', path: '/admin/usuarios' },
    { label: 'Productos', path: '/admin/productos' },
    { label: 'Categorías', path: '/admin/categorias' },
    { label: 'Ingredientes', path: '/admin/ingredientes' },
    { label: 'Pedidos', path: '/admin/pedidos' },
  ],
};

function getNavItems(user: { roles?: string[] } | null, isAuthenticated: boolean): NavItem[] {
  if (!isAuthenticated) return navItems.public;
  if (user?.roles?.includes('ADMIN')) return [...navItems.public, ...navItems.admin];
  if (user?.roles?.includes('STOCK')) return [...navItems.public, ...navItems.stock];
  if (user?.roles?.includes('PEDIDOS')) return [...navItems.public, ...navItems.pedidos];
  return [...navItems.public, ...navItems.client];
}

export function MainLayout() {
  const { isAuthenticated, user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const items = getNavItems(user, isAuthenticated);

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-gray-800 text-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/" className="text-xl font-bold text-amber-400 shrink-0">
            The Food Store
          </Link>

          <nav className="hidden md:flex items-center gap-6">
            {items.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className="hover:text-amber-400 transition-colors text-sm"
              >
                {item.label}
              </Link>
            ))}
          </nav>

          <div className="hidden md:flex items-center gap-4">
            {isAuthenticated ? (
              <>
                <span className="text-sm text-gray-300">{user?.nombre}</span>
                <button
                  onClick={handleLogout}
                  className="text-sm text-red-300 hover:text-red-100 transition-colors"
                >
                  Cerrar sesión
                </button>
              </>
            ) : (
              <Link to="/login" className="text-sm hover:text-amber-400 transition-colors">
                Iniciar sesión
              </Link>
            )}
          </div>

          <button
            className="md:hidden text-gray-300 hover:text-white"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Menú"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {mobileOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {mobileOpen && (
          <div className="md:hidden border-t border-gray-700 px-4 py-3 space-y-2">
            {items.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className="block text-sm hover:text-amber-400 transition-colors py-1"
                onClick={() => setMobileOpen(false)}
              >
                {item.label}
              </Link>
            ))}
            <hr className="border-gray-700 my-2" />
            {isAuthenticated ? (
              <>
                <span className="block text-sm text-gray-300">{user?.nombre}</span>
                <button
                  onClick={() => { handleLogout(); setMobileOpen(false); }}
                  className="text-sm text-red-300 hover:text-red-100 transition-colors py-1"
                >
                  Cerrar sesión
                </button>
              </>
            ) : (
              <Link
                to="/login"
                className="block text-sm hover:text-amber-400 transition-colors py-1"
                onClick={() => setMobileOpen(false)}
              >
                Iniciar sesión
              </Link>
            )}
          </div>
        )}
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
