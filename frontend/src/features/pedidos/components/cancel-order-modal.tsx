import { useState } from 'react';
import { useCancelarPedido } from '../hooks/useOrders';
import { Modal } from '@/shared/ui/modal';
import { Button } from '@/shared/ui/button';
import { Spinner } from '@/shared/ui/spinner';

interface Props {
  pedidoId: number;
  isOpen: boolean;
  onClose: () => void;
}

export function CancelOrderModal({ pedidoId, isOpen, onClose }: Props) {
  const [motivo, setMotivo] = useState('');
  const cancelMutation = useCancelarPedido();

  const handleCancel = async () => {
    if (!motivo.trim() || motivo.trim().length < 5) return;
    try {
      await cancelMutation.mutateAsync({ pedidoId, motivo: motivo.trim() });
      setMotivo('');
      onClose();
    } catch {
      // error handled by mutation
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Cancelar pedido">
      <div className="space-y-4">
        <div className="bg-red-50 border border-red-200 rounded-md p-3">
          <p className="text-sm text-red-700">
            <strong>Advertencia:</strong> Esta acción no se puede deshacer. El pedido será cancelado y no podrá continuar su proceso.
          </p>
        </div>

        <div>
          <label htmlFor="motivo" className="block text-sm font-medium text-gray-700 mb-1">
            Motivo de cancelaci&oacute;n *
          </label>
          <textarea
            id="motivo"
            rows={3}
            className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-red-500 focus:border-red-500"
            placeholder="Indicá el motivo de la cancelación..."
            value={motivo}
            onChange={(e) => setMotivo(e.target.value)}
            disabled={cancelMutation.isPending}
          />
          {motivo.length > 0 && motivo.length < 5 && (
            <p className="text-xs text-red-500 mt-1">El motivo debe tener al menos 5 caracteres</p>
          )}
        </div>

        {cancelMutation.error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-3">
            <p className="text-sm text-red-700">
              {cancelMutation.error instanceof Error
                ? cancelMutation.error.message
                : 'Error al cancelar el pedido'}
            </p>
          </div>
        )}

        <div className="flex justify-end gap-3">
          <Button variant="outline" onClick={onClose} disabled={cancelMutation.isPending}>
            Volver
          </Button>
          <Button
            variant="danger"
            onClick={handleCancel}
            disabled={!motivo.trim() || motivo.trim().length < 5 || cancelMutation.isPending}
          >
            {cancelMutation.isPending ? <Spinner size="sm" /> : 'Confirmar cancelación'}
          </Button>
        </div>
      </div>
    </Modal>
  );
}
