import { useState } from 'react';
import { useAdminUsuarios, useToggleEstado } from '@/features/usuarios/hooks/use-admin-users';
import { EditUserModal } from '@/features/usuarios/components/edit-user-modal';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { Spinner } from '@/shared/ui/spinner';
import type { User } from '@/shared/types';

const ROLES_FILTER: Array<{ value: string; label: string }> = [
  { value: '', label: 'Todos los roles' },
  { value: 'ADMIN', label: 'ADMIN' },
  { value: 'STOCK', label: 'STOCK' },
  { value: 'PEDIDOS', label: 'PEDIDOS' },
  { value: 'CLIENT', label: 'CLIENT' },
];

export default function AdminUsersPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [rolFilter, setRolFilter] = useState('');
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const limit = 10;

  const { data, isLoading, isError, error } = useAdminUsuarios({
    skip: (page - 1) * limit,
    limit,
    search: search || undefined,
    rol: rolFilter || undefined,
  });

  const toggleEstado = useToggleEstado();

  const usuarios: User[] = data?.items ?? data?.data ?? [];
  const total: number = data?.total ?? 0;
  const totalPages = Math.ceil(total / limit);

  const handleToggleEstado = (user: User) => {
    if (window.confirm(`¿${user.activo ? 'Desactivar' : 'Activar'} al usuario "${user.nombre}"?`)) {
      toggleEstado.mutate(user.id);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-800">Gestión de Usuarios</h1>
        <p className="text-sm text-gray-500 mt-1">Administrá los usuarios del sistema</p>
      </div>

      <div className="flex flex-col sm:flex-row gap-3">
        <div className="flex-1">
          <Input
            placeholder="Buscar por nombre o email..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
          />
        </div>
        <select
          value={rolFilter}
          onChange={(e) => {
            setRolFilter(e.target.value);
            setPage(1);
          }}
          className="px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-400 bg-white"
        >
          {ROLES_FILTER.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      {isLoading && (
        <div className="flex justify-center py-12">
          <Spinner size="lg" />
        </div>
      )}

      {isError && (
        <div className="text-center py-12">
          <p className="text-red-600 mb-2">Error al cargar los usuarios.</p>
          <p className="text-sm text-gray-500">
            {(error as { message?: string })?.message ?? 'Intentalo de nuevo más tarde.'}
          </p>
        </div>
      )}

      {!isLoading && !isError && usuarios.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg mb-1">No se encontraron usuarios</p>
          <p className="text-sm text-gray-400">
            {search || rolFilter ? 'Intentá con otros filtros.' : 'No hay usuarios registrados.'}
          </p>
        </div>
      )}

      {!isLoading && !isError && usuarios.length > 0 && (
        <>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-50 border-b border-gray-200">
                    <th className="text-left px-4 py-3 font-medium text-gray-600">Nombre</th>
                    <th className="text-left px-4 py-3 font-medium text-gray-600">Email</th>
                    <th className="text-left px-4 py-3 font-medium text-gray-600">Roles</th>
                    <th className="text-left px-4 py-3 font-medium text-gray-600">Estado</th>
                    <th className="text-right px-4 py-3 font-medium text-gray-600">Acciones</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {usuarios.map((user) => (
                    <tr key={user.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 font-medium text-gray-800">{user.nombre}</td>
                      <td className="px-4 py-3 text-gray-600">{user.email}</td>
                      <td className="px-4 py-3">
                        <div className="flex flex-wrap gap-1">
                          {user.roles.map((rol) => (
                            <span
                              key={rol}
                              className="inline-block px-2 py-0.5 text-xs font-medium rounded-full bg-amber-100 text-amber-800"
                            >
                              {rol}
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className={`inline-flex items-center gap-1 text-xs font-medium ${
                            user.activo ? 'text-green-700' : 'text-red-700'
                          }`}
                        >
                          <span
                            className={`w-2 h-2 rounded-full ${
                              user.activo ? 'bg-green-500' : 'bg-red-500'
                            }`}
                          />
                          {user.activo ? 'Activo' : 'Desactivado'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <div className="flex justify-end gap-2">
                          <Button
                            variant="ghost"
                            className="text-xs px-2 py-1"
                            onClick={() => setEditingUser(user)}
                          >
                            Editar
                          </Button>
                          <Button
                            variant={user.activo ? 'danger' : 'secondary'}
                            className="text-xs px-2 py-1"
                            isLoading={toggleEstado.isPending}
                            onClick={() => handleToggleEstado(user)}
                          >
                            {user.activo ? 'Desactivar' : 'Activar'}
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {totalPages > 1 && (
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-500">
                Página {page} de {totalPages} ({total} usuarios)
              </p>
              <div className="flex gap-2">
                <Button
                  variant="secondary"
                  disabled={page <= 1}
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                >
                  Anterior
                </Button>
                <Button
                  variant="secondary"
                  disabled={page >= totalPages}
                  onClick={() => setPage((p) => p + 1)}
                >
                  Siguiente
                </Button>
              </div>
            </div>
          )}
        </>
      )}

      {editingUser && (
        <EditUserModal
          user={editingUser}
          isOpen={true}
          onClose={() => setEditingUser(null)}
        />
      )}
    </div>
  );
}
