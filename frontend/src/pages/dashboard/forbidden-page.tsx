import { Link } from 'react-router-dom';
import { Button } from '@/shared/ui/button';

export default function ForbiddenPage() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center gap-6 px-4">
      <h1 className="text-8xl font-bold text-amber-500">403</h1>
      <h2 className="text-2xl font-semibold text-gray-800">Acceso denegado</h2>
      <p className="text-gray-500 text-center max-w-md">
        No tienes permisos suficientes para acceder a esta página.
      </p>
      <Link to="/">
        <Button>Volver al inicio</Button>
      </Link>
    </div>
  );
}
