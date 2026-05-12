import { useState } from 'react';
import { Modal } from '@/shared/ui/modal';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { useChangePassword } from '@/features/usuarios/hooks/use-perfil';
import { useAuthStore } from '@/app/store/auth-store';

interface ChangePasswordModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function ChangePasswordModal({ isOpen, onClose }: ChangePasswordModalProps) {
  const [passwordActual, setPasswordActual] = useState('');
  const [passwordNueva, setPasswordNueva] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const changePasswordMutation = useChangePassword();
  const logout = useAuthStore((state) => state.logout);

  const resetForm = () => {
    setPasswordActual('');
    setPasswordNueva('');
    setPasswordConfirm('');
    setError('');
    setSuccess(false);
  };

  const handleClose = () => {
    resetForm();
    onClose();
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!passwordActual || !passwordNueva || !passwordConfirm) {
      setError('Todos los campos son obligatorios.');
      return;
    }

    if (passwordNueva.length < 8) {
      setError('La nueva contraseña debe tener al menos 8 caracteres.');
      return;
    }

    if (passwordNueva !== passwordConfirm) {
      setError('Las contraseñas nuevas no coinciden.');
      return;
    }

    changePasswordMutation.mutate(
      { password_actual: passwordActual, password_nueva: passwordNueva },
      {
        onSuccess: () => {
          setSuccess(true);
        },
        onError: (err: unknown) => {
          const axiosError = err as { response?: { data?: { message?: string } } };
          setError(axiosError.response?.data?.message ?? 'Error al cambiar la contraseña.');
        },
      },
    );
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="Cambiar contraseña">
      {success ? (
        <div className="space-y-4">
          <div className="text-sm text-green-700 bg-green-50 border border-green-200 rounded-md px-3 py-2">
            Contraseña cambiada exitosamente. Por favor iniciá sesión de nuevo.
          </div>
          <div className="flex justify-end">
            <Button onClick={logout}>Cerrar sesión</Button>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Contraseña actual"
            type="password"
            value={passwordActual}
            onChange={(e) => setPasswordActual(e.target.value)}
            required
            placeholder="••••••••"
          />
          <Input
            label="Nueva contraseña"
            type="password"
            value={passwordNueva}
            onChange={(e) => setPasswordNueva(e.target.value)}
            required
            minLength={8}
            placeholder="••••••••"
          />
          <Input
            label="Confirmar nueva contraseña"
            type="password"
            value={passwordConfirm}
            onChange={(e) => setPasswordConfirm(e.target.value)}
            required
            minLength={8}
            placeholder="••••••••"
          />

          {error && (
            <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2">
              {error}
            </p>
          )}

          <div className="flex justify-end gap-3 pt-2">
            <Button type="button" variant="secondary" onClick={handleClose}>
              Cancelar
            </Button>
            <Button type="submit" isLoading={changePasswordMutation.isPending}>
              Cambiar contraseña
            </Button>
          </div>
        </form>
      )}
    </Modal>
  );
}
