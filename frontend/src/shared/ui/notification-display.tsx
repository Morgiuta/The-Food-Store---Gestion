import { useEffect, useRef } from 'react';
import { useUIStore } from '@/app/store/ui-store';

export function NotificationDisplay() {
  const { notifications, removeNotification } = useUIStore();
  const timersRef = useRef<Map<string, number>>(new Map());

  useEffect(() => {
    notifications.forEach((n) => {
      if (!timersRef.current.has(n.id)) {
        const timer = window.setTimeout(() => {
          removeNotification(n.id);
          timersRef.current.delete(n.id);
        }, 5000);
        timersRef.current.set(n.id, timer);
      }
    });

    return () => {
      timersRef.current.forEach((timer) => window.clearTimeout(timer));
      timersRef.current.clear();
    };
  }, [notifications, removeNotification]);

  if (notifications.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-sm">
      {notifications.map((n) => (
        <div
          key={n.id}
          className={`px-4 py-3 rounded-lg shadow-lg text-white text-sm flex items-start gap-2 ${
            n.type === 'error' ? 'bg-red-500' :
            n.type === 'success' ? 'bg-green-500' :
            n.type === 'warning' ? 'bg-yellow-500 text-yellow-900' :
            'bg-gray-700'
          }`}
        >
          <span className="flex-1">{n.message}</span>
          <button
            onClick={() => {
              const timer = timersRef.current.get(n.id);
              if (timer) window.clearTimeout(timer);
              timersRef.current.delete(n.id);
              removeNotification(n.id);
            }}
            className="ml-2 hover:opacity-70 shrink-0 text-lg leading-none"
          >
            &times;
          </button>
        </div>
      ))}
    </div>
  );
}
