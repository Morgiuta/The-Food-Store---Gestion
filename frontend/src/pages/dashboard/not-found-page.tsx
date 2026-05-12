import { Link } from 'react-router-dom';
import { Button } from '@/shared/ui/button';

export default function NotFoundPage() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center gap-6 px-4">
      <h1 className="text-8xl font-bold text-amber-500">404</h1>
      <h2 className="text-2xl font-semibold text-gray-800">Página no encontrada</h2>
      <p className="text-gray-500 text-center max-w-md">
        La página que estás buscando no existe o ha sido movida.
      </p>
      <Link to="/">
        <Button>Volver al inicio</Button>
      </Link>
    </div>
  );
}
