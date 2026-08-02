import { apiRequest } from './client.js';

export async function getPayrollSummary() {
  const response = await apiRequest('/api/v1/payroll/summary', { method: 'GET' });
  return response || { netPay: 0 };
}

export async function calculatePayroll(data = {}) {
  const response = await apiRequest('/api/v1/payroll/calculate', {
    method: 'POST',
    body: data
  });
  return response;
}
