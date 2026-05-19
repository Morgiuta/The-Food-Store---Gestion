import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';
import { useDirecciones } from '@/features/direcciones/hooks/use-direcciones';
import { useCartStore } from '@/app/store/cart-store';

interface CheckoutItem {
  producto_id: number;
  cantidad: number;
}

interface ValidacionStock {
  valido: boolean;
  errores: string[];
  items_validados: CheckoutItem[];
}

interface CheckoutTotal {
  subtotal: number;
  costo_envio: number;
  total: number;
  direccion_id: number | null;
}

export function useCheckout() {
  const items = useCartStore((state) => state.items);
  const { data: direcciones, isLoading: isLoadingDirecciones } = useDirecciones();

  // Estado para la dirección seleccionada
  const [selectedDireccionId, setSelectedDireccionId] = useState<number | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);

  // Mutación para validar stock
  const validarStockMutation = useMutation({
    mutationFn: async (itemsToValidate: CheckoutItem[]) => {
      const response = await apiClient.post(ENDPOINTS.PEDIDOS.VALIDAR, {
        items: itemsToValidate,
      });
      return response.data as ValidacionStock;
    },
  });

  // Mutación para calcular total
  const calcularTotalMutation = useMutation({
    mutationFn: async (itemsToCalculate: CheckoutItem[]) => {
      const response = await apiClient.post(ENDPOINTS.PEDIDOS.CALCULAR_TOTAL, {
        items: itemsToCalculate,
        direccion_id: selectedDireccionId,
      });
      return response.data as CheckoutTotal;
    },
  });

  // Calcular subtotal local (sin llamada al backend)
  const calcularSubtotal = useCallback(() => {
    return items.reduce((sum, item) => sum + item.producto.precio * item.cantidad, 0);
  }, [items]);

  // Costo de envío fijo
  const costoEnvio = 500;

  // Total = subtotal + envío
  const total = calcularSubtotal() + costoEnvio;

  // Validar stock al cargar el checkout
  const validarStock = useCallback(async () => {
    if (items.length === 0) {
      setValidationError("El carrito está vacío");
      return false;
    }

    const itemsToValidate: CheckoutItem[] = items.map((item) => ({
      producto_id: item.producto.id,
      cantidad: item.cantidad,
    }));

    try {
      const result = await validarStockMutation.mutateAsync(itemsToValidate);
      if (!result.valido) {
        setValidationError(result.errores.join("\n"));
        return false;
      }
      setValidationError(null);
      return true;
    } catch (error) {
      setValidationError("Error al validar el stock");
      return false;
    }
  }, [items, validarStockMutation]);

  // Seleccionar dirección
  const selectDireccion = (direccionId: number) => {
    setSelectedDireccionId(direccionId);
  };

  // Obtener dirección seleccionada
  const direccionSeleccionada = direcciones?.find((d) => d.id === selectedDireccionId);

  return {
    // Estado
    items,
    direcciones: direcciones ?? [],
    isLoadingDirecciones,
    selectedDireccionId,
    direccionSeleccionada,
    validationError,
    calcularSubtotal,
    costoEnvio,
    total,

    // Funciones
    validarStock,
    selectDireccion,
    isValidating: validarStockMutation.isPending,
    isCalculating: calcularTotalMutation.isPending,
  };
}
