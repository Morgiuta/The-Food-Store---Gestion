import { Link } from 'react-router-dom';
import { Button } from '@/shared/ui/button';

export default function UnauthorizedPage() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center gap-6 px-4">
      <h1 className="text-8xl font-bold text-amber-500">401</h1>
      <h2 className="text-2xl font-semibold text-gray-800">No has iniciado sesión</h2>
      <p className="text-gray-500 text-center max-w-md">
        Debes iniciar sesión para acceder a esta página.
      </p>
      <Link to="/login">
        <Button>Iniciar sesión</Button>
      </Link>
    </div>
  );
}
