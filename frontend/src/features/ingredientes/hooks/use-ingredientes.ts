import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';

export interface Ingrediente {
  id: number;
  nombre: string;
  descripcion?: string;
  es_alergeno: boolean;
}

export interface IngredienteCreate {
  nombre: string;
  descripcion?: string;
  es_alergeno?: boolean;
}

interface IngredientesParams {
  es_alergeno?: boolean;
}

function sortIngredientes(items: Ingrediente[]) {
  return [...items].sort((a, b) => a.nombre.localeCompare(b.nombre));
}

function upsertIngrediente(items: Ingrediente[] | undefined, ingrediente: Ingrediente) {
  if (!items) return items;
  const exists = items.some((item) => item.id === ingrediente.id);
  const next = exists
    ? items.map((item) => (item.id === ingrediente.id ? ingrediente : item))
    : [...items, ingrediente];
  return sortIngredientes(next);
}

export function useIngredientes(params?: IngredientesParams) {
  return useQuery<Ingrediente[]>({
    queryKey: ['ingredientes', params],
    queryFn: () =>
      apiClient
        .get(ENDPOINTS.INGREDIENTES.BASE, { params })
        .then((r) => r.data),
  });
}

export function useCreateIngrediente() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: IngredienteCreate) =>
      apiClient.post(ENDPOINTS.INGREDIENTES.BASE, data).then((r) => r.data),
    onSuccess: (created: Ingrediente) => {
      qc.setQueryData<Ingrediente[]>(['ingredientes', undefined], (old) =>
        upsertIngrediente(old, created),
      );
      if (created.es_alergeno) {
        qc.setQueryData<Ingrediente[]>(['ingredientes', { es_alergeno: true }], (old) =>
          upsertIngrediente(old, created),
        );
      }
      qc.invalidateQueries({ queryKey: ['ingredientes'] });
    },
  });
}

export function useUpdateIngrediente() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<IngredienteCreate> }) =>
      apiClient.put(ENDPOINTS.INGREDIENTES.BY_ID(id), data).then((r) => r.data),
    onSuccess: (updated: Ingrediente) => {
      qc.setQueryData<Ingrediente[]>(['ingredientes', undefined], (old) =>
        upsertIngrediente(old, updated),
      );
      qc.setQueryData<Ingrediente[]>(['ingredientes', { es_alergeno: true }], (old) => {
        if (!old) return old;
        if (updated.es_alergeno) return upsertIngrediente(old, updated);
        return old.filter((item) => item.id !== updated.id);
      });
      qc.invalidateQueries({ queryKey: ['ingredientes'] });
    },
  });
}

export function useDeleteIngrediente() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) =>
      apiClient.delete(ENDPOINTS.INGREDIENTES.BY_ID(id)),
    onSuccess: (_response, deletedId) => {
      qc.setQueryData<Ingrediente[]>(['ingredientes', undefined], (old) =>
        old?.filter((item) => item.id !== deletedId),
      );
      qc.setQueryData<Ingrediente[]>(['ingredientes', { es_alergeno: true }], (old) =>
        old?.filter((item) => item.id !== deletedId),
      );
      qc.invalidateQueries({ queryKey: ['ingredientes'] });
    },
  });
}
