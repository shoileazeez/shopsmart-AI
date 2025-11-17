interface TokenResponse {
    access: string;
    refresh: string;
}

interface RefreshError {
    error: string;
    status: number;
}

export async function refreshToken(currentRefreshToken: string): Promise<TokenResponse | RefreshError> {
    try {
        const response = await fetch('http://localhost:8000/api/auth/token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                refresh: currentRefreshToken,
            }),
        });

        if (!response.ok) {
            return {
                error: 'Token refresh failed',
                status: response.status,
            };
        }

        const data = await response.json();
        return data as TokenResponse;
    } catch (error) {
        return {
            error: 'Network error during token refresh',
            status: 0,
        };
    }
}

export function isTokenExpired(token: string): boolean {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const expiryTime = payload.exp * 1000; // Convert to milliseconds
        return Date.now() >= expiryTime;
    } catch {
        return true; // If we can't decode the token, consider it expired
    }
}

export function getTimeUntilExpiry(token: string): number {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const expiryTime = payload.exp * 1000; // Convert to milliseconds
        return Math.max(0, expiryTime - Date.now());
    } catch {
        return 0;
    }
}