import { FC } from 'react';
import { Outlet } from 'react-router-dom';
import { NavBar } from '@/components/shared/Navbar';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '@/config/reactQueryConfig';

export const RootLayout: FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="flex min-h-screen flex-col">
        <NavBar />
        <div className="m-6 grow">
          <Outlet></Outlet>
        </div>
      </div>
    </QueryClientProvider>
  );
};
