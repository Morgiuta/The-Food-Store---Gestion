import { useEstadoPago } from '../hooks/usePago';
import { Modal } from '@/shared/ui/modal';
import { Button } from '@/shared/ui/button';
import { Spinner } from '@/shared/ui/spinner';

interface Props {
  pedidoId: number;
  isOpen: boolean;
  onClose: () => void;
  onRetry: () => void;
  onViewOrder: () => void;
}

export function PaymentStatusModal({ pedidoId, isOpen, onClose, onRetry, onViewOrder }: Props) {
  const { data: pago, isLoading } = useEstadoPago(pedidoId);

  const status = pago?.mp_status;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Estado del pago">
      <div className="space-y-4 text-center">
        {isLoading && (
          <div className="py-8">
            <Spinner size="lg" />
            <p className="text-sm text-gray-500 mt-2">Consultando estado del pago...</p>
          </div>
        )}

        {!isLoading && !status && (
          <div className="py-8">
            <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="text-lg font-medium text-gray-900">Iniciando pago...</p>
            <p className="text-sm text-gray-500 mt-1">Esperando confirmación de MercadoPago.</p>
          </div>
        )}

        {status === 'approved' && (
          <div className="py-8">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <p className="text-lg font-medium text-green-900">¡Pago aprobado!</p>
            <p className="text-sm text-gray-500 mt-1">Tu pedido fue confirmado y está siendo procesado.</p>
            <div className="mt-4">
              <Button onClick={onViewOrder}>Ver mi pedido</Button>
            </div>
          </div>
        )}

        {status === 'rejected' && (
          <div className="py-8">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <p className="text-lg font-medium text-red-900">Pago rechazado</p>
            <p className="text-sm text-gray-500 mt-1">El pago no pudo ser procesado. Podés intentar con otro medio de pago.</p>
            <div className="flex justify-center gap-3 mt-4">
              <Button variant="outline" onClick={onClose}>Cerrar</Button>
              <Button onClick={onRetry}>Reintentar</Button>
            </div>
          </div>
        )}

        {(status === 'pending' || status === 'in_process') && (
          <div className="py-8">
            <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Spinner size="lg" />
            </div>
            <p className="text-lg font-medium text-gray-900">Pago en proceso</p>
            <p className="text-sm text-gray-500 mt-1">Estamos esperando la confirmación de MercadoPago.</p>
          </div>
        )}

        {pago && (
          <div className="text-xs text-gray-400 pt-4 border-t border-gray-200">
            <p>Monto: ${Number(pago.monto).toLocaleString('es-AR', { minimumFractionDigits: 2 })}</p>
            <p>Estado: {pago.mp_status || 'pendiente'}</p>
          </div>
        )}
      </div>
    </Modal>
  );
}
