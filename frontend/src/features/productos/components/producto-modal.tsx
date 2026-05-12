import { useState, useEffect } from 'react';
import { Modal } from '@/shared/ui/modal';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { useCategorias } from '@/features/categorias/hooks/use-categorias';
import { useIngredientes } from '@/features/ingredientes/hooks/use-ingredientes';
import { useCreateProducto, useUpdateProducto } from '../hooks/use-productos';
import type { Product } from '@/shared/types';
import type { ProductCreate } from '../hooks/use-productos';
import type { Categoria as CategoriaHook } from '@/features/categorias/hooks/use-categorias';

interface ProductoModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  producto?: Product | null;
}

export function ProductoModal({ isOpen, onClose, onSuccess, producto }: ProductoModalProps) {
  const [nombre, setNombre] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [precio, setPrecio] = useState('');
  const [stockCantidad, setStockCantidad] = useState('');
  const [disponible, setDisponible] = useState(true);
  const [selectedCategorias, setSelectedCategorias] = useState<number[]>([]);
  const [selectedIngredientes, setSelectedIngredientes] = useState<number[]>([]);
  const [error, setError] = useState('');

  const createMutation = useCreateProducto();
  const updateMutation = useUpdateProducto();
  const { data: categorias } = useCategorias();
  const { data: ingredientes } = useIngredientes();
  const isEdit = !!producto;
  const isPending = createMutation.isPending || updateMutation.isPending;

  useEffect(() => {
    if (isOpen) {
      setNombre(producto?.nombre ?? '');
      setDescripcion(producto?.descripcion ?? '');
      setPrecio(producto?.precio ? String(producto.precio) : '');
      setStockCantidad(producto?.stock_cantidad != null ? String(producto.stock_cantidad) : '0');
      setDisponible(producto?.disponible ?? true);
      setSelectedCategorias(producto?.categorias?.map((c) => c.id) ?? []);
      setSelectedIngredientes(producto?.ingredientes?.map((i) => i.id) ?? []);
      setError('');
    }
  }, [isOpen, producto]);

  const toggleCategoria = (id: number) => {
    setSelectedCategorias((prev) =>
      prev.includes(id) ? prev.filter((v) => v !== id) : [...prev, id],
    );
  };

  const toggleIngrediente = (id: number) => {
    setSelectedIngredientes((prev) =>
      prev.includes(id) ? prev.filter((v) => v !== id) : [...prev, id],
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const trimmedNombre = nombre.trim();
    if (!trimmedNombre) {
      setError('El nombre es obligatorio.');
      return;
    }

    const precioNum = parseFloat(precio);
    if (isNaN(precioNum) || precioNum <= 0) {
      setError('El precio debe ser un número mayor a 0.');
      return;
    }

    const stockNum = parseInt(stockCantidad, 10);
    if (isNaN(stockNum) || stockNum < 0) {
      setError('El stock debe ser un número mayor o igual a 0.');
      return;
    }

    const payload: ProductCreate = {
      nombre: trimmedNombre,
      descripcion: descripcion.trim() || undefined,
      precio: precioNum,
      stock_cantidad: stockNum,
      disponible,
      categoria_ids: selectedCategorias.length > 0 ? selectedCategorias : undefined,
      ingrediente_ids: selectedIngredientes.length > 0 ? selectedIngredientes : undefined,
    };

    if (isEdit && producto) {
      updateMutation.mutate(
        { id: producto.id, data: payload },
        { onSuccess: () => { onSuccess(); onClose(); }, onError: handleError },
      );
    } else {
      createMutation.mutate(payload, {
        onSuccess: () => { onSuccess(); onClose(); },
        onError: handleError,
      });
    }
  };

  const handleError = (err: unknown) => {
    const axiosError = err as { response?: { data?: { message?: string } } };
    setError(axiosError.response?.data?.message ?? 'Ocurrió un error al guardar el producto.');
  };

  const flatCategorias = flattenCategorias(categorias ?? []);

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={isEdit ? 'Editar producto' : 'Nuevo producto'}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Nombre"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          maxLength={200}
          required
        />

        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-gray-700">Descripción</label>
          <textarea
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
            rows={3}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-400 transition-colors resize-none"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <Input
            label="Precio"
            type="number"
            step="0.01"
            min="0.01"
            value={precio}
            onChange={(e) => setPrecio(e.target.value)}
            required
          />
          <Input
            label="Stock"
            type="number"
            min="0"
            value={stockCantidad}
            onChange={(e) => setStockCantidad(e.target.value)}
            required
          />
        </div>

        <label className="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={disponible}
            onChange={(e) => setDisponible(e.target.checked)}
            className="w-4 h-4 rounded border-gray-300 text-amber-500 focus:ring-amber-400"
          />
          <span className="text-sm font-medium text-gray-700">Producto disponible</span>
        </label>

        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-gray-700">Categorías</label>
          <div className="max-h-40 overflow-y-auto border border-gray-200 rounded-md p-2 space-y-1">
            {flatCategorias.length === 0 && (
              <p className="text-xs text-gray-400">No hay categorías disponibles.</p>
            )}
            {flatCategorias.map((cat) => (
              <label
                key={cat.id}
                className="flex items-center gap-2 cursor-pointer hover:bg-gray-50 rounded px-1 py-0.5"
              >
                <input
                  type="checkbox"
                  checked={selectedCategorias.includes(cat.id)}
                  onChange={() => toggleCategoria(cat.id)}
                  className="w-4 h-4 rounded border-gray-300 text-amber-500 focus:ring-amber-400"
                />
                <span className="text-sm text-gray-700" style={{ marginLeft: `${cat.depth * 16}px` }}>
                  {cat.nombre}
                </span>
              </label>
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-gray-700">Ingredientes</label>
          <div className="max-h-40 overflow-y-auto border border-gray-200 rounded-md p-2 space-y-1">
            {(!ingredientes || ingredientes.length === 0) && (
              <p className="text-xs text-gray-400">No hay ingredientes disponibles.</p>
            )}
            {ingredientes?.map((ing) => (
              <label
                key={ing.id}
                className="flex items-center gap-2 cursor-pointer hover:bg-gray-50 rounded px-1 py-0.5"
              >
                <input
                  type="checkbox"
                  checked={selectedIngredientes.includes(ing.id)}
                  onChange={() => toggleIngrediente(ing.id)}
                  className="w-4 h-4 rounded border-gray-300 text-amber-500 focus:ring-amber-400"
                />
                <span className={`text-sm ${ing.es_alergeno ? 'text-red-700 font-medium' : 'text-gray-700'}`}>
                  {ing.nombre}
                  {ing.es_alergeno && (
                    <span className="ml-1.5 text-xs font-medium text-red-500">(alérgeno)</span>
                  )}
                </span>
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
          <Button type="submit" isLoading={isPending}>
            {isEdit ? 'Guardar cambios' : 'Crear producto'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}

interface FlatCategoria {
  id: number;
  nombre: string;
  depth: number;
}

function flattenCategorias(list: CategoriaHook[], depth = 0): FlatCategoria[] {
  const result: FlatCategoria[] = [];
  for (const cat of list) {
    result.push({ id: cat.id, nombre: cat.nombre, depth });
    const children = cat.subcategorias ?? [];
    if (children.length > 0) {
      result.push(...flattenCategorias(children, depth + 1));
    }
  }
  return result;
}
