import { useState, useEffect } from 'react';
import { Modal } from '@/shared/ui/modal';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { useCreateCategoria, useUpdateCategoria } from '../hooks/use-categorias';
import type { Categoria, CategoriaCreate } from '../hooks/use-categorias';

interface CategoriaModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  categoria?: Categoria | null;
  categorias: Categoria[];
}

type FlatOption = { id: number | null; nombre: string; depth: number };

function flattenTree(list: Categoria[], depth = 0, excludeId?: number): FlatOption[] {
  const result: FlatOption[] = [];
  for (const cat of list) {
    if (cat.id === excludeId) continue;
    result.push({ id: cat.id, nombre: cat.nombre, depth });
    if (cat.subcategorias?.length) {
      result.push(...flattenTree(cat.subcategorias, depth + 1, excludeId));
    }
  }
  return result;
}

export function CategoriaModal({ isOpen, onClose, onSuccess, categoria, categorias }: CategoriaModalProps) {
  const [nombre, setNombre] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [padreId, setPadreId] = useState<number | null>(null);
  const [error, setError] = useState('');

  const createMutation = useCreateCategoria();
  const updateMutation = useUpdateCategoria();
  const isEdit = !!categoria;
  const isPending = createMutation.isPending || updateMutation.isPending;

  useEffect(() => {
    if (isOpen) {
      setNombre(categoria?.nombre ?? '');
      setDescripcion(categoria?.descripcion ?? '');
      setPadreId(categoria?.padre_id ?? null);
      setError('');
    }
  }, [isOpen, categoria]);

  const flatOptions = flattenTree(categorias, 0, categoria?.id);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const trimmed = nombre.trim();
    if (!trimmed) {
      setError('El nombre es obligatorio.');
      return;
    }
    if (trimmed.length > 100) {
      setError('El nombre no puede superar los 100 caracteres.');
      return;
    }

    const payload: CategoriaCreate = {
      nombre: trimmed,
      descripcion: descripcion.trim() || undefined,
      padre_id: padreId ?? undefined,
    };

    if (isEdit && categoria) {
      updateMutation.mutate(
        { id: categoria.id, data: payload },
        { onSuccess: () => { onSuccess(); onClose(); }, onError: handleError },
      );
    } else {
      createMutation.mutate(
        payload,
        { onSuccess: () => { onSuccess(); onClose(); }, onError: handleError },
      );
    }
  };

  const handleError = (err: unknown) => {
    const axiosError = err as { response?: { data?: { message?: string } } };
    setError(axiosError.response?.data?.message ?? 'Ocurrió un error al guardar la categoría.');
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={isEdit ? 'Editar categoría' : 'Nueva categoría'}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Nombre"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          maxLength={100}
          required
        />

        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-gray-700">Descripción</label>
          <textarea
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
            rows={3}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-400 transition-colors resize-none"
          />
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-gray-700">Categoría padre</label>
          <select
            value={padreId ?? ''}
            onChange={(e) => setPadreId(e.target.value ? Number(e.target.value) : null)}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-400 bg-white"
          >
            <option value="">— Ninguna (categoría raíz) —</option>
            {flatOptions.map((opt) => (
              <option key={opt.id} value={opt.id ?? ''}>
                {'— '.repeat(opt.depth)}{opt.nombre}
              </option>
            ))}
          </select>
        </div>

        {error && (
          <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2">
            {error}
          </p>
        )}

        <div className="flex justify-end gap-3 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>
            Cancelar
          </Button>
          <Button type="submit" isLoading={isPending}>
            {isEdit ? 'Guardar cambios' : 'Crear categoría'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
