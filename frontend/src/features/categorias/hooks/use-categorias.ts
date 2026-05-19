import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';

export interface Categoria {
  id: number;
  nombre: string;
  descripcion?: string;
  imagen_url?: string;
  padre_id?: number | null;
  subcategorias?: Categoria[];
}

export interface CategoriaCreate {
  nombre: string;
  descripcion?: string;
  imagen_url?: string;
  padre_id?: number | null;
}

function sortCategorias(items: Categoria[]) {
  return [...items].sort((a, b) => a.nombre.localeCompare(b.nombre));
}

function removeCategoriaFromTree(items: Categoria[], id: number): Categoria[] {
  return items
    .filter((item) => item.id !== id)
    .map((item) => ({
      ...item,
      subcategorias: item.subcategorias
        ? removeCategoriaFromTree(item.subcategorias, id)
        : undefined,
    }));
}

function insertCategoriaInTree(items: Categoria[], categoria: Categoria): Categoria[] {
  if (categoria.padre_id == null) {
    return sortCategorias([...items, { ...categoria, subcategorias: categoria.subcategorias ?? [] }]);
  }

  return items.map((item) => {
    if (item.id === categoria.padre_id) {
      return {
        ...item,
        subcategorias: sortCategorias([
          ...(item.subcategorias ?? []),
          { ...categoria, subcategorias: categoria.subcategorias ?? [] },
        ]),
      };
    }

    return {
      ...item,
      subcategorias: item.subcategorias
        ? insertCategoriaInTree(item.subcategorias, categoria)
        : item.subcategorias,
    };
  });
}

function upsertCategoriaInTree(items: Categoria[] | undefined, categoria: Categoria) {
  if (!items) return items;
  const withoutCategoria = removeCategoriaFromTree(items, categoria.id);
  return insertCategoriaInTree(withoutCategoria, categoria);
}

export function useCategorias() {
  return useQuery<Categoria[]>({
    queryKey: ['categorias'],
    queryFn: () => apiClient.get(ENDPOINTS.CATEGORIAS.BASE).then(r => r.data),
  });
}

export function useCategoria(id: number) {
  return useQuery<Categoria>({
    queryKey: ['categorias', id],
    queryFn: () => apiClient.get(ENDPOINTS.CATEGORIAS.BY_ID(id)).then(r => r.data),
    enabled: !!id,
  });
}

export function useCreateCategoria() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: CategoriaCreate) =>
      apiClient.post(ENDPOINTS.CATEGORIAS.BASE, data).then(r => r.data),
    onSuccess: (created: Categoria) => {
      qc.setQueryData<Categoria[]>(['categorias'], (old) =>
        upsertCategoriaInTree(old, created),
      );
      qc.invalidateQueries({ queryKey: ['categorias'] });
    },
  });
}

export function useUpdateCategoria() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<CategoriaCreate> }) =>
      apiClient.put(ENDPOINTS.CATEGORIAS.BY_ID(id), data).then(r => r.data),
    onSuccess: (updated: Categoria) => {
      qc.setQueryData<Categoria[]>(['categorias'], (old) =>
        upsertCategoriaInTree(old, updated),
      );
      qc.setQueryData<Categoria>(['categorias', updated.id], updated);
      qc.invalidateQueries({ queryKey: ['categorias'] });
    },
  });
}

export function useDeleteCategoria() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) =>
      apiClient.delete(ENDPOINTS.CATEGORIAS.BY_ID(id)),
    onSuccess: (_response, deletedId) => {
      qc.setQueryData<Categoria[]>(['categorias'], (old) =>
        old ? removeCategoriaFromTree(old, deletedId) : old,
      );
      qc.removeQueries({ queryKey: ['categorias', deletedId] });
      qc.invalidateQueries({ queryKey: ['categorias'] });
    },
  });
}
