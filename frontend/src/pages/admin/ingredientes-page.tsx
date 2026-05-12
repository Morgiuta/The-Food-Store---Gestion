import { useState } from 'react';
import {
  useIngredientes,
  useDeleteIngrediente,
} from '@/features/ingredientes/hooks/use-ingredientes';
import { IngredienteModal } from '@/features/ingredientes/components/ingrediente-modal';
import { Button } from '@/shared/ui/button';
import { Spinner } from '@/shared/ui/spinner';
import { useUIStore } from '@/app/store/ui-store';
import type { Ingrediente } from '@/features/ingredientes/hooks/use-ingredientes';

export default function IngredientesPage() {
  const [soloAlergenos, setSoloAlergenos] = useState(false);
  const { data: ingredientes, isLoading, isError, error } = useIngredientes(
    soloAlergenos ? { es_alergeno: true } : undefined,
  );
  const deleteMutation = useDeleteIngrediente();
  const addNotification = useUIStore((s) => s.addNotification);

  const [editingIngrediente, setEditingIngrediente] =
    useState<Ingrediente | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const handleDelete = (ing: Ingrediente) => {
    if (!window.confirm(`¿Eliminar el ingrediente "${ing.nombre}"?`)) return;
    setDeletingId(ing.id);
    deleteMutation.mutate(ing.id, {
      onSuccess: () => {
        addNotification({
          type: 'success',
          message: `Ingrediente "${ing.nombre}" eliminado.`,
        });
        setDeletingId(null);
      },
      onError: () => {
        addNotification({
          type: 'error',
          message: `Error al eliminar el ingrediente "${ing.nombre}".`,
        });
        setDeletingId(null);
      },
    });
  };

  const handleModalSuccess = () => {
    const msg = editingIngrediente
      ? `Ingrediente "${editingIngrediente.nombre}" actualizado.`
      : 'Ingrediente creado correctamente.';
    addNotification({ type: 'success', message: msg });
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            Gestión de Ingredientes
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Administrá los ingredientes y alérgenos del catálogo
          </p>
        </div>
        <Button onClick={() => setShowCreateModal(true)}>
          + Nuevo ingrediente
        </Button>
      </div>

      <div className="flex items-center gap-2">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={soloAlergenos}
            onChange={(e) => setSoloAlergenos(e.target.checked)}
            className="w-4 h-4 rounded border-gray-300 text-amber-500 focus:ring-amber-400"
          />
          <span className="text-sm text-gray-700 select-none">
            Mostrar solo alérgenos
          </span>
        </label>
      </div>

      {isLoading && (
        <div className="flex justify-center py-16">
          <Spinner size="lg" />
        </div>
      )}

      {isError && (
        <div className="text-center py-16">
          <p className="text-red-600 mb-2">
            Error al cargar los ingredientes.
          </p>
          <p className="text-sm text-gray-500">
            {(error as { message?: string })?.message ??
              'Intentalo de nuevo más tarde.'}
          </p>
        </div>
      )}

      {!isLoading && !isError && (!ingredientes || ingredientes.length === 0) && (
        <div className="text-center py-16">
          <p className="text-gray-500 text-lg mb-1">
            {soloAlergenos
              ? 'No hay alérgenos registrados'
              : 'No hay ingredientes'}
          </p>
          <p className="text-sm text-gray-400">
            {soloAlergenos
              ? 'Ningún ingrediente está marcado como alérgeno.'
              : 'Creá el primer ingrediente para empezar.'}
          </p>
        </div>
      )}

      {!isLoading && !isError && ingredientes && ingredientes.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-200">
                  <th className="text-left px-4 py-3 font-medium text-gray-600">
                    Nombre
                  </th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">
                    Alérgeno
                  </th>
                  <th className="text-right px-4 py-3 font-medium text-gray-600">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {ingredientes.map((ing) => (
                  <tr
                    key={ing.id}
                    className="hover:bg-gray-50 transition-colors"
                  >
                    <td className="px-4 py-3 font-medium text-gray-800">
                      {ing.nombre}
                    </td>
                    <td className="px-4 py-3">
                      {ing.es_alergeno ? (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium rounded-full bg-red-100 text-red-700">
                          <svg
                            className="w-3.5 h-3.5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
                            />
                          </svg>
                          Alérgeno
                        </span>
                      ) : (
                        <span className="text-xs text-gray-400">—</span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex justify-end gap-1">
                        <button
                          type="button"
                          onClick={() => setEditingIngrediente(ing)}
                          className="p-1.5 rounded text-gray-400 hover:text-amber-600 hover:bg-amber-50 transition-colors"
                          title="Editar"
                        >
                          <svg
                            className="w-4 h-4"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                            />
                          </svg>
                        </button>
                        <button
                          type="button"
                          onClick={() => handleDelete(ing)}
                          disabled={deletingId === ing.id}
                          className="p-1.5 rounded text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors disabled:opacity-50"
                          title="Eliminar"
                        >
                          {deletingId === ing.id ? (
                            <Spinner size="sm" />
                          ) : (
                            <svg
                              className="w-4 h-4"
                              fill="none"
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                            >
                              <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                              />
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
      )}

      {showCreateModal && (
        <IngredienteModal
          isOpen={showCreateModal}
          onClose={() => setShowCreateModal(false)}
          onSuccess={handleModalSuccess}
        />
      )}

      {editingIngrediente && (
        <IngredienteModal
          isOpen={!!editingIngrediente}
          onClose={() => setEditingIngrediente(null)}
          onSuccess={handleModalSuccess}
          ingrediente={editingIngrediente}
        />
      )}
    </div>
  );
}
