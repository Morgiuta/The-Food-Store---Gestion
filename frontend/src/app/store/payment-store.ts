import { create } from 'zustand';

type PaymentStatus = 'idle' | 'processing' | 'approved' | 'rejected' | 'error';

interface PaymentState {
  status: PaymentStatus;
  paymentId: string | null;
  error: string | null;
  setStatus: (status: PaymentStatus) => void;
  setPaymentId: (id: string) => void;
  setError: (error: string) => void;
  reset: () => void;
}

const initialState = {
  status: 'idle' as PaymentStatus,
  paymentId: null as string | null,
  error: null as string | null,
};

export const usePaymentStore = create<PaymentState>()((set) => ({
  ...initialState,

  setStatus: (status) => set({ status }),

  setPaymentId: (paymentId) => set({ paymentId }),

  setError: (error) => set({ error, status: 'error' }),

  reset: () => set(initialState),
}));
