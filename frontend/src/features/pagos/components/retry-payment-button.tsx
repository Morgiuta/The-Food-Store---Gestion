import { Button } from '@/shared/ui/button';

interface Props {
  onClick: () => void;
  disabled?: boolean;
}

export function RetryPaymentButton({ onClick, disabled }: Props) {
  return (
    <Button
      variant="outline"
      onClick={onClick}
      disabled={disabled}
      className="text-blue-600 border-blue-300 hover:bg-blue-50"
    >
      Reintentar pago
    </Button>
  );
}
