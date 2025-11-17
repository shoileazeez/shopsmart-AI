import axios, { InternalAxiosRequestConfig } from 'axios';

const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add request interceptor
interface Tokens {
    access: string;
    refresh?: string;
    [key: string]: any;
}

// Use axios' InternalAxiosRequestConfig so headers typing is compatible with axios' definitions
type RequestConfig = InternalAxiosRequestConfig & {
    _retry?: boolean;
    [key: string]: any;
};

apiClient.interceptors.request.use(
    (config: RequestConfig) => {
        // Try to get the token from localStorage
        const tokensStr = localStorage.getItem('tokens');
        if (tokensStr) {
            try {
                const tokens: Tokens = JSON.parse(tokensStr);
                config.headers!.Authorization = `Bearer ${tokens.access}`;
            } catch (err: unknown) {
                console.error('Error parsing tokens:', err);
            }
        }
        return config;
    },
    (error: unknown) => {
        return Promise.reject(error);
    }
);

// Define interface for refresh token response
interface RefreshTokensResponse {
    success: boolean;
    message: string;
    tokens: {
        access: string;
        refresh: string;
    };
}

// Local interface for typing the error response
interface AxiosLikeError {
    response?: { status?: number; [key: string]: any };
    config: RequestConfig & {
        headers?: { Authorization?: string | null; [key: string]: any };
        _retry?: boolean;
        [key: string]: any;
    };
    [key: string]: any;
}

// Add response interceptor
apiClient.interceptors.response.use(
    (response: any) => response,
    async (error: unknown) => {
        const err = error as AxiosLikeError;
        const originalRequest = err.config;

        // If the error is 401 and we haven't tried to refresh yet
        if (err.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const tokensStr = localStorage.getItem('tokens');
                if (tokensStr) {
                    const tokens = JSON.parse(tokensStr) as Tokens;
                    const response = await axios.post<RefreshTokensResponse>('http://localhost:8000/api/token/refresh/', {
                        refresh: tokens.refresh
                    });

                    if (response.data.success) {
                        const newTokens: Tokens = {
                            access: response.data.tokens.access,
                            refresh: response.data.tokens.refresh
                        };
                        localStorage.setItem('tokens', JSON.stringify(newTokens));

                        // Retry the original request with the new token
                        originalRequest.headers = originalRequest.headers ?? {};
                        originalRequest.headers.Authorization = `Bearer ${newTokens.access}`;
                        return apiClient(originalRequest);
                    } else {
                        // If token refresh was not successful, redirect to login
                        localStorage.removeItem('tokens');
                        localStorage.removeItem('user');
                        window.location.href = '/login';
                        return Promise.reject(new Error(response.data.message));
                    }
                }
            } catch (refreshError) {
                // If refresh fails, redirect to login
                localStorage.removeItem('tokens');
                localStorage.removeItem('user');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default apiClient;