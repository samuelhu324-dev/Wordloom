import { ReactNode, Suspense } from 'react';
import { ProtectedRoute } from '@/shared/auth';
import { Header } from '@/shared/layouts';

interface WorkboxLayoutProps {
  children: ReactNode;
}

export const dynamic = 'force-dynamic';

export default function WorkboxLayout({ children }: WorkboxLayoutProps) {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Suspense fallback={<div style={{ minHeight: 64 }} />}>
        <Header />
      </Suspense>
      <div style={{ flex: 1 }}>
        <ProtectedRoute>{children}</ProtectedRoute>
      </div>
    </div>
  );
}