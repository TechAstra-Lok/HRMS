import { apiRequest } from './client.js';

export async function login(email, password) {
  return apiRequest('/api/v1/auth/login', {
    method: 'POST',
    body: { email, password }
  });
}

export async function logout() {
  try {
    await apiRequest('/api/v1/auth/logout', { method: 'POST' });
  } catch (error) {
    console.warn('Logout request failed:', error.message);
  }

  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  localStorage.removeItem('user');
  localStorage.removeItem('tenantId');
}

export function isAuthenticated() {
  return Boolean(localStorage.getItem('accessToken'));
}

export function getCurrentUser() {
  try {
    return JSON.parse(localStorage.getItem('user') || 'null');
  } catch {
    return null;
  }
}

export function saveAuthTokens(data) {
  if (data.access_token) {
    localStorage.setItem('accessToken', data.access_token);
  }

  if (data.refresh_token) {
    localStorage.setItem('refreshToken', data.refresh_token);
  }

  if (data.user) {
    localStorage.setItem('user', JSON.stringify(data.user));
  }

  if (data.tenant_id) {
    localStorage.setItem('tenantId', data.tenant_id);
  }
}
