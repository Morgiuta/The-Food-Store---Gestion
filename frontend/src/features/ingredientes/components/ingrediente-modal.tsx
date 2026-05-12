import { useState, useEffect } from 'react';
import { Modal } from '@/shared/ui/modal';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import {
  useCreateIngrediente,
  useUpdateIngrediente,
} from '../hooks/use-ingredientes';
import type { Ingrediente, IngredienteCreate } from '../hooks/use-ingredientes';

interface IngredienteModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  ingrediente?: Ingrediente | null;
}

export function IngredienteModal({
  isOpen,
  onClose,
  onSuccess,
  ingrediente,
}: IngredienteModalProps) {
  const [nombre, setNombre] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [esAlergeno, setEsAlergeno] = useState(false);
  const [error, setError] = useState('');

  const createMutation = useCreateIngrediente();
  const updateMutation = useUpdateIngrediente();
  const isEdit = !!ingrediente;
  const isPending = createMutation.isPending || updateMutation.isPending;

  useEffect(() => {
    if (isOpen) {
      setNombre(ingrediente?.nombre ?? '');
      setDescripcion(ingrediente?.descripcion ?? '');
      setEsAlergeno(ingrediente?.es_alergeno ?? false);
      setError('');
    }
  }, [isOpen, ingrediente]);

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

    const payload: IngredienteCreate = {
      nombre: trimmed,
      descripcion: descripcion.trim() || undefined,
      es_alergeno: esAlergeno,
    };

    if (isEdit && ingrediente) {
      updateMutation.mutate(
        { id: ingrediente.id, data: payload },
        {
          onSuccess: () => {
            onSuccess();
            onClose();
          },
          onError: handleError,
        },
      );
    } else {
      createMutation.mutate(payload, {
        onSuccess: () => {
          onSuccess();
          onClose();
        },
        onError: handleError,
      });
    }
  };

  const handleError = (err: unknown) => {
    const axiosError = err as {
      response?: { data?: { message?: string } };
    };
    setError(
      axiosError.response?.data?.message ??
        'Ocurrió un error al guardar el ingrediente.',
    );
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={isEdit ? 'Editar ingrediente' : 'Nuevo ingrediente'}
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Nombre"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          maxLength={100}
          required
        />

        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-gray-700">
            Descripción
          </label>
          <textarea
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
            rows={3}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-400 transition-colors resize-none"
          />
        </div>

        <label className="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={esAlergeno}
            onChange={(e) => setEsAlergeno(e.target.checked)}
            className="w-4 h-4 rounded border-gray-300 text-amber-500 focus:ring-amber-400"
          />
          <span className="text-sm font-medium text-gray-700">
            Es alérgeno
          </span>
        </label>

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
            {isEdit ? 'Guardar cambios' : 'Crear ingrediente'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
