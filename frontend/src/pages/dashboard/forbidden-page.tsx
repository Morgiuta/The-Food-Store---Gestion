import { Link } from 'react-router-dom';
import { Button } from '@/shared/ui/button';

export default function ForbiddenPage() {
  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center text-center px-4">
      <h1 className="text-6xl font-bold text-gray-300 mb-4">403</h1>
      <h2 className="text-2xl font-semibold text-gray-700 mb-2">Acceso denegado</h2>
      <p className="text-gray-500 mb-8 max-w-md">
        No tenés permisos suficientes para acceder a esta página.
      </p>
      <Link to="/">
        <Button variant="primary">Volver al inicio</Button>
      </Link>
    </div>
  );
}
