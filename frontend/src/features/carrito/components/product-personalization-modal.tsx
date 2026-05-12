import { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/shared/ui/dialog';
import { Button } from '@/shared/ui/button';
import { Check } from 'lucide-react';
import type { Product } from '@/shared/types';

interface ProductPersonalizationModalProps {
  isOpen: boolean;
  onClose: () => void;
  producto: Product;
  onConfirm: (ingredientesExcluidos: number[]) => void;
}

export function ProductPersonalizationModal({
  isOpen,
  onClose,
  producto,
  onConfirm,
}: ProductPersonalizationModalProps) {
  const [selectedIngredients, setSelectedIngredients] = useState<number[]>([]);

  const ingredientes = producto.ingredientes ?? [];

  const toggleIngredient = (id: number) => {
    setSelectedIngredients((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id],
    );
  };

  const handleConfirm = () => {
    onConfirm(selectedIngredients);
    setSelectedIngredients([]);
    onClose();
  };

  const handleClose = () => {
    setSelectedIngredients([]);
    onClose();
  };

  // Si el producto no tiene ingredientes, no mostrar modal
  if (ingredientes.length === 0) {
    return null;
  }

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Personalizar {producto.nombre}</DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          <p className="text-sm text-gray-600">
            Selecciona los ingredientes que deseas excluir:
          </p>

          <div className="space-y-2 max-h-64 overflow-y-auto">
            {ingredientes.map((ingrediente) => (
              <label
                key={ingrediente.id}
                className="flex items-center gap-3 p-3 border rounded-md cursor-pointer hover:bg-gray-50"
              >
                <input
                  type="checkbox"
                  checked={selectedIngredients.includes(ingrediente.id)}
                  onChange={() => toggleIngredient(ingrediente.id)}
                  className="w-4 h-4 rounded border-gray-300 text-amber-600 focus:ring-amber-500"
                />
                <span className="flex-1">{ingrediente.nombre}</span>
                {ingrediente.es_alergeno && (
                  <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded">
                    Alérgeno
                  </span>
                )}
              </label>
            ))}
          </div>

          {selectedIngredients.length > 0 && (
            <p className="text-sm text-gray-500">
              {selectedIngredients.length} ingrediente(s) excluido(s)
            </p>
          )}
        </div>

        <div className="flex justify-end gap-2 pt-4">
          <Button variant="outline" onClick={handleClose}>
            Cancelar
          </Button>
          <Button onClick={handleConfirm}>
            <Check className="w-4 h-4 mr-2" />
            Agregar al Carrito
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}