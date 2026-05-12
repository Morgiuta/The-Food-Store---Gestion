import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { Textarea } from '@/shared/ui/textarea';

const direccionSchema = z.object({
  calle: z.string().min(1, 'La calle es requerida'),
  numero: z.string().min(1, 'El número es requerido'),
  piso: z.string().optional(),
  departamento: z.string().optional(),
  ciudad: z.string().min(1, 'La ciudad es requerida'),
  codigo_postal: z.string().min(1, 'El código postal es requerido'),
  referencia: z.string().optional(),
});

type DireccionFormData = z.infer<typeof direccionSchema>;

interface AddressFormProps {
  onSubmit: (data: DireccionFormData) => void;
  onCancel: () => void;
  isLoading?: boolean;
  initialData?: DireccionFormData;
}

export function AddressForm({
  onSubmit,
  onCancel,
  isLoading,
  initialData,
}: AddressFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<DireccionFormData>({
    resolver: zodResolver(direccionSchema),
    defaultValues: initialData || {
      calle: '',
      numero: '',
      piso: '',
      departamento: '',
      ciudad: '',
      codigo_postal: '',
      referencia: '',
    },
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="col-span-2">
          <label className="block text-sm font-medium mb-1">Calle</label>
          <Input {...register('calle')} placeholder="Av. principal" />
          {errors.calle && (
            <p className="text-sm text-red-600 mt-1">{errors.calle.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Número</label>
          <Input {...register('numero')} placeholder="123" />
          {errors.numero && (
            <p className="text-sm text-red-600 mt-1">{errors.numero.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Piso</label>
          <Input {...register('piso')} placeholder="Opcional" />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Departamento</label>
          <Input {...register('departamento')} placeholder="Opcional" />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Código Postal</label>
          <Input {...register('codigo_postal')} placeholder="1000" />
          {errors.codigo_postal && (
            <p className="text-sm text-red-600 mt-1">
              {errors.codigo_postal.message}
            </p>
          )}
        </div>

        <div className="col-span-2">
          <label className="block text-sm font-medium mb-1">Ciudad</label>
          <Input {...register('ciudad')} placeholder="Buenos Aires" />
          {errors.ciudad && (
            <p className="text-sm text-red-600 mt-1">{errors.ciudad.message}</p>
          )}
        </div>

        <div className="col-span-2">
          <label className="block text-sm font-medium mb-1">
            Referencia (opcional)
          </label>
          <Textarea
            {...register('referencia')}
            placeholder="Entre calles, punto de referencia, etc."
            rows={2}
          />
        </div>
      </div>

      <div className="flex justify-end gap-2 pt-4">
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancelar
        </Button>
        <Button type="submit" disabled={isLoading}>
          {isLoading ? 'Guardando...' : initialData ? 'Actualizar' : 'Crear'}
        </Button>
      </div>
    </form>
  );
}