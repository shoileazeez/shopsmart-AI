import { useState } from 'react';
import { useAuth } from '../components/ui/themeProvider';
import { AuthService } from '../utils/auth.service';
import { 
    LoginCredentials, 
    RegisterCredentials, 
    PasswordResetRequest, 
    PasswordResetConfirm 
} from '../types/auth.types';

export function useAuthActions() {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const { login: setAuth, logout: clearAuth } = useAuth();

    const register = async (credentials: RegisterCredentials) => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await AuthService.register(credentials);
            if (response.success && response.tokens && response.user) {
                setAuth(response.tokens, response.user);
                return response;
            }
            setError(response.message);
            return response;
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Registration failed';
            setError(message);
            return { success: false, message };
        } finally {
            setIsLoading(false);
        }
    };

    const login = async (credentials: LoginCredentials) => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await AuthService.login(credentials);
            if (response.success && response.tokens && response.user) {
                setAuth(response.tokens, response.user);
                return response;
            }
            setError(response.message);
            return response;
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Login failed';
            setError(message);
            return { success: false, message };
        } finally {
            setIsLoading(false);
        }
    };

    const logout = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await AuthService.logout();
            if (response.success) {
                clearAuth();
            }
            return response;
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Logout failed';
            setError(message);
            return { success: false, message };
        } finally {
            setIsLoading(false);
        }
    };

    const requestPasswordReset = async (data: PasswordResetRequest) => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await AuthService.requestPasswordReset(data);
            if (!response.success) {
                setError(response.message);
            }
            return response;
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Password reset request failed';
            setError(message);
            return { success: false, message };
        } finally {
            setIsLoading(false);
        }
    };

    const resendResetCode = async (data: PasswordResetRequest) => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await AuthService.resendResetCode(data);
            if (!response.success) {
                setError(response.message);
            }
            return response;
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Resend code request failed';
            setError(message);
            return { success: false, message };
        } finally {
            setIsLoading(false);
        }
    };

    const resetPassword = async (data: PasswordResetConfirm) => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await AuthService.resetPassword(data);
            if (!response.success) {
                setError(response.message);
            }
            return response;
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Password reset failed';
            setError(message);
            return { success: false, message };
        } finally {
            setIsLoading(false);
        }
    };

    return {
        register,
        login,
        logout,
        requestPasswordReset,
        resendResetCode,
        resetPassword,
        isLoading,
        error
    };
}