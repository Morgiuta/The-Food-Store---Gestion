import { useState } from 'react';
import { Link, Outlet, useNavigate } from 'react-router-dom';
import { ChevronDown, ShoppingCart } from 'lucide-react';
import { useAuthStore } from '@/app/store/auth-store';
import { useCartStore } from '@/app/store/cart-store';

type NavItem = { label: string; path: string };

const navItems: Record<string, NavItem[]> = {
  public: [
    { label: 'Catálogo', path: '/productos' },
  ],
  client: [
    { label: 'Catálogo', path: '/productos' },
  ],
  stock: [
    { label: 'Admin', path: '/admin/dashboard' },
  ],
  pedidos: [
    { label: 'Admin', path: '/admin/dashboard' },
  ],
  admin: [
    { label: 'Admin', path: '/admin/dashboard' },
  ],
};

const userMenuItems: NavItem[] = [
  { label: 'Mis pedidos', path: '/mis-pedidos' },
  { label: 'Mis direcciones', path: '/mis-direcciones' },
  { label: 'Mi perfil', path: '/perfil' },
];

function getNavItems(user: { roles?: string[] } | null, isAuthenticated: boolean): NavItem[] {
  const items = !isAuthenticated
    ? navItems.public
    : user?.roles?.includes('ADMIN')
      ? [...navItems.public, ...navItems.admin]
      : user?.roles?.includes('STOCK')
        ? [...navItems.public, ...navItems.stock]
        : user?.roles?.includes('PEDIDOS')
          ? [...navItems.public, ...navItems.pedidos]
          : [...navItems.public, ...navItems.client];

  return Array.from(new Map(items.map((item) => [item.path, item])).values());
}

function CartHeaderLink() {
  const totalItems = useCartStore((state) => state.totalItems());

  return (
    <Link
      to="/carrito"
      className="relative inline-flex h-9 w-9 items-center justify-center rounded-md text-gray-200 transition-colors hover:bg-gray-700 hover:text-amber-400"
      aria-label={`Carrito con ${totalItems} ${totalItems === 1 ? 'producto' : 'productos'}`}
    >
      <ShoppingCart className="h-5 w-5" />
      {totalItems > 0 && (
        <span className="absolute -right-1 -top-1 min-w-[1.25rem] rounded-full bg-amber-500 px-1.5 py-0.5 text-center text-[11px] font-bold leading-none text-gray-900">
          {totalItems > 99 ? '99+' : totalItems}
        </span>
      )}
    </Link>
  );
}

export function MainLayout() {
  const { isAuthenticated, user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  const handleLogout = () => {
    setUserMenuOpen(false);
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
            <CartHeaderLink />
            {isAuthenticated ? (
              <div className="relative">
                <button
                  type="button"
                  onClick={() => setUserMenuOpen((open) => !open)}
                  className="inline-flex items-center gap-1 rounded-md px-2 py-1.5 text-sm text-gray-200 transition-colors hover:bg-gray-700 hover:text-amber-400"
                  aria-expanded={userMenuOpen}
                  aria-haspopup="menu"
                >
                  {user?.nombre}
                  <ChevronDown className={`h-4 w-4 transition-transform ${userMenuOpen ? 'rotate-180' : ''}`} />
                </button>
                {userMenuOpen && (
                  <div
                    role="menu"
                    className="absolute right-0 top-full z-50 mt-2 w-48 overflow-hidden rounded-md border border-gray-200 bg-white py-1 text-gray-800 shadow-lg"
                  >
                    {userMenuItems.map((item) => (
                      <Link
                        key={item.path}
                        to={item.path}
                        role="menuitem"
                        className="block px-4 py-2 text-sm hover:bg-amber-50 hover:text-amber-700"
                        onClick={() => setUserMenuOpen(false)}
                      >
                        {item.label}
                      </Link>
                    ))}
                    <hr className="my-1 border-gray-100" />
                    <button
                      type="button"
                      onClick={handleLogout}
                      role="menuitem"
                      className="block w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50"
                    >
                      Cerrar sesión
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <Link to="/login" className="text-sm hover:text-amber-400 transition-colors">
                Iniciar sesión
              </Link>
            )}
          </div>

          <div className="flex items-center gap-2 md:hidden">
            <CartHeaderLink />
            <button
              className="text-gray-300 hover:text-white"
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
                {userMenuItems.map((item) => (
                  <Link
                    key={item.path}
                    to={item.path}
                    className="block text-sm hover:text-amber-400 transition-colors py-1"
                    onClick={() => setMobileOpen(false)}
                  >
                    {item.label}
                  </Link>
                ))}
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
