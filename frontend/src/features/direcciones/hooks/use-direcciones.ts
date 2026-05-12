import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/shared/api/client';
import { ENDPOINTS } from '@/shared/api/endpoints';

export interface Direccion {
  id: number;
  usuario_id: number;
  calle: string;
  numero: string;
  piso?: string;
  departamento?: string;
  ciudad: string;
  codigo_postal: string;
  referencia?: string;
  es_predeterminada: boolean;
  creado_en: string;
  actualizado_en: string;
}

export interface DireccionCreate {
  calle: string;
  numero: string;
  piso?: string;
  departamento?: string;
  ciudad: string;
  codigo_postal: string;
  referencia?: string;
}

export interface DireccionUpdate extends Partial<DireccionCreate> {}

export function useDirecciones() {
  return useQuery<Direccion[]>({
    queryKey: ['direcciones'],
    queryFn: () =>
      apiClient.get(ENDPOINTS.DIRECCIONES.BASE).then((r) => r.data),
  });
}

export function useDireccion(id: number) {
  return useQuery<Direccion>({
    queryKey: ['direcciones', id],
    queryFn: () =>
      apiClient.get(ENDPOINTS.DIRECCIONES.BY_ID(id)).then((r) => r.data),
    enabled: !!id,
  });
}

export function useCreateDireccion() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: DireccionCreate) =>
      apiClient.post(ENDPOINTS.DIRECCIONES.BASE, data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['direcciones'] }),
  });
}

export function useUpdateDireccion() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: DireccionUpdate }) =>
      apiClient.put(ENDPOINTS.DIRECCIONES.BY_ID(id), data).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['direcciones'] }),
  });
}

export function useDeleteDireccion() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) =>
      apiClient.delete(ENDPOINTS.DIRECCIONES.BY_ID(id)),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['direcciones'] }),
  });
}

export function useSetPredeterminada() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) =>
      apiClient
        .post(ENDPOINTS.DIRECCIONES.SET_DEFAULT(id))
        .then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['direcciones'] }),
  });
}