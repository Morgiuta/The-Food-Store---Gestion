import { useState, useEffect } from 'react';
import { Modal } from '@/shared/ui/modal';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { useUpdateUsuario } from '../hooks/use-admin-users';
import type { User, Rol } from '@/shared/types';

const ROLES_LIST: Rol[] = ['ADMIN', 'STOCK', 'PEDIDOS', 'CLIENT'];

interface EditUserModalProps {
  user: User;
  isOpen: boolean;
  onClose: () => void;
}

export function EditUserModal({ user, isOpen, onClose }: EditUserModalProps) {
  const [nombre, setNombre] = useState(user.nombre);
  const [email, setEmail] = useState(user.email);
  const [telefono, setTelefono] = useState(user.telefono ?? '');
  const [roles, setRoles] = useState<Rol[]>([...user.roles]);
  const [error, setError] = useState('');

  const updateMutation = useUpdateUsuario();

  useEffect(() => {
    if (isOpen) {
      setNombre(user.nombre);
      setEmail(user.email);
      setTelefono(user.telefono ?? '');
      setRoles([...user.roles]);
      setError('');
    }
  }, [isOpen, user]);

  const toggleRole = (rol: Rol) => {
    setRoles((prev) =>
      prev.includes(rol) ? prev.filter((r) => r !== rol) : [...prev, rol],
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!nombre.trim() || !email.trim()) {
      setError('Nombre y email son obligatorios.');
      return;
    }

    if (roles.length === 0) {
      setError('Debe seleccionar al menos un rol.');
      return;
    }

    updateMutation.mutate(
      { id: user.id, data: { nombre: nombre.trim(), email: email.trim(), telefono: telefono.trim() || null, roles } },
      {
        onSuccess: () => onClose(),
        onError: (err: unknown) => {
          const axiosError = err as { response?: { data?: { message?: string } } };
          setError(axiosError.response?.data?.message ?? 'Error al actualizar el usuario.');
        },
      },
    );
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Editar usuario">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input label="Nombre" value={nombre} onChange={(e) => setNombre(e.target.value)} required />
        <Input label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <Input label="Teléfono" value={telefono} onChange={(e) => setTelefono(e.target.value)} />

        <div className="flex flex-col gap-1">
          <span className="text-sm font-medium text-gray-700">Roles</span>
          <div className="flex flex-wrap gap-3">
            {ROLES_LIST.map((rol) => (
              <label key={rol} className="flex items-center gap-2 text-sm cursor-pointer">
                <input
                  type="checkbox"
                  checked={roles.includes(rol)}
                  onChange={() => toggleRole(rol)}
                  className="rounded border-gray-300 text-amber-500 focus:ring-amber-400"
                />
                {rol}
              </label>
            ))}
          </div>
        </div>

        {error && (
          <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2">
            {error}
          </p>
        )}

        <div className="flex justify-end gap-3 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>
            Cancelar
          </Button>
          <Button type="submit" isLoading={updateMutation.isPending}>
            Guardar cambios
          </Button>
        </div>
      </form>
    </Modal>
  );
}
