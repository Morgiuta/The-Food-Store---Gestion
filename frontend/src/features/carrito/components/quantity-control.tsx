import { Minus, Plus } from 'lucide-react';
import { Button } from '@/shared/ui/button';

interface QuantityControlProps {
  cantidad: number;
  onChange: (cantidad: number) => void;
  min?: number;
  max?: number;
}

export function QuantityControl({
  cantidad,
  onChange,
  min = 1,
  max = 999,
}: QuantityControlProps) {
  const handleDecrement = () => {
    if (cantidad > min) {
      onChange(cantidad - 1);
    }
  };

  const handleIncrement = () => {
    if (cantidad < max) {
      onChange(cantidad + 1);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value, 10);
    if (!isNaN(value)) {
      onChange(Math.min(Math.max(value, min), max));
    }
  };

  return (
    <div className="flex items-center gap-2">
      <Button
        type="button"
        variant="outline"
        size="icon"
        className="h-8 w-8"
        onClick={handleDecrement}
        disabled={cantidad <= min}
      >
        <Minus className="h-4 w-4" />
      </Button>

      <input
        type="number"
        value={cantidad}
        onChange={handleInputChange}
        min={min}
        max={max}
        className="w-14 h-8 text-center border rounded-md text-sm"
      />

      <Button
        type="button"
        variant="outline"
        size="icon"
        className="h-8 w-8"
        onClick={handleIncrement}
        disabled={cantidad >= max}
      >
        <Plus className="h-4 w-4" />
      </Button>
    </div>
  );
}