import { apiRequest } from './client.js';

export async function getEmployees() {
  const response = await apiRequest('/api/v1/employees', { method: 'GET' });
  return Array.isArray(response?.employees) ? response.employees : [];
}
