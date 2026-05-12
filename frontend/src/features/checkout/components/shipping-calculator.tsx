import { useNavigate } from 'react-router-dom';
import { MapPin } from 'lucide-react';
import { Button } from '@/shared/ui/button';
import type { Direccion } from '@/features/direcciones/hooks/use-direcciones';

interface ShippingCalculatorProps {
  direcciones: Direccion[];
  selectedDireccionId: number | null;
  onSelectDireccion: (direccionId: number) => void;
  costoEnvio: number;
  isLoading?: boolean;
}

export function ShippingCalculator({
  direcciones,
  selectedDireccionId,
  onSelectDireccion,
  costoEnvio,
  isLoading,
}: ShippingCalculatorProps) {
  const navigate = useNavigate();

  const direccionSeleccionada = direcciones.find((d) => d.id === selectedDireccionId);

  return (
    <div className="bg-gray-50 rounded-lg p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Dirección de Entrega</h2>

      {isLoading ? (
        <p className="text-gray-500">Cargando direcciones...</p>
      ) : direcciones.length === 0 ? (
        <div className="text-center py-4">
          <p className="text-gray-500 mb-4">No tienes direcciones guardadas</p>
          <Button variant="outline" onClick={() => navigate('/mis-direcciones')}>
            Agregar Dirección
          </Button>
        </div>
      ) : (
        <div className="space-y-3">
          {direcciones.map((direccion) => {
            const isSelected = direccion.id === selectedDireccionId;
            const fullAddress = [
              direccion.calle,
              direccion.numero,
              direccion.piso && `, Piso ${direccion.piso}`,
              direccion.departamento && `, Depto ${direccion.departamento}`,
            ]
              .filter(Boolean)
              .join('');

            return (
              <label
                key={direccion.id}
                className={`flex items-start gap-3 p-3 border rounded-lg cursor-pointer transition-colors ${
                  isSelected
                    ? 'border-amber-500 bg-amber-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <input
                  type="radio"
                  name="direccion"
                  value={direccion.id}
                  checked={isSelected}
                  onChange={() => onSelectDireccion(direccion.id)}
                  className="mt-1"
                />
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-gray-400" />
                    <span className="font-medium text-gray-900">
                      {fullAddress}, {direccion.ciudad}, {direccion.codigo_postal}
                    </span>
                  </div>
                  {direccion.es_predeterminada && (
                    <span className="inline-block mt-1 text-xs bg-amber-100 text-amber-800 px-2 py-0.5 rounded">
                      Predeterminada
                    </span>
                  )}
                  {direccion.referencia && (
                    <p className="text-sm text-gray-500 mt-1">{direccion.referencia}</p>
                  )}
                </div>
              </label>
            );
          })}

          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate('/mis-direcciones')}
            className="w-full"
          >
            + Agregar nueva dirección
          </Button>
        </div>
      )}

      {/* Costo de envío */}
      {selectedDireccionId && (
        <div className="mt-6 pt-4 border-t">
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Costo de envío:</span>
            <span className="font-medium text-gray-900">${costoEnvio.toFixed(2)}</span>
          </div>
        </div>
      )}
    </div>
  );
}