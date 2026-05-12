import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/shared/hooks/use-auth';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { Card } from '@/shared/ui/card';

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
            placeholder="••••••••"
          />

          {loginError && (
            <p className="text-sm text-red-600">
              {(loginError as { response?: { data?: { message?: string } } })?.response?.data
                ?.message ?? 'Error al iniciar sesión'}
            </p>
          )}

          <Button type="submit" isLoading={isLoggingIn} className="w-full">
            Iniciar sesión
          </Button>
        </form>

        <p className="mt-4 text-center text-sm text-gray-600">
          ¿No tenés cuenta?{' '}
          <Link to="/register" className="text-amber-600 hover:text-amber-700 font-medium">
            Registrate
          </Link>
        </p>
      </Card>
    </div>
  );
}
