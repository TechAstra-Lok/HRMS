/**
 * Authentication Manager
 */

class AuthManager {
    static async login(email, password) {
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Login failed');
            }
            
            const data = await response.json();
            
            // Store tokens and user data
            localStorage.setItem('accessToken', data.access_token);
            localStorage.setItem('refreshToken', data.refresh_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            localStorage.setItem('tenantId', data.tenant_id);
            
            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }
    
    static async refreshToken() {
        try {
            const refreshToken = localStorage.getItem('refreshToken');
            if (!refreshToken) return false;
            
            const response = await fetch('/api/auth/refresh', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${refreshToken}`
                }
            });
            
            if (!response.ok) {
                localStorage.clear();
                return false;
            }
            
            const data = await response.json();
            localStorage.setItem('accessToken', data.access_token);
            
            return true;
        } catch (error) {
            console.error('Token refresh error:', error);
            return false;
        }
    }
    
    static async logout() {
        try {
            await fetch('/api/auth/logout', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                }
            });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            localStorage.clear();
        }
    }
    
    static async setupMFA(email) {
        try {
            const response = await fetch('/api/auth/mfa/setup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                },
                body: JSON.stringify({ email })
            });
            
            if (!response.ok) throw new Error('MFA setup failed');
            
            return await response.json();
        } catch (error) {
            console.error('MFA setup error:', error);
            throw error;
        }
    }
    
    static async verifyMFA(token, code) {
        try {
            const response = await fetch('/api/auth/mfa/verify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ token, code })
            });
            
            if (!response.ok) throw new Error('MFA verification failed');
            
            const data = await response.json();
            localStorage.setItem('accessToken', data.access_token);
            
            return data;
        } catch (error) {
            console.error('MFA verification error:', error);
            throw error;
        }
    }
    
    static async changePassword(currentPassword, newPassword) {
        try {
            const response = await fetch('/api/auth/change-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                },
                body: JSON.stringify({
                    current_password: currentPassword,
                    new_password: newPassword
                })
            });
            
            if (!response.ok) throw new Error('Password change failed');
            
            return await response.json();
        } catch (error) {
            console.error('Password change error:', error);
            throw error;
        }
    }
}

// Login Form Handler
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const result = await AuthManager.login(email, password);
        AppState.isAuthenticated = true;
        showApp();
        initializeApp();
    } catch (error) {
        alert('Login failed: ' + error.message);
    }
});
