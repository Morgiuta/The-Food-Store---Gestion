import { useState } from 'react';
import { useCrearPago } from '../hooks/usePago';
import { Button } from '@/shared/ui/button';

interface Props {
  pedidoId: number;
  onSuccess: (preferenceId: string, initPoint: string) => void;
  onError: (error: string) => void;
}

export function PaymentForm({ pedidoId, onSuccess, onError }: Props) {
  const [isProcessing, setIsProcessing] = useState(false);
  const crearPagoMutation = useCrearPago();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isProcessing) return;

    setIsProcessing(true);
    try {
      const result = await crearPagoMutation.mutateAsync({ pedido_id: pedidoId });
      onSuccess(result.preference_id, result.init_point);
    } catch (err) {
      onError(err instanceof Error ? err.message : 'Error al procesar el pago');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
        <p className="text-sm text-blue-700">
          Al hacer clic en "Pagar ahora", serás redirigido a MercadoPago para completar el pago de forma segura.
        </p>
      </div>

      {crearPagoMutation.error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-3">
          <p className="text-sm text-red-700">
            {crearPagoMutation.error instanceof Error
              ? crearPagoMutation.error.message
              : 'Error al iniciar el pago'}
          </p>
        </div>
      )}

      <Button
        type="submit"
        className="w-full"
        size="lg"
        isLoading={isProcessing}
      >
        {isProcessing ? 'Iniciando pago...' : 'Pagar ahora'}
      </Button>
    </form>
  );
}
