import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Button } from '@/shared/ui/button';

describe('Button', () => {
  it('should render with text', () => {
    render(<Button>Iniciar sesión</Button>);
    expect(screen.getByText('Iniciar sesión')).toBeInTheDocument();
  });

  it('should show spinner when loading', () => {
    render(<Button isLoading>Cargando</Button>);
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
    expect(button.querySelector('.animate-spin')).toBeTruthy();
  });

  it('should apply variant classes', () => {
    const { rerender } = render(<Button variant="danger">Eliminar</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-red-600');

    rerender(<Button variant="secondary">Cancelar</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-gray-200');
  });
});
