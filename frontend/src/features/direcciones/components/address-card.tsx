import { Button } from '@/shared/ui/button';
import { Pencil, Trash2, Star } from 'lucide-react';
import type { Direccion } from '../hooks/use-direcciones';

interface AddressCardProps {
  direccion: Direccion;
  onEdit: (direccion: Direccion) => void;
  onDelete: (id: number) => void;
  onSetDefault: (id: number) => void;
  isDeleting?: boolean;
  isSettingDefault?: boolean;
}

export function AddressCard({
  direccion,
  onEdit,
  onDelete,
  onSetDefault,
  isDeleting,
  isSettingDefault,
}: AddressCardProps) {
  const fullAddress = [
    direccion.calle,
    direccion.numero,
    direccion.piso && `, Piso ${direccion.piso}`,
    direccion.departamento && `, Depto ${direccion.departamento}`,
  ]
    .filter(Boolean)
    .join('');

  return (
    <div className="border rounded-lg p-4 space-y-3 bg-white">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          {direccion.es_predeterminada && (
            <span className="inline-flex items-center gap-1 text-xs bg-amber-100 text-amber-800 px-2 py-0.5 rounded-full mb-2">
              <Star className="w-3 h-3 fill-current" />
              Predeterminada
            </span>
          )}
          <p className="font-medium text-gray-900">
            {fullAddress}, {direccion.ciudad}, {direccion.codigo_postal}
          </p>
          {direccion.referencia && (
            <p className="text-sm text-gray-500 mt-1">
              Referencia: {direccion.referencia}
            </p>
          )}
        </div>
      </div>

      <div className="flex items-center gap-2 pt-2 border-t">
        {!direccion.es_predeterminada && (
          <Button
            variant="outline"
            size="sm"
            onClick={() => onSetDefault(direccion.id)}
            disabled={isSettingDefault}
          >
            <Star className="w-4 h-4 mr-1" />
            Predeterminada
          </Button>
        )}
        <Button
          variant="outline"
          size="sm"
          onClick={() => onEdit(direccion)}
        >
          <Pencil className="w-4 h-4 mr-1" />
          Editar
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => onDelete(direccion.id)}
          disabled={isDeleting}
          className="text-red-600 hover:text-red-700 hover:bg-red-50"
        >
          <Trash2 className="w-4 h-4 mr-1" />
          Eliminar
        </Button>
      </div>
    </div>
  );
}