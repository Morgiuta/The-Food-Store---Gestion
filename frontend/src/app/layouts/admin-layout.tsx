import { Link, Outlet, useLocation } from 'react-router-dom';

const sidebarLinks = [
  { to: '/admin/dashboard', label: 'Dashboard' },
  { to: '/admin/usuarios', label: 'Usuarios' },
  { to: '/admin/productos', label: 'Productos' },
  { to: '/admin/categorias', label: 'Categorías' },
  { to: '/admin/pedidos', label: 'Pedidos' },
  { to: '/admin/ingredientes', label: 'Ingredientes' },
];

export function AdminLayout() {
  const location = useLocation();

  return (
    <div className="min-h-screen flex">
      <aside className="w-64 bg-gray-900 text-white flex flex-col">
        <div className="p-4 border-b border-gray-700">
          <Link to="/admin" className="text-lg font-bold text-amber-400">
            Panel Admin
          </Link>
        </div>
        <nav className="flex-1 p-2 space-y-1">
          {sidebarLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              className={`block px-3 py-2 rounded-md text-sm transition-colors ${
                location.pathname === link.to
                  ? 'bg-gray-700 text-amber-400'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              }`}
            >
              {link.label}
            </Link>
          ))}
        </nav>
        <div className="p-4 border-t border-gray-700">
          <Link to="/" className="text-sm text-gray-400 hover:text-white transition-colors">
            &larr; Volver a la tienda
          </Link>
        </div>
      </aside>

      <main className="flex-1 bg-gray-50 overflow-auto">
        <Outlet />
      </main>
    </div>
  );
}
