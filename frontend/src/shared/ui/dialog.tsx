import type { ReactNode } from 'react';

interface DialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  children: ReactNode;
}

interface DialogContentProps {
  children: ReactNode;
  className?: string;
}

interface DialogTextProps {
  children: ReactNode;
  className?: string;
}

export function Dialog({ open, onOpenChange, children }: DialogProps) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center px-4">
      <button
        type="button"
        aria-label="Cerrar"
        className="absolute inset-0 bg-black/50"
        onClick={() => onOpenChange(false)}
      />
      {children}
    </div>
  );
}

export function DialogContent({ children, className = '' }: DialogContentProps) {
  return (
    <div
      role="dialog"
      aria-modal="true"
      className={`relative z-10 w-full max-w-lg rounded-lg bg-white p-6 shadow-xl ${className}`}
    >
      {children}
    </div>
  );
}

export function DialogHeader({ children, className = '' }: DialogTextProps) {
  return <div className={`mb-4 space-y-1 ${className}`}>{children}</div>;
}

export function DialogTitle({ children, className = '' }: DialogTextProps) {
  return <h2 className={`text-lg font-semibold text-gray-900 ${className}`}>{children}</h2>;
}

export function DialogDescription({ children, className = '' }: DialogTextProps) {
  return <p className={`text-sm text-gray-600 ${className}`}>{children}</p>;
}
