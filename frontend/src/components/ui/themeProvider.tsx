'use client';

import React, { createContext, useContext, useEffect, useState, useCallback, useRef } from 'react';
import { ThemeProvider as NextThemesProvider } from 'next-themes';
import contentConfig from '../content.config';
import { NavItem } from '../content.config';
import { refreshToken, isTokenExpired, getTimeUntilExpiry } from '../../utils/auth';

interface TokenPair {
  access: string;
  refresh: string;
}

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  navigation: NavItem[];
  user: UserType | null;
  login: (tokens: TokenPair, user: UserType) => void;
  logout: () => void;
  getAccessToken: () => string | null;
}

interface UserType {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
}

interface ThemeProviderProps {
  children: React.ReactNode;
}

const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  isLoading: true,
  navigation: [],
  user: null,
  login: () => {},
  logout: () => {},
  getAccessToken: () => null,
});

export const useAuth = () => useContext(AuthContext);

export function ThemeProvider({ children }: ThemeProviderProps) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<UserType | null>(null);
  const [navigation, setNavigation] = useState<NavItem[]>(contentConfig.publicHeader.navigation);
  const refreshTimeoutRef = useRef<NodeJS.Timeout | undefined>(undefined);
  const tokenRef = useRef<TokenPair | undefined>(undefined);

  // Check authentication status on mount
  useEffect(() => {
    const checkAuth = () => {
      setIsLoading(true);
      const storedTokens = localStorage.getItem('tokens');
      const storedUser = localStorage.getItem('user');

      if (storedTokens && storedUser) {
        try {
          const tokens: TokenPair = JSON.parse(storedTokens);
          const parsedUser = JSON.parse(storedUser);

          if (isTokenExpired(tokens.access)) {
            // Try to refresh the token immediately
            refreshToken(tokens.refresh).then((result) => {
              if ('access' in result) {
                tokenRef.current = result;
                localStorage.setItem('tokens', JSON.stringify(result));
                setUser(parsedUser);
                setIsAuthenticated(true);
                setNavigation(contentConfig.privateHeader.navigation);
                setupRefreshTimer(result.access);
              } else {
                handleLogout();
              }
              setIsLoading(false);
            });
          } else {
            tokenRef.current = tokens;
            setUser(parsedUser);
            setIsAuthenticated(true);
            setNavigation(contentConfig.privateHeader.navigation);
            setupRefreshTimer(tokens.access);
            setIsLoading(false);
          }
        } catch (error) {
          console.error('Error parsing stored data:', error);
          handleLogout();
          setIsLoading(false);
        }
      } else {
        handleLogout();
        setIsLoading(false);
      }
    };

    checkAuth();
    // Listen for storage events to sync across tabs
    window.addEventListener('storage', checkAuth);
    return () => window.removeEventListener('storage', checkAuth);
  }, []);

  const setupRefreshTimer = useCallback((token: string) => {
    // Clear any existing refresh timer
    if (refreshTimeoutRef.current) {
      clearTimeout(refreshTimeoutRef.current);
    }

    // Get time until token expires
    const timeUntilExpiry = getTimeUntilExpiry(token);
    
    // Set refresh to occur at 90% of token lifetime
    const refreshTime = timeUntilExpiry * 0.9;
    
    refreshTimeoutRef.current = setTimeout(async () => {
      const currentRefreshToken = tokenRef.current?.refresh;
      if (currentRefreshToken) {
        const result = await refreshToken(currentRefreshToken);
        if ('access' in result) {
          // Success - update tokens
          tokenRef.current = result;
          localStorage.setItem('tokens', JSON.stringify(result));
          setupRefreshTimer(result.access);
        } else {
          // Error - log out
          handleLogout();
        }
      }
    }, refreshTime);
  }, []);

  const handleLogin = (tokens: TokenPair, userData: UserType) => {
    localStorage.setItem('tokens', JSON.stringify(tokens));
    localStorage.setItem('user', JSON.stringify(userData));
    tokenRef.current = tokens;
    setUser(userData);
    setIsAuthenticated(true);
    setNavigation(contentConfig.privateHeader.navigation);
    setupRefreshTimer(tokens.access);
  };

  const handleLogout = () => {
    localStorage.removeItem('tokens');
    localStorage.removeItem('user');
    if (refreshTimeoutRef.current) {
      clearTimeout(refreshTimeoutRef.current);
    }
    tokenRef.current = undefined;
    setUser(null);
    setIsAuthenticated(false);
    setNavigation(contentConfig.publicHeader.navigation);
  };

  const getAccessToken = useCallback(() => {
    return tokenRef.current?.access || null;
  }, []);

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        isLoading,
        navigation,
        user,
        login: handleLogin,
        logout: handleLogout,
        getAccessToken,
      }}
    >
      <NextThemesProvider
        attribute="class"
        defaultTheme="system"
        enableSystem
        disableTransitionOnChange
      >
        {children}
      </NextThemesProvider>
    </AuthContext.Provider>
  );
}

export default ThemeProvider;