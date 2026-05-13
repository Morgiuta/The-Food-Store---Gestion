import { useState, useEffect } from 'react';
import { useConfig, useUpdateConfig, useFormasPago, useToggleFormaPago } from '@/features/admin/hooks/useAdminConfig';
import { Button } from '@/shared/ui/button';
import { Spinner } from '@/shared/ui/spinner';

export default function AdminConfigPage() {
  const { data: configs, isLoading: configsLoading } = useConfig();
  const { data: formasPago, isLoading: formasLoading } = useFormasPago();
  const updateConfigMutation = useUpdateConfig();
  const toggleFormaMutation = useToggleFormaPago();

  const [formValues, setFormValues] = useState<Record<string, string>>({});

  useEffect(() => {
    if (configs) {
      const values: Record<string, string> = {};
      configs.forEach((c) => { values[c.clave] = c.valor; });
      setFormValues(values);
    }
  }, [configs]);

  const handleSaveConfig = async () => {
    const configsToSave = Object.entries(formValues).map(([clave, valor]) => ({ clave, valor, descripcion: null }));
    updateConfigMutation.mutate(configsToSave);
  };

  const handleToggle = (id: number, currentActive: boolean) => {
    toggleFormaMutation.mutate({ id, activo: !currentActive });
  };

  const isLoading = configsLoading || formasLoading;

  if (isLoading) {
    return <div className="flex justify-center py-16"><Spinner size="lg" /></div>;
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Configuración</h1>
        <p className="text-sm text-gray-500 mt-1">Gestioná los parámetros globales del sistema.</p>
      </div>

      {/* General Config */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Configuración general</h2>
        
        {(!configs || configs.length === 0) ? (
          <p className="text-gray-400 text-sm">No hay configuraciones disponibles.</p>
        ) : (
          <div className="space-y-4 max-w-lg">
            {configs.map((config) => (
              <div key={config.clave}>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {config.descripcion || config.clave}
                </label>
                <input
                  type="text"
                  value={formValues[config.clave] || ''}
                  onChange={(e) => setFormValues({ ...formValues, [config.clave]: e.target.value })}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                />
              </div>
            ))}

            <div className="pt-4">
              <Button
                onClick={handleSaveConfig}
                disabled={updateConfigMutation.isPending}
              >
                {updateConfigMutation.isPending ? 'Guardando...' : 'Guardar configuración'}
              </Button>
              {updateConfigMutation.isSuccess && (
                <span className="ml-3 text-sm text-green-600">✓ Guardado</span>
              )}
              {updateConfigMutation.isError && (
                <span className="ml-3 text-sm text-red-600">
                  Error: {updateConfigMutation.error instanceof Error ? updateConfigMutation.error.message : 'Error al guardar'}
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Payment Methods */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Formas de pago</h2>

        {(!formasPago || formasPago.length === 0) ? (
          <p className="text-gray-400 text-sm">No hay formas de pago registradas.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                  <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">Estado</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acción</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {formasPago.map((fp) => (
                  <tr key={fp.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm text-gray-500">{fp.id}</td>
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">{fp.nombre}</td>
                    <td className="px-4 py-3 text-center">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        fp.activo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {fp.activo ? 'Activo' : 'Inactivo'}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-right">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleToggle(fp.id, fp.activo)}
                        disabled={toggleFormaMutation.isPending && toggleFormaMutation.variables?.id === fp.id}
                      >
                        {fp.activo ? 'Desactivar' : 'Activar'}
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
