import { useState } from 'react';
import { useAvanzarEstado } from '../hooks/useOrders';
import { Modal } from '@/shared/ui/modal';
import { Button } from '@/shared/ui/button';
import { Spinner } from '@/shared/ui/spinner';

interface Props {
  pedidoId: number;
  estadoActual: string;
  isOpen: boolean;
  onClose: () => void;
}

const TRANSICIONES: Record<string, { value: string; label: string }[]> = {
  CONFIRMADO: [
    { value: 'EN_PREPARACION', label: 'En Preparación' },
  ],
  EN_PREPARACION: [
    { value: 'EN_CAMINO', label: 'En Camino' },
  ],
  EN_CAMINO: [
    { value: 'ENTREGADO', label: 'Entregado' },
  ],
};

export function ChangeStatusModal({ pedidoId, estadoActual, isOpen, onClose }: Props) {
  const [nuevoEstado, setNuevoEstado] = useState('');
  const avanzarMutation = useAvanzarEstado();

  const opciones = TRANSICIONES[estadoActual] || [];

  const handleAvanzar = async () => {
    if (!nuevoEstado) return;
    try {
      await avanzarMutation.mutateAsync({ pedidoId, nuevoEstado });
      setNuevoEstado('');
      onClose();
    } catch {
      // error handled by mutation
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Avanzar estado del pedido">
      <div className="space-y-4">
        <div>
          <p className="text-sm text-gray-600 mb-1">Estado actual:</p>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
            {estadoActual}
          </span>
        </div>

        {opciones.length === 0 ? (
          <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
            <p className="text-sm text-yellow-700">
              No hay transiciones disponibles desde este estado.
            </p>
          </div>
        ) : (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Seleccionar nuevo estado
            </label>
            <div className="space-y-2">
              {opciones.map((op) => (
                <label
                  key={op.value}
                  className={`flex items-center p-3 border rounded-md cursor-pointer transition-colors ${
                    nuevoEstado === op.value
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:bg-gray-50'
                  }`}
                >
                  <input
                    type="radio"
                    name="nuevoEstado"
                    value={op.value}
                    checked={nuevoEstado === op.value}
                    onChange={(e) => setNuevoEstado(e.target.value)}
                    className="mr-3"
                  />
                  <span className="text-sm font-medium text-gray-900">{op.label}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        {avanzarMutation.error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-3">
            <p className="text-sm text-red-700">
              {avanzarMutation.error instanceof Error
                ? avanzarMutation.error.message
                : 'Error al avanzar el estado'}
            </p>
          </div>
        )}

        <div className="flex justify-end gap-3">
          <Button variant="outline" onClick={onClose} disabled={avanzarMutation.isPending}>
            Volver
          </Button>
          {opciones.length > 0 && (
            <Button
              onClick={handleAvanzar}
              disabled={!nuevoEstado || avanzarMutation.isPending}
            >
              {avanzarMutation.isPending ? <Spinner size="sm" /> : 'Avanzar estado'}
            </Button>
          )}
        </div>
      </div>
    </Modal>
  );
}
