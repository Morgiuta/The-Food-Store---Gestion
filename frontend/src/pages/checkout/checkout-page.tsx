import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShoppingCart, AlertCircle } from 'lucide-react';
import { Button } from '@/shared/ui/button';
import { OrderSummary } from '@/features/checkout/components/order-summary';
import { ShippingCalculator } from '@/features/checkout/components/shipping-calculator';
import { PaymentMethodSelector } from '@/features/checkout/components/payment-method-selector';
import { ReviewOrderModal } from '@/features/checkout/components/review-order-modal';
import { useCheckout } from '@/features/checkout/hooks/use-checkout';
import { useCartStore } from '@/app/store/cart-store';

export default function CheckoutPage() {
  const navigate = useNavigate();
  const items = useCartStore((state) => state.items);
  const [showReviewModal, setShowReviewModal] = useState(false);

  const {
    direcciones,
    isLoadingDirecciones,
    selectedDireccionId,
    selectDireccion,
    direccionSeleccionada,
    validationError,
    calcularSubtotal,
    costoEnvio,
    total,
    validarStock,
  } = useCheckout();

  // Validar stock al cargar la página
  useEffect(() => {
    if (items.length > 0) {
      validarStock();
    }
  }, [items.length, validarStock]);

  // Redirigir si el carrito está vacío
  useEffect(() => {
    if (items.length === 0) {
      navigate('/carrito');
    }
  }, [items.length, navigate]);

  const subtotal = calcularSubtotal();

  const handleConfirmarPedido = () => {
    // TODO: Aquí se llamaría al backend para crear el pedido (sprint-4)
    alert("Esta funcionalidad se implementará en el sprint de creación de pedidos");
    setShowReviewModal(false);
  };

  if (items.length === 0) {
    return null; // Evita flicker antes de la redirección
  }

  return (
    <div className="max-w-5xl mx-auto py-8 px-4">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Checkout</h1>
        <p className="text-gray-600">Revisa y confirma tu pedido</p>
      </div>

      {/* Errores de validación de stock */}
      {validationError && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 mt-0.5" />
          <div>
            <p className="font-medium text-red-800">Error de validación</p>
            <p className="text-sm text-red-600 mt-1 whitespace-pre-line">
              {validationError}
            </p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Columna izquierda: Order Summary */}
        <div>
          <OrderSummary
            items={items}
            subtotal={subtotal}
            costoEnvio={costoEnvio}
            total={total}
          />
        </div>

        {/* Columna derecha: Shipping & Payment */}
        <div className="space-y-4">
          <ShippingCalculator
            direcciones={direcciones}
            selectedDireccionId={selectedDireccionId}
            onSelectDireccion={selectDireccion}
            costoEnvio={costoEnvio}
            isLoading={isLoadingDirecciones}
          />

          <PaymentMethodSelector />

          {/* Botón de confirmar */}
          <Button
            className="w-full"
            size="lg"
            onClick={() => setShowReviewModal(true)}
            disabled={!selectedDireccionId || !!validationError}
          >
            Revisar y Confirmar Pedido
          </Button>
        </div>
      </div>

      {/* Modal de revisión */}
      <ReviewOrderModal
        isOpen={showReviewModal}
        onClose={() => setShowReviewModal(false)}
        onConfirm={handleConfirmarPedido}
        items={items}
        direccion={direccionSeleccionada}
        subtotal={subtotal}
        costoEnvio={costoEnvio}
        total={total}
      />
    </div>
  );
}