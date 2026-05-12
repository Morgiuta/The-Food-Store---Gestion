import { create } from 'zustand';

interface Notification {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
}

interface UIState {
  modals: Record<string, boolean>;
  notifications: Notification[];
  globalLoading: boolean;
  openModal: (key: string) => void;
  closeModal: (key: string) => void;
  addNotification: (notification: Omit<Notification, 'id'>) => void;
  removeNotification: (id: string) => void;
  setGlobalLoading: (loading: boolean) => void;
}

export const useUIStore = create<UIState>()((set) => ({
  modals: {},
  notifications: [],
  globalLoading: false,

  openModal: (key) =>
    set((state) => ({ modals: { ...state.modals, [key]: true } })),

  closeModal: (key) =>
    set((state) => ({ modals: { ...state.modals, [key]: false } })),

  addNotification: (notification) =>
    set((state) => ({
      notifications: [
        ...state.notifications,
        { ...notification, id: crypto.randomUUID() },
      ],
    })),

  removeNotification: (id) =>
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    })),

  setGlobalLoading: (loading) => set({ globalLoading: loading }),
}));
