import { Link } from 'react-router-dom';
import { Button } from '@/shared/ui/button';

export default function NotFoundPage() {
  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center text-center px-4">
      <h1 className="text-6xl font-bold text-gray-300 mb-4">404</h1>
      <h2 className="text-2xl font-semibold text-gray-700 mb-2">Página no encontrada</h2>
      <p className="text-gray-500 mb-8 max-w-md">
        La página que estás buscando no existe o fue movida.
      </p>
      <Link to="/">
        <Button variant="primary">Volver al inicio</Button>
      </Link>
    </div>
  );
}
