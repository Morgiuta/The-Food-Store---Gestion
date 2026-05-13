import type { OrderHistoryEntry } from '@/shared/types';
import { OrderStatusBadge } from './order-status-badge';

interface Props {
  historial: OrderHistoryEntry[];
}

export function OrderHistoryTimeline({ historial }: Props) {
  if (!historial || historial.length === 0) {
    return <p className="text-sm text-gray-400">Sin historial disponible</p>;
  }

  return (
    <div className="space-y-0">
      {historial.map((entry, index) => {
        const fecha = new Date(entry.timestamp).toLocaleString('es-AR', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
        });

        const isLast = index === historial.length - 1;

        return (
          <div key={entry.id} className="flex gap-3">
            <div className="flex flex-col items-center">
              <div
                className={`w-3 h-3 rounded-full border-2 flex-shrink-0 ${
                  isLast
                    ? 'bg-green-500 border-green-500'
                    : 'bg-white border-gray-400'
                }`}
              />
              {!isLast && (
                <div className="w-0.5 flex-1 bg-gray-300 min-h-[2rem]" />
              )}
            </div>

            <div className="pb-4 flex-1">
              <div className="flex items-center gap-2 flex-wrap">
                {entry.estado_anterior && (
                  <>
                    <OrderStatusBadge estado={entry.estado_anterior} />
                    <span className="text-gray-400 text-sm">→</span>
                  </>
                )}
                <OrderStatusBadge estado={entry.estado_nuevo} />
              </div>
              <p className="text-xs text-gray-400 mt-1">{fecha}</p>
              {entry.observacion && (
                <p className="text-sm text-gray-600 mt-0.5 italic">
                  &ldquo;{entry.observacion}&rdquo;
                </p>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
