import { useState } from 'react';
import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/app/store/auth-store';

const sidebarLinks = [
  { to: '/admin/dashboard', label: 'Dashboard', icon: '📊' },
  { to: '/admin/usuarios', label: 'Usuarios', icon: '👥' },
  { to: '/admin/productos', label: 'Productos', icon: '🍔' },
  { to: '/admin/categorias', label: 'Categorías', icon: '📂' },
  { to: '/admin/ingredientes', label: 'Ingredientes', icon: '🥘' },
  { to: '/admin/pedidos', label: 'Pedidos', icon: '📦' },
  { to: '/admin/pagos', label: 'Pagos', icon: '💳' },
  { to: '/admin/config', label: 'Configuración', icon: '⚙️' },
  { to: '/admin/audit', label: 'Auditoría', icon: '📋' },
];

export function AdminLayout() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const q = searchQuery.trim();
    if (!q) return;
    if (/^\d+$/.test(q)) {
      navigate(`/admin/pedidos?search=${q}`);
    } else {
      navigate(`/admin/productos?search=${encodeURIComponent(q)}`);
    }
    setSearchQuery('');
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex">
      <aside className="w-64 bg-gray-900 text-white flex flex-col shrink-0">
        <div className="p-4 border-b border-gray-700">
          <Link to="/admin" className="text-lg font-bold text-amber-400">
            Panel Admin
          </Link>
        </div>

        <nav className="flex-1 p-2 space-y-1 overflow-y-auto">
          {sidebarLinks.map((link) => {
            const isActive =
              location.pathname === link.to ||
              (link.to === '/admin/dashboard' && location.pathname === '/admin');

            return (
              <Link
                key={link.to}
                to={link.to}
                className={`flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors ${
                  isActive
                    ? 'bg-gray-700 text-amber-400'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`}
              >
                <span className="text-base">{link.icon}</span>
                <span>{link.label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-gray-700 space-y-3">
          {user && (
            <div className="text-sm text-gray-400 px-1">
              <p className="font-medium text-gray-300 truncate">{user.nombre}</p>
              <p className="text-xs truncate">{user.email}</p>
            </div>
          )}

          <div className="flex flex-col gap-2">
            <Link
              to="/"
              className="text-sm text-gray-400 hover:text-white transition-colors px-1"
            >
              &larr; Volver a la tienda
            </Link>
            <button
              onClick={handleLogout}
              className="text-sm text-left text-red-400 hover:text-red-300 transition-colors px-1"
            >
              Cerrar sesión
            </button>
          </div>
        </div>
      </aside>

      <main className="flex-1 bg-gray-50 overflow-auto">
        <div className="bg-white border-b border-gray-200 px-6 py-3">
          <form onSubmit={handleSearch} className="flex gap-2">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Buscar pedido por ID o producto..."
              className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm"
            />
            <button type="submit" className="bg-amber-500 text-white px-4 py-2 rounded-md text-sm hover:bg-amber-600">
              Buscar
            </button>
          </form>
        </div>
        <div className="p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
