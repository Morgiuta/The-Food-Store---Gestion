import { useNavigate } from 'react-router-dom';
import { Button } from '@/shared/ui/button';

interface CartSummaryProps {
  totalItems: number;
  totalPrice: number;
}

export function CartSummary({ totalItems, totalPrice }: CartSummaryProps) {
  const navigate = useNavigate();

  return (
    <div className="border-t pt-4 mt-4">
      <div className="flex justify-between text-sm text-gray-600 mb-2">
        <span>Total de items:</span>
        <span>{totalItems}</span>
      </div>

      <div className="flex justify-between text-lg font-bold text-gray-900 mb-4">
        <span>Total:</span>
        <span>${totalPrice.toFixed(2)}</span>
      </div>

      <Button
        className="w-full"
        size="lg"
        onClick={() => navigate('/checkout')}
        disabled={totalItems === 0}
      >
        Ir al Checkout
      </Button>
    </div>
  );
}