import { useState } from 'react';
import {
  useProductosAdmin,
  useDeleteProducto,
} from '@/features/productos/hooks/use-productos';
import { ProductoModal } from '@/features/productos/components/producto-modal';
import { Button } from '@/shared/ui/button';
import { Spinner } from '@/shared/ui/spinner';
import { Input } from '@/shared/ui/input';
import { useUIStore } from '@/app/store/ui-store';
import type { Product } from '@/shared/types';

export default function ProductosPage() {
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [editingProducto, setEditingProducto] = useState<Product | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const { data, isLoading, isError, error } = useProductosAdmin({
    page,
    per_page: 10,
    search: search || undefined,
  });
  const deleteMutation = useDeleteProducto();
  const addNotification = useUIStore((s) => s.addNotification);

  const productos = data?.items ?? [];
  const totalPages = data?.pages ?? 1;

  const handleDelete = (prod: Product) => {
    if (!window.confirm(`¿Eliminar el producto "${prod.nombre}"?`)) return;
    setDeletingId(prod.id);
    deleteMutation.mutate(prod.id, {
      onSuccess: () => {
        addNotification({ type: 'success', message: `Producto "${prod.nombre}" eliminado.` });
        setDeletingId(null);
      },
      onError: () => {
        addNotification({ type: 'error', message: `Error al eliminar el producto "${prod.nombre}".` });
        setDeletingId(null);
      },
    });
  };

  const handleModalSuccess = () => {
    const msg = editingProducto
      ? `Producto "${editingProducto.nombre}" actualizado.`
      : 'Producto creado correctamente.';
    addNotification({ type: 'success', message: msg });
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Gestión de Productos</h1>
          <p className="text-sm text-gray-500 mt-1">Administrá el catálogo de productos</p>
        </div>
        <Button onClick={() => setShowCreateModal(true)}>
          + Nuevo producto
        </Button>
      </div>

      <div className="max-w-sm">
        <Input
          placeholder="Buscar por nombre..."
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(1); }}
        />
      </div>

      {isLoading && (
        <div className="flex justify-center py-16">
          <Spinner size="lg" />
        </div>
      )}

      {isError && (
        <div className="text-center py-16">
          <p className="text-red-600 mb-2">Error al cargar los productos.</p>
          <p className="text-sm text-gray-500">
            {(error as { message?: string })?.message ?? 'Intentalo de nuevo más tarde.'}
          </p>
        </div>
      )}

      {!isLoading && !isError && productos.length === 0 && (
        <div className="text-center py-16">
          <p className="text-gray-500 text-lg mb-1">
            {search ? 'No hay productos que coincidan con la búsqueda.' : 'No hay productos'}
          </p>
          <p className="text-sm text-gray-400">
            {search ? 'Intentá con otro término.' : 'Creá el primer producto para empezar.'}
          </p>
        </div>
      )}

      {!isLoading && !isError && productos.length > 0 && (
        <>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-50 border-b border-gray-200">
                    <th className="text-left px-4 py-3 font-medium text-gray-600">Nombre</th>
                    <th className="text-left px-4 py-3 font-medium text-gray-600">Precio</th>
                    <th className="text-left px-4 py-3 font-medium text-gray-600">Stock</th>
                    <th className="text-left px-4 py-3 font-medium text-gray-600">Disponible</th>
                    <th className="text-right px-4 py-3 font-medium text-gray-600">Acciones</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {productos.map((prod) => (
                    <tr key={prod.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 font-medium text-gray-800 truncate max-w-[200px]">
                        {prod.nombre}
                      </td>
                      <td className="px-4 py-3 text-gray-700">
                        ${Number(prod.precio).toFixed(2)}
                      </td>
                      <td className="px-4 py-3">
                        <span className={`text-sm font-medium ${
                          prod.stock_cantidad <= 5
                            ? 'text-red-600'
                            : prod.stock_cantidad <= 20
                              ? 'text-amber-600'
                              : 'text-green-600'
                        }`}>
                          {prod.stock_cantidad}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        {prod.disponible ? (
                          <span className="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-full bg-green-100 text-green-700">
                            Sí
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-full bg-red-100 text-red-700">
                            No
                          </span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-right">
                        <div className="flex justify-end gap-1">
                          <button
                            type="button"
                            onClick={() => setEditingProducto(prod)}
                            className="p-1.5 rounded text-gray-400 hover:text-amber-600 hover:bg-amber-50 transition-colors"
                            title="Editar"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                            </svg>
                          </button>
                          <button
                            type="button"
                            onClick={() => handleDelete(prod)}
                            disabled={deletingId === prod.id}
                            className="p-1.5 rounded text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors disabled:opacity-50"
                            title="Eliminar"
                          >
                            {deletingId === prod.id ? (
                              <Spinner size="sm" />
                            ) : (
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            )}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2">
              <button
                type="button"
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1}
                className="px-3 py-1.5 text-sm rounded-md border border-gray-300 text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Anterior
              </button>
              <span className="text-sm text-gray-600">
                Página {page} de {totalPages}
              </span>
              <button
                type="button"
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page >= totalPages}
                className="px-3 py-1.5 text-sm rounded-md border border-gray-300 text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Siguiente
              </button>
            </div>
          )}
        </>
      )}

      {showCreateModal && (
        <ProductoModal
          isOpen={showCreateModal}
          onClose={() => setShowCreateModal(false)}
          onSuccess={handleModalSuccess}
        />
      )}

      {editingProducto && (
        <ProductoModal
          isOpen={!!editingProducto}
          onClose={() => setEditingProducto(null)}
          onSuccess={handleModalSuccess}
          producto={editingProducto}
        />
      )}
    </div>
  );
}
