import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/shared/hooks/use-auth';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { Card } from '@/shared/ui/card';

function getErrorMessage(error: unknown): string {
  if (!error) return '';
  const axiosError = error as { response?: { status?: number; data?: { message?: string } } };
  const status = axiosError.response?.status;
  const message = axiosError.response?.data?.message;

  if (status === 429) {
    return 'Demasiados intentos. Intentalo de nuevo en unos minutos.';
  }
  if (status === 401) {
    return 'Email o contraseña incorrectos.';
  }
  return message ?? 'Error al iniciar sesión. Intentalo de nuevo.';
}

export default function LoginPage() {
  const navigate = useNavigate();
  const { login, isLoggingIn, loginError } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login(
      { email, password },
      {
        onSuccess: () => navigate('/productos'),
      },
    );
  };

  const errorMessage = getErrorMessage(loginError);

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <Card title="Iniciar sesión" className="w-full max-w-md">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="tu@email.com"
          />
          <Input
            label="Contraseña"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            placeholder="••••••••"
          />

          {errorMessage && (
            <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2">
              {errorMessage}
            </p>
          )}

          <Button type="submit" isLoading={isLoggingIn} className="w-full">
            Iniciar sesión
          </Button>
        </form>

        <div className="mt-4 space-y-2 text-center text-sm text-gray-600">
          <p>
            ¿No tenés cuenta?{' '}
            <Link to="/register" className="text-amber-600 hover:text-amber-700 font-medium">
              Registrate
            </Link>
          </p>
          <p>
            <Link to="/productos" className="text-gray-500 hover:text-gray-700">
              Volver al inicio
            </Link>
          </p>
        </div>
      </Card>
    </div>
  );
}
