import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/shared/hooks/use-auth';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { Card } from '@/shared/ui/card';

interface FieldErrors {
  nombre?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
}

function getFieldErrors(error: unknown): FieldErrors {
  if (!error) return {};
  const axiosError = error as {
    response?: {
      status?: number;
      data?: { message?: string; detail?: Array<{ loc: string[]; msg: string }> };
    };
  };
  const data = axiosError.response?.data;
  const status = axiosError.response?.status;

  if (status === 409) {
    return { email: data?.message ?? 'El email ya está registrado.' };
  }
  if (status === 422 && data?.detail) {
    const errors: FieldErrors = {};
    for (const err of data.detail) {
      const field = err.loc[err.loc.length - 1];
      if (field === 'nombre') errors.nombre = err.msg;
      if (field === 'email') errors.email = err.msg;
      if (field === 'password') errors.password = err.msg;
    }
    return errors;
  }
  return {};
}

function getGeneralError(error: unknown): string {
  if (!error) return '';
  const axiosError = error as { response?: { status?: number; data?: { message?: string } } };
  const status = axiosError.response?.status;
  if (status === 409 || status === 422) return '';
  return axiosError.response?.data?.message ?? 'Error al registrarse. Intentalo de nuevo.';
}

export default function RegisterPage() {
  const navigate = useNavigate();
  const { register, isRegistering, registerError } = useAuth();
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [telefono, setTelefono] = useState('');
  const [clientErrors, setClientErrors] = useState<FieldErrors>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setClientErrors({});

    const errors: FieldErrors = {};
    if (nombre.trim().length < 2) {
      errors.nombre = 'El nombre debe tener al menos 2 caracteres.';
    }
    if (password.length < 8) {
      errors.password = 'La contraseña debe tener al menos 8 caracteres.';
    }
    if (password !== confirmPassword) {
      errors.confirmPassword = 'Las contraseñas no coinciden.';
    }
    if (Object.keys(errors).length > 0) {
      setClientErrors(errors);
      return;
    }

    register(
      { nombre: nombre.trim(), email, password, telefono: telefono || undefined },
      {
        onSuccess: () => navigate('/productos'),
      },
    );
  };

  const serverErrors = getFieldErrors(registerError);
  const generalError = getGeneralError(registerError);

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <Card title="Crear cuenta" className="w-full max-w-md">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Nombre"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
            minLength={2}
            placeholder="Tu nombre"
            error={clientErrors.nombre ?? serverErrors.nombre}
          />
          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="tu@email.com"
            error={serverErrors.email}
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
            minLength={8}
            placeholder="••••••••"
            error={clientErrors.password ?? serverErrors.password}
          />
          <Input
            label="Confirmar contraseña"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            placeholder="••••••••"
            error={clientErrors.confirmPassword}
          />

          {generalError && (
            <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2">
              {generalError}
            </p>
          )}

          <Button type="submit" isLoading={isRegistering} className="w-full">
            Crear cuenta
          </Button>
        </form>

        <div className="mt-4 space-y-2 text-center text-sm text-gray-600">
          <p>
            ¿Ya tenés cuenta?{' '}
            <Link to="/login" className="text-amber-600 hover:text-amber-700 font-medium">
              Iniciá sesión
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
