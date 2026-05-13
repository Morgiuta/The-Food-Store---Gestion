const STATUS_STYLES: Record<string, string> = {
  PENDIENTE: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  CONFIRMADO: 'bg-blue-100 text-blue-800 border-blue-300',
  EN_PREPARACION: 'bg-orange-100 text-orange-800 border-orange-300',
  EN_CAMINO: 'bg-cyan-100 text-cyan-800 border-cyan-300',
  ENTREGADO: 'bg-green-100 text-green-800 border-green-300',
  CANCELADO: 'bg-red-100 text-red-800 border-red-300',
};

interface Props {
  estado: string;
}

export function OrderStatusBadge({ estado }: Props) {
  const styles = STATUS_STYLES[estado] || 'bg-gray-100 text-gray-800 border-gray-300';

  const labels: Record<string, string> = {
    PENDIENTE: 'Pendiente',
    CONFIRMADO: 'Confirmado',
    EN_PREPARACION: 'En Preparación',
    EN_CAMINO: 'En Camino',
    ENTREGADO: 'Entregado',
    CANCELADO: 'Cancelado',
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${styles}`}
    >
      {labels[estado] || estado}
    </span>
  );
}
