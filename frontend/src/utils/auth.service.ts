import apiClient from './apiClient';
import { 
    AuthResponse, 
    LoginCredentials, 
    RegisterCredentials, 
    PasswordResetRequest, 
    PasswordResetConfirm,
    User,
    TokenPair
} from '../types/auth.types';

export class AuthService {
    static async register(credentials: RegisterCredentials): Promise<AuthResponse> {
        try {
            const response = await apiClient.post<AuthResponse>('/auth/user/register/', credentials);
            if (response.data.success && response.data.tokens && response.data.user) {
                this.setAuthData(response.data.tokens, response.data.user);
            }
            return response.data;
        } catch (error: any) {
            return this.handleError(error);
        }
    }

    static async login(credentials: LoginCredentials): Promise<AuthResponse> {
        try {
            const response = await apiClient.post<AuthResponse>('/auth/user/login/', credentials);
            if (response.data.success && response.data.tokens && response.data.user) {
                this.setAuthData(response.data.tokens, response.data.user);
            }
            return response.data;
        } catch (error: any) {
            return this.handleError(error);
        }
    }

    static async logout(): Promise<AuthResponse> {
        try {
            const tokens = this.getTokens();
            if (!tokens?.refresh) {
                throw new Error('No refresh token found');
            }

            const response = await apiClient.post<AuthResponse>('/auth/user/logout/', {
                refresh: tokens.refresh
            });

            if (response.data.success) {
                this.clearAuthData();
            }
            return response.data;
        } catch (error: any) {
            this.clearAuthData(); // Clear auth data even if the request fails
            return this.handleError(error);
        }
    }

    static async requestPasswordReset(data: PasswordResetRequest): Promise<AuthResponse> {
        try {
            const response = await apiClient.post<AuthResponse>('/auth/password-reset/', data);
            return response.data;
        } catch (error: any) {
            return this.handleError(error);
        }
    }

    static async resendResetCode(data: PasswordResetRequest): Promise<AuthResponse> {
        try {
            const response = await apiClient.post<AuthResponse>('/auth/password-reset/resend/', data);
            return response.data;
        } catch (error: any) {
            return this.handleError(error);
        }
    }

    static async resetPassword(data: PasswordResetConfirm): Promise<AuthResponse> {
        try {
            const response = await apiClient.post<AuthResponse>('/auth/password-reset/confirm/', data);
            return response.data;
        } catch (error: any) {
            return this.handleError(error);
        }
    }

    static async refreshToken(refreshToken: string): Promise<AuthResponse> {
        try {
            const response = await apiClient.post<AuthResponse>('/auth/token/refresh/', {
                refresh: refreshToken
            });
            
            if (response.data.success && response.data.tokens) {
                this.updateTokens(response.data.tokens);
            }
            return response.data;
        } catch (error: any) {
            return this.handleError(error);
        }
    }

    // Helper methods
    private static setAuthData(tokens: TokenPair, user: User): void {
        localStorage.setItem('tokens', JSON.stringify(tokens));
        localStorage.setItem('user', JSON.stringify(user));
    }

    private static updateTokens(tokens: TokenPair): void {
        const storedTokens = this.getTokens();
        const newTokens = { ...storedTokens, ...tokens };
        localStorage.setItem('tokens', JSON.stringify(newTokens));
    }

    private static getTokens(): TokenPair | null {
        const tokens = localStorage.getItem('tokens');
        return tokens ? JSON.parse(tokens) : null;
    }

    private static clearAuthData(): void {
        localStorage.removeItem('tokens');
        localStorage.removeItem('user');
    }

    private static handleError(error: any): AuthResponse {
        if (error.response?.data) {
            return {
                success: false,
                message: error.response.data.message || 'An error occurred',
                ...error.response.data
            };
        }
        return {
            success: false,
            message: error.message || 'Network error occurred'
        };
    }
}