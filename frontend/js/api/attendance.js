import { apiRequest } from './client.js';

export async function checkIn(employeeId) {
  return apiRequest('/api/v1/attendance/check-in', {
    method: 'POST',
    body: { employee_id: employeeId }
  });
}

export async function checkOut(employeeId) {
  return apiRequest('/api/v1/attendance/check-out', {
    method: 'POST',
    body: { employee_id: employeeId }
  });
}
