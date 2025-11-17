'use client';

import { useAuth } from '../ui/themeProvider';
import { useRouter, usePathname } from 'next/navigation';
import { useEffect } from 'react';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!isAuthenticated) {
      // Store the attempted URL to redirect back after login
      localStorage.setItem('redirectAfterLogin', pathname);
      router.push('/login');
    }
  }, [isAuthenticated, router, pathname]);

  // Show loading or nothing while checking auth
  if (!isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}