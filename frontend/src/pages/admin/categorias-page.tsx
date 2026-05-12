import { useState } from 'react';
import { useCategorias, useDeleteCategoria } from '@/features/categorias/hooks/use-categorias';
import { CategoriaModal } from '@/features/categorias/components/categoria-modal';
import { Button } from '@/shared/ui/button';
import { Spinner } from '@/shared/ui/spinner';
import { useUIStore } from '@/app/store/ui-store';
import type { Categoria } from '@/features/categorias/hooks/use-categorias';

function ChevronIcon({ expanded }: { expanded: boolean }) {
  return (
    <svg
      className={`w-4 h-4 transition-transform ${expanded ? 'rotate-90' : ''}`}
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
    </svg>
  );
}

function EditIcon() {
  return (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
    </svg>
  );
}

function TrashIcon() {
  return (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
    </svg>
  );
}

interface CategoriaNodeProps {
  categoria: Categoria;
  expanded: Set<number>;
  onToggle: (id: number) => void;
  onEdit: (cat: Categoria) => void;
  onDelete: (cat: Categoria) => void;
  deletingId: number | null;
  depth?: number;
}

function CategoriaNode({ categoria, expanded, onToggle, onEdit, onDelete, deletingId, depth = 0 }: CategoriaNodeProps) {
  const hasChildren = !!categoria.subcategorias?.length;
  const isExpanded = expanded.has(categoria.id);

  return (
    <div>
      <div
        className={`flex items-center gap-2 px-3 py-2.5 hover:bg-gray-50 rounded-md transition-colors group ${depth > 0 ? 'ml-6' : ''}`}
      >
        <button
          type="button"
          onClick={() => onToggle(categoria.id)}
          className={`p-0.5 rounded text-gray-400 hover:text-gray-600 hover:bg-gray-200 transition-colors ${hasChildren ? 'visible' : 'invisible'}`}
          title={isExpanded ? 'Contraer' : 'Expandir'}
        >
          <ChevronIcon expanded={isExpanded} />
        </button>

        <span className="flex-1 text-sm font-medium text-gray-800 truncate">
          {categoria.nombre}
        </span>

        {categoria.descripcion && (
          <span className="hidden sm:inline text-xs text-gray-400 truncate max-w-[200px]">
            {categoria.descripcion}
          </span>
        )}

        <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            type="button"
            onClick={() => onEdit(categoria)}
            className="p-1.5 rounded text-gray-400 hover:text-amber-600 hover:bg-amber-50 transition-colors"
            title="Editar"
          >
            <EditIcon />
          </button>
          <button
            type="button"
            onClick={() => onDelete(categoria)}
            disabled={deletingId === categoria.id}
            className="p-1.5 rounded text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors disabled:opacity-50"
            title="Eliminar"
          >
            {deletingId === categoria.id ? <Spinner size="sm" /> : <TrashIcon />}
          </button>
        </div>
      </div>

      {hasChildren && isExpanded && (
        <div className="border-l-2 border-gray-200 ml-5">
          {categoria.subcategorias!.map((sub) => (
            <CategoriaNode
              key={sub.id}
              categoria={sub}
              expanded={expanded}
              onToggle={onToggle}
              onEdit={onEdit}
              onDelete={onDelete}
              deletingId={deletingId}
              depth={depth + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default function CategoriasPage() {
  const { data: categorias, isLoading, isError, error } = useCategorias();
  const deleteMutation = useDeleteCategoria();
  const addNotification = useUIStore((s) => s.addNotification);

  const [expanded, setExpanded] = useState<Set<number>>(new Set());
  const [editingCategoria, setEditingCategoria] = useState<Categoria | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const handleToggle = (id: number) => {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const handleDelete = (cat: Categoria) => {
    if (!window.confirm(`¿Eliminar la categoría "${cat.nombre}"?`)) return;
    setDeletingId(cat.id);
    deleteMutation.mutate(cat.id, {
      onSuccess: () => {
        addNotification({ type: 'success', message: `Categoría "${cat.nombre}" eliminada.` });
        setDeletingId(null);
      },
      onError: () => {
        addNotification({ type: 'error', message: `Error al eliminar la categoría "${cat.nombre}".` });
        setDeletingId(null);
      },
    });
  };

  const handleModalSuccess = () => {
    const msg = editingCategoria
      ? `Categoría "${editingCategoria.nombre}" actualizada.`
      : 'Categoría creada correctamente.';
    addNotification({ type: 'success', message: msg });
  };

  const openEdit = (cat: Categoria) => {
    setEditingCategoria(cat);
  };

  const closeEdit = () => {
    setEditingCategoria(null);
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Gestión de Categorías</h1>
          <p className="text-sm text-gray-500 mt-1">Administrá las categorías del catálogo</p>
        </div>
        <Button onClick={() => setShowCreateModal(true)}>
          + Nueva categoría
        </Button>
      </div>

      {isLoading && (
        <div className="flex justify-center py-16">
          <Spinner size="lg" />
        </div>
      )}

      {isError && (
        <div className="text-center py-16">
          <p className="text-red-600 mb-2">Error al cargar las categorías.</p>
          <p className="text-sm text-gray-500">
            {(error as { message?: string })?.message ?? 'Intentalo de nuevo más tarde.'}
          </p>
        </div>
      )}

      {!isLoading && !isError && (!categorias || categorias.length === 0) && (
        <div className="text-center py-16">
          <p className="text-gray-500 text-lg mb-1">No hay categorías</p>
          <p className="text-sm text-gray-400">
            Creá la primera categoría para empezar a organizar el catálogo.
          </p>
        </div>
      )}

      {!isLoading && !isError && categorias && categorias.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="p-4">
            {categorias.map((cat) => (
              <CategoriaNode
                key={cat.id}
                categoria={cat}
                expanded={expanded}
                onToggle={handleToggle}
                onEdit={openEdit}
                onDelete={handleDelete}
                deletingId={deletingId}
              />
            ))}
          </div>
        </div>
      )}

      {showCreateModal && (
        <CategoriaModal
          isOpen={showCreateModal}
          onClose={() => setShowCreateModal(false)}
          onSuccess={handleModalSuccess}
          categorias={categorias ?? []}
        />
      )}

      {editingCategoria && (
        <CategoriaModal
          isOpen={!!editingCategoria}
          onClose={closeEdit}
          onSuccess={handleModalSuccess}
          categoria={editingCategoria}
          categorias={categorias ?? []}
        />
      )}
    </div>
  );
}
