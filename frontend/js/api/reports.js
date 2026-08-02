import { apiRequest } from './client.js';

export async function getReportsMetrics() {
  const response = await apiRequest('/api/v1/dashboard/stats', { method: 'GET' });
  return response.data || {};
}
