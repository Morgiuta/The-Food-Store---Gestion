import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/shared/hooks/use-auth';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { Card } from '@/shared/ui/card';

export default function RegisterPage() {
  const navigate = useNavigate();
  const { register, isRegistering, registerError } = useAuth();
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [telefono, setTelefono] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    register(
      { nombre, email, password, telefono: telefono || undefined },
      {
        onSuccess: () => navigate('/productos'),
      },
    );
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <Card title="Crear cuenta" className="w-full max-w-md">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Nombre"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
            placeholder="Tu nombre"
          />
          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="tu@email.com"
          />
          <Input
            label="Teléfono"
            type="tel"
            value={telefono}
            onChange={(e) => setTelefono(e.target.value)}
            placeholder="+54 11 1234-5678"
          />
          <Input
            label="Contraseña"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder="••••••••"
          />

          {registerError && (
            <p className="text-sm text-red-600">
              {(registerError as { response?: { data?: { message?: string } } })?.response?.data
                ?.message ?? 'Error al registrarse'}
            </p>
          )}

          <Button type="submit" isLoading={isRegistering} className="w-full">
            Crear cuenta
          </Button>
        </form>

        <p className="mt-4 text-center text-sm text-gray-600">
          ¿Ya tenés cuenta?{' '}
          <Link to="/login" className="text-amber-600 hover:text-amber-700 font-medium">
            Iniciá sesión
          </Link>
        </p>
      </Card>
    </div>
  );
}
