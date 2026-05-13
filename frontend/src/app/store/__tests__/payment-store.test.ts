import { describe, it, expect, beforeEach } from 'vitest';
import { usePaymentStore } from '@/app/store/payment-store';

describe('paymentStore', () => {
  beforeEach(() => {
    usePaymentStore.getState().reset();
  });

  it('should start with idle status', () => {
    const state = usePaymentStore.getState();
    expect(state.status).toBe('idle');
    expect(state.paymentId).toBeNull();
    expect(state.error).toBeNull();
  });

  it('should set status to processing', () => {
    usePaymentStore.getState().setStatus('processing');
    expect(usePaymentStore.getState().status).toBe('processing');
  });

  it('should set payment id', () => {
    usePaymentStore.getState().setPaymentId('mp_123');
    expect(usePaymentStore.getState().paymentId).toBe('mp_123');
  });

  it('should set error and change status to error', () => {
    usePaymentStore.getState().setError('Payment failed');
    expect(usePaymentStore.getState().status).toBe('error');
    expect(usePaymentStore.getState().error).toBe('Payment failed');
  });

  it('should reset to initial state', () => {
    usePaymentStore.getState().setStatus('approved');
    usePaymentStore.getState().setPaymentId('mp_456');
    usePaymentStore.getState().reset();
    expect(usePaymentStore.getState().status).toBe('idle');
    expect(usePaymentStore.getState().paymentId).toBeNull();
    expect(usePaymentStore.getState().error).toBeNull();
  });
});
