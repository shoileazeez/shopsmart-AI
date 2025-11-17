export interface User {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
}

export interface TokenPair {
    access: string;
    refresh: string;
}

export interface AuthResponse {
    success: boolean;
    message: string;
    user?: User;
    tokens?: TokenPair;
}

export interface LoginCredentials {
    email: string;
    password: string;
}

export interface RegisterCredentials {
    email: string;
    first_name: string;
    last_name: string;
    password: string;
    confirm_password: string;
}

export interface PasswordResetRequest {
    email: string;
}

export interface PasswordResetConfirm {
    email: string;
    code: string;
    new_password: string;
    confirm_new_password: string;
}

export interface ApiError {
    success: false;
    message: string;
    errors?: Record<string, string[]>;
}