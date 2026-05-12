import { BrowserRouter } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '@/app/providers/query-provider';
import { AppRouter } from '@/app/providers/router';
import { NotificationDisplay } from '@/shared/ui/notification-display';

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <NotificationDisplay />
        <AppRouter />
      </BrowserRouter>
    </QueryClientProvider>
  );
}
