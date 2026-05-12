import { useState, useEffect } from 'react';
import { useCatalogo, useSearchProductos } from '@/features/productos/hooks/use-catalogo';
import { useCategorias } from '@/features/categorias/hooks/use-categorias';
import { Spinner } from '@/shared/ui/spinner';
import { Input } from '@/shared/ui/input';
import type { Categoria as CategoriaHook } from '@/features/categorias/hooks/use-categorias';

function useDebounce<T>(value: T, delay: number = 300): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debounced;
}

export default function CatalogPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [precioMin, setPrecioMin] = useState('');
  const [precioMax, setPrecioMax] = useState('');
  const [categoriaId, setCategoriaId] = useState<number | undefined>(undefined);
  const [expandedProducto, setExpandedProducto] = useState<number | null>(null);

  const debouncedQ = useDebounce(searchQuery, 400);
  const isSearching = !!debouncedQ || !!precioMin || !!precioMax;

  const searchResult = useSearchProductos({
    q: debouncedQ || undefined,
    precio_min: precioMin ? Number(precioMin) : undefined,
    precio_max: precioMax ? Number(precioMax) : undefined,
    categoria_id: isSearching ? categoriaId : undefined,
  });

  const catalogResult = useCatalogo(
    !isSearching && categoriaId ? { categoria_id: categoriaId } : undefined,
  );

  const { data: productos, isLoading, isError, error } = isSearching
    ? searchResult
    : catalogResult;

  const { data: categorias } = useCategorias();

  const toggleExpand = (id: number) => {
    setExpandedProducto((prev) => (prev === id ? null : id));
  };

  const flatCategorias = categorias ? flattenTree(categorias) : [];

  const hasAnyFilter = !!searchQuery || !!precioMin || !!precioMax || !!categoriaId;

  const handleClearFilters = () => {
    setSearchQuery('');
    setPrecioMin('');
    setPrecioMax('');
    setCategoriaId(undefined);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-2">Catálogo de productos</h1>
      <p className="text-gray-500 mb-6">Explorá todos nuestros productos disponibles</p>

      {/* Search + price filters */}
      <div className="flex flex-wrap items-end gap-4 mb-6">
        <div className="flex-1 min-w-[200px]">
          <Input
            placeholder="Buscar productos..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="w-32">
          <Input
            placeholder="Precio min"
            type="number"
            min={0}
            value={precioMin}
            onChange={(e) => setPrecioMin(e.target.value)}
          />
        </div>
        <div className="w-32">
          <Input
            placeholder="Precio max"
            type="number"
            min={0}
            value={precioMax}
            onChange={(e) => setPrecioMax(e.target.value)}
          />
        </div>
        {hasAnyFilter && (
          <button
            type="button"
            onClick={handleClearFilters}
            className="px-3 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
          >
            Limpiar filtros
          </button>
        )}
      </div>

      {/* Category pills */}
      <div className="flex flex-wrap items-center gap-2 mb-8">
        <button
          type="button"
          onClick={() => setCategoriaId(undefined)}
          className={`px-3 py-1.5 text-sm rounded-full border transition-colors ${
            categoriaId === undefined
              ? 'bg-amber-500 text-white border-amber-500'
              : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
          }`}
        >
          Todas
        </button>
        {flatCategorias.map((cat) => (
          <button
            key={cat.id}
            type="button"
            onClick={() => setCategoriaId(cat.id)}
            className={`px-3 py-1.5 text-sm rounded-full border transition-colors ${
              categoriaId === cat.id
                ? 'bg-amber-500 text-white border-amber-500'
                : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
            }`}
          >
            {cat.nombre}
          </button>
        ))}
      </div>

      {isLoading && (
        <div className="flex justify-center py-20">
          <Spinner size="lg" />
        </div>
      )}

      {isError && (
        <div className="text-center py-20">
          <p className="text-red-600 mb-2">Error al cargar los productos.</p>
          <p className="text-sm text-gray-500">
            {(error as { message?: string })?.message ?? 'Intentalo de nuevo más tarde.'}
          </p>
        </div>
      )}

      {!isLoading && !isError && (!productos || productos.length === 0) && (
        <div className="text-center py-20">
          <p className="text-gray-500 text-lg mb-1">
            {isSearching
              ? 'No se encontraron productos con esos filtros.'
              : categoriaId
              ? 'No hay productos en esta categoría.'
              : 'No hay productos disponibles.'}
          </p>
          <p className="text-sm text-gray-400">
            {isSearching
              ? 'Probá con otros términos o ajustá los filtros.'
              : categoriaId
              ? 'Elegí otra categoría para explorar.'
              : 'Volvé más tarde para ver novedades.'}
          </p>
        </div>
      )}

      {!isLoading && !isError && productos && productos.length > 0 && (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {productos.map((prod) => (
            <div
              key={prod.id}
              className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
            >
              <div className="aspect-video bg-gray-100 flex items-center justify-center text-gray-400 text-sm">
                {prod.imagen_url ? (
                  <img
                    src={prod.imagen_url}
                    alt={prod.nombre}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                )}
              </div>

              <div className="p-4 space-y-2">
                <h3 className="font-semibold text-gray-800 truncate">{prod.nombre}</h3>

                <p className="text-lg font-bold text-amber-600">
                  ${Number(prod.precio).toFixed(2)}
                </p>

                <div className="flex items-center gap-2">
                  {prod.stock_cantidad > 0 ? (
                    <span className="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-full bg-green-100 text-green-700">
                      En stock
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-full bg-red-100 text-red-700">
                      Sin stock
                    </span>
                  )}
                  {!prod.disponible && (
                    <span className="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-full bg-gray-100 text-gray-600">
                      No disponible
                    </span>
                  )}
                </div>

                {prod.categorias && prod.categorias.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {prod.categorias.map((cat) => (
                      <span
                        key={cat.id}
                        className="px-2 py-0.5 text-xs rounded-full bg-amber-50 text-amber-700 border border-amber-200"
                      >
                        {cat.nombre}
                      </span>
                    ))}
                  </div>
                )}

                <button
                  type="button"
                  onClick={() => toggleExpand(prod.id)}
                  className="text-sm text-amber-600 hover:text-amber-700 font-medium"
                >
                  {expandedProducto === prod.id ? 'Ver menos' : 'Ver detalles'}
                </button>

                {expandedProducto === prod.id && (
                  <div className="pt-2 border-t border-gray-100 space-y-2">
                    {prod.descripcion && (
                      <p className="text-sm text-gray-600">{prod.descripcion}</p>
                    )}
                    {prod.ingredientes && prod.ingredientes.length > 0 && (
                      <div>
                        <p className="text-xs font-medium text-gray-500 mb-1">Ingredientes:</p>
                        <div className="flex flex-wrap gap-1">
                          {prod.ingredientes.map((ing) => (
                            <span
                              key={ing.id}
                              className={`px-2 py-0.5 text-xs rounded-full ${
                                ing.es_alergeno
                                  ? 'bg-red-50 text-red-700 border border-red-200'
                                  : 'bg-gray-50 text-gray-600 border border-gray-200'
                              }`}
                            >
                              {ing.nombre}
                              {ing.es_alergeno && ' ⚠'}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

interface FlatCategoria {
  id: number;
  nombre: string;
  depth: number;
}

function flattenTree(list: CategoriaHook[], depth = 0): FlatCategoria[] {
  const result: FlatCategoria[] = [];
  for (const cat of list) {
    result.push({ id: cat.id, nombre: cat.nombre, depth });
    const children = cat.subcategorias ?? [];
    if (children.length > 0) {
      result.push(...flattenTree(children, depth + 1));
    }
  }
  return result;
}
