import { CreditCard } from 'lucide-react';

export function PaymentMethodSelector() {
  return (
    <div className="bg-gray-50 rounded-lg p-6 mt-4">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Método de Pago</h2>

      <div className="flex items-center gap-3 p-4 border border-amber-200 bg-amber-50 rounded-lg">
        <CreditCard className="w-6 h-6 text-amber-600" />
        <div>
          <p className="font-medium text-gray-900">MercadoPago</p>
          <p className="text-sm text-gray-500">Pago rápido y seguro</p>
        </div>
      </div>

      <p className="text-sm text-gray-500 mt-4">
        Serás redirigido a MercadoPago para completar el pago de forma segura.
      </p>
    </div>
  );
}