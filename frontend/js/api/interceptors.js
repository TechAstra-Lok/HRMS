import { config } from '../config.js';

export const apiRequest = async (path, options = {}) => {
  const url = `${config.apiBaseUrl}${path}`;
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    ...options.headers,
  };
  const response = await fetch(url, {
    ...options,
    credentials: 'include',
    headers,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Network error' }));
    throw new Error(error.message || 'Request failed');
  }
  return response.json();
};
