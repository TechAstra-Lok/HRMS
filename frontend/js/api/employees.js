import { apiRequest } from './client.js';

export async function getEmployees() {
  const response = await apiRequest('/api/v1/employees', { method: 'GET' });
  return response.employees || [];
}
