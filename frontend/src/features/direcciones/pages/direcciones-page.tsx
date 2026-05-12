import { useState } from 'react';
import { Plus } from 'lucide-react';
import { Button } from '@/shared/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/shared/ui/dialog';
import { AddressCard } from '../components/address-card';
import {
  AddressForm,
  type DireccionFormData,
} from '../components/address-form';
import {
  useDirecciones,
  useCreateDireccion,
  useUpdateDireccion,
  useDeleteDireccion,
  useSetPredeterminada,
  type Direccion,
} from '../hooks/use-direcciones';
import { Spinner } from '@/shared/ui/spinner';

export default function DireccionesPage() {
  const { data: direcciones, isLoading } = useDirecciones();
  const createMutation = useCreateDireccion();
  const updateMutation = useUpdateDireccion();
  const deleteMutation = useDeleteDireccion();
  const setDefaultMutation = useSetPredeterminada();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingDireccion, setEditingDireccion] = useState<Direccion | null>(null);
  const [deleteConfirmId, setDeleteConfirmId] = useState<number | null>(null);

  const handleCreate = async (data: DireccionFormData) => {
    await createMutation.mutateAsync(data);
    setIsModalOpen(false);
  };

  const handleUpdate = async (data: DireccionFormData) => {
    if (!editingDireccion) return;
    await updateMutation.mutateAsync({ id: editingDireccion.id, data });
    setEditingDireccion(null);
    setIsModalOpen(false);
  };

  const handleDelete = async (id: number) => {
    await deleteMutation.mutateAsync(id);
    setDeleteConfirmId(null);
  };

  const handleSetDefault = async (id: number) => {
    await setDefaultMutation.mutateAsync(id);
  };

  const openCreateModal = () => {
    setEditingDireccion(null);
    setIsModalOpen(true);
  };

  const openEditModal = (direccion: Direccion) => {
    setEditingDireccion(direccion);
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setEditingDireccion(null);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto py-8 px-4">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Mis Direcciones</h1>
          <p className="text-gray-600 mt-1">
            Gestiona tus direcciones de entrega
          </p>
        </div>
        <Button onClick={openCreateModal}>
          <Plus className="w-4 h-4 mr-2" />
          Agregar dirección
        </Button>
      </div>

      {(!direcciones || direcciones.length === 0) ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <p className="text-gray-500 mb-4">No tienes direcciones guardadas</p>
          <Button onClick={openCreateModal}>
            <Plus className="w-4 h-4 mr-2" />
            Agregar tu primera dirección
          </Button>
        </div>
      ) : (
        <div className="space-y-4">
          {direcciones.map((direccion) => (
            <AddressCard
              key={direccion.id}
              direccion={direccion}
              onEdit={openEditModal}
              onDelete={(id) => setDeleteConfirmId(id)}
              onSetDefault={handleSetDefault}
              isDeleting={deleteMutation.isPending && deleteConfirmId === direccion.id}
              isSettingDefault={setDefaultMutation.isPending}
            />
          ))}
        </div>
      )}

      {/* Modal de create/edit */}
      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {editingDireccion ? 'Editar Dirección' : 'Nueva Dirección'}
            </DialogTitle>
          </DialogHeader>
          <AddressForm
            onSubmit={editingDireccion ? handleUpdate : handleCreate}
            onCancel={handleModalClose}
            isLoading={createMutation.isPending || updateMutation.isPending}
            initialData={
              editingDireccion
                ? {
                    calle: editingDireccion.calle,
                    numero: editingDireccion.numero,
                    piso: editingDireccion.piso,
                    departamento: editingDireccion.departamento,
                    ciudad: editingDireccion.ciudad,
                    codigo_postal: editingDireccion.codigo_postal,
                    referencia: editingDireccion.referencia,
                  }
                : undefined
            }
          />
        </DialogContent>
      </Dialog>

      {/* Modal de confirmación de eliminación */}
      <Dialog open={deleteConfirmId !== null} onOpenChange={() => setDeleteConfirmId(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Eliminar Dirección</DialogTitle>
          </DialogHeader>
          <p className="text-gray-600">
            ¿Estás seguro de que deseas eliminar esta dirección? Esta acción no se
            puede deshacer.
          </p>
          <div className="flex justify-end gap-2 mt-4">
            <Button variant="outline" onClick={() => setDeleteConfirmId(null)}>
              Cancelar
            </Button>
            <Button
              variant="destructive"
              onClick={() => deleteConfirmId && handleDelete(deleteConfirmId)}
              disabled={deleteMutation.isPending}
            >
              {deleteMutation.isPending ? 'Eliminando...' : 'Eliminar'}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}