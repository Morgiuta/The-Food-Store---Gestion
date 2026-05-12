import { useState } from 'react';
import { useAuth } from '@/shared/hooks/use-auth';
import { useUpdatePerfil } from '@/features/usuarios/hooks/use-perfil';
import { ChangePasswordModal } from '@/features/auth/components/change-password-modal';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { Card } from '@/shared/ui/card';

export default function ProfilePage() {
  const { user } = useAuth();
  const updatePerfil = useUpdatePerfil();

  const [nombre, setNombre] = useState(user?.nombre ?? '');
  const [email, setEmail] = useState(user?.email ?? '');
  const [telefono, setTelefono] = useState(user?.telefono ?? '');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [showPasswordModal, setShowPasswordModal] = useState(false);

  if (!user) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess(false);

    if (!nombre.trim() || !email.trim()) {
      setError('Nombre y email son obligatorios.');
      return;
    }

    updatePerfil.mutate(
      { nombre: nombre.trim(), email: email.trim(), telefono: telefono.trim() || null },
      {
        onSuccess: () => {
          setSuccess(true);
        },
        onError: (err: unknown) => {
          const axiosError = err as { response?: { data?: { message?: string } } };
          setError(axiosError.response?.data?.message ?? 'Error al actualizar el perfil.');
        },
      },
    );
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-800">Mi Perfil</h1>
        <p className="text-sm text-gray-500 mt-1">Administrá tus datos personales</p>
      </div>

      <Card title="Datos personales">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Nombre"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
          />
          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <Input
            label="Teléfono"
            value={telefono}
            onChange={(e) => setTelefono(e.target.value)}
          />

          {error && (
            <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2">
              {error}
            </p>
          )}

          {success && (
            <p className="text-sm text-green-700 bg-green-50 border border-green-200 rounded-md px-3 py-2">
              Perfil actualizado correctamente.
            </p>
          )}

          <div className="flex justify-end">
            <Button type="submit" isLoading={updatePerfil.isPending}>
              Guardar cambios
            </Button>
          </div>
        </form>
      </Card>

      <Card title="Seguridad">
        <p className="text-sm text-gray-600 mb-4">
          Podés cambiar tu contraseña en cualquier momento.
        </p>
        <Button
          type="button"
          variant="secondary"
          onClick={() => setShowPasswordModal(true)}
        >
          Cambiar contraseña
        </Button>
      </Card>

      <ChangePasswordModal
        isOpen={showPasswordModal}
        onClose={() => setShowPasswordModal(false)}
      />
    </div>
  );
}
