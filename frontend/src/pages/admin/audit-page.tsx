import { useState } from 'react';
import { useAuditLog } from '@/features/admin/hooks/useAuditLog';
import { Button } from '@/shared/ui/button';
import { Spinner } from '@/shared/ui/spinner';

const TABLAS = ['', 'usuarios', 'productos', 'pedidos', 'pagos'];
const ACCIONES = ['', 'CREATE', 'UPDATE', 'DELETE'];

export default function AdminAuditPage() {
  const [page, setPage] = useState(1);
  const [tabla, setTabla] = useState('');
  const [accion, setAccion] = useState('');
  const { data, isLoading, error } = useAuditLog({ page, size: 50, tabla: tabla || undefined, accion: accion || undefined });

  const formatDate = (d: string) => new Date(d).toLocaleString('es-AR');

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Auditoría</h1>
        <p className="text-sm text-gray-500 mt-1">Registro de cambios en el sistema.</p>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Tabla</label>
            <select value={tabla} onChange={e => { setTabla(e.target.value); setPage(1); }}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm">
              {TABLAS.map(t => <option key={t} value={t}>{t || 'Todas'}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Acción</label>
            <select value={accion} onChange={e => { setAccion(e.target.value); setPage(1); }}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm">
              {ACCIONES.map(a => <option key={a} value={a}>{a || 'Todas'}</option>)}
            </select>
          </div>
        </div>
      </div>

      {isLoading && <div className="flex justify-center py-12"><Spinner size="lg" /></div>}
      {error && <div className="bg-red-50 border border-red-200 rounded-md p-4 text-red-700 text-sm">Error al cargar auditoría.</div>}

      {data && (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          {data.items.length === 0 ? (
            <div className="text-center py-12 text-gray-500">Sin registros de auditoría.</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-3 py-2 text-xs font-medium text-gray-500 uppercase">ID</th>
                    <th className="px-3 py-2 text-xs font-medium text-gray-500 uppercase">Usuario</th>
                    <th className="px-3 py-2 text-xs font-medium text-gray-500 uppercase">Acción</th>
                    <th className="px-3 py-2 text-xs font-medium text-gray-500 uppercase">Tabla</th>
                    <th className="px-3 py-2 text-xs font-medium text-gray-500 uppercase">Registro</th>
                    <th className="px-3 py-2 text-xs font-medium text-gray-500 uppercase">Fecha</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {data.items.map(entry => (
                    <tr key={entry.id} className="hover:bg-gray-50">
                      <td className="px-3 py-2 text-sm text-gray-500">{entry.id}</td>
                      <td className="px-3 py-2 text-sm text-gray-900">{entry.usuario_id || '—'}</td>
                      <td className="px-3 py-2">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                          entry.accion === 'CREATE' ? 'bg-green-100 text-green-800' :
                          entry.accion === 'UPDATE' ? 'bg-blue-100 text-blue-800' :
                          'bg-red-100 text-red-800'
                        }`}>{entry.accion}</span>
                      </td>
                      <td className="px-3 py-2 text-sm text-gray-600">{entry.tabla}</td>
                      <td className="px-3 py-2 text-sm text-gray-600">{entry.registro_id || '—'}</td>
                      <td className="px-3 py-2 text-sm text-gray-500">{formatDate(entry.created_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {data.pages > 1 && (
            <div className="flex items-center justify-between px-4 py-3 border-t">
              <span className="text-sm text-gray-600">Pág {data.page} de {data.pages}</span>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage(p => p - 1)}>Anterior</Button>
                <Button variant="outline" size="sm" disabled={page >= data.pages} onClick={() => setPage(p => p + 1)}>Siguiente</Button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
