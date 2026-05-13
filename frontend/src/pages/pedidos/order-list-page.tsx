import { useState } from 'react';
import { useMisPedidos } from '@/features/pedidos/hooks/useOrders';
import { OrderCard } from '@/features/pedidos/components/order-card';
import { OrderDetailModal } from '@/features/pedidos/components/order-detail-modal';
import { Button } from '@/shared/ui/button';
import { Spinner } from '@/shared/ui/spinner';

export default function OrderListPage() {
  const [page, setPage] = useState(1);
  const [selectedOrderId, setSelectedOrderId] = useState<number | null>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const { data, isLoading, error } = useMisPedidos(page);

  const handleViewDetail = (id: number) => {
    setSelectedOrderId(id);
    setModalOpen(true);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Mis Pedidos</h1>

      {isLoading && (
        <div className="flex justify-center py-12">
          <Spinner size="lg" />
        </div>
      )}

      {error && (
        <div className="text-center py-12 text-red-500">
          Error al cargar los pedidos. Intenta de nuevo más tarde.
        </div>
      )}

      {data && data.items.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          <p className="text-lg mb-2">No tenés pedidos todavía</p>
          <p className="text-sm">Explorá el catálogo y hacé tu primer pedido</p>
        </div>
      )}

      {data && data.items.length > 0 && (
        <>
          <div className="grid gap-4 md:grid-cols-2">
            {data.items.map((order) => (
              <OrderCard
                key={order.id}
                order={order}
                onViewDetail={handleViewDetail}
              />
            ))}
          </div>

          {/* Pagination */}
          {data.pages > 1 && (
            <div className="flex items-center justify-center gap-2 mt-8">
              <Button
                variant="outline"
                size="sm"
                disabled={page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
              >
                Anterior
              </Button>
              <span className="text-sm text-gray-600">
                Página {data.page} de {data.pages}
              </span>
              <Button
                variant="outline"
                size="sm"
                disabled={page >= data.pages}
                onClick={() => setPage((p) => p + 1)}
              >
                Siguiente
              </Button>
            </div>
          )}
        </>
      )}

      <OrderDetailModal
        pedidoId={selectedOrderId}
        isOpen={modalOpen}
        onClose={() => {
          setModalOpen(false);
          setSelectedOrderId(null);
        }}
      />
    </div>
  );
}
