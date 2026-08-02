import { apiRequest } from '../api/client.js';

export function PayrollPage() {
  return `
    <section class="card payroll-card">
      <div class="section-header">
        <div>
          <p class="eyebrow">HRMS workspace</p>
          <h1>Payroll</h1>
        </div>
        <span class="pill">Action required</span>
      </div>
      <div class="payroll-panel">
        <p>Trigger payroll processing for the active pay period.</p>
        <button id="runPayrollButton" class="primary-button">Run payroll calculation</button>
        <p id="payrollStatus">Payroll processing will use the latest employee and attendance data.</p>
      </div>
    </section>
  `;
}

PayrollPage.afterRender = () => {
  const status = document.getElementById('payrollStatus');
  const button = document.getElementById('runPayrollButton');

  button?.addEventListener('click', async () => {
    button.disabled = true;
    button.textContent = 'Calculating…';
    status.textContent = 'Payroll calculation in progress.';

    try {
      const result = await apiRequest('/api/v1/payroll/calculate', { method: 'POST', body: {} });
      status.textContent = `Payroll process started: ${result?.data?.status || 'pending'}`;
    } catch (error) {
      status.textContent = `Payroll request failed: ${error.message}`;
    } finally {
      button.disabled = false;
      button.textContent = 'Run payroll calculation';
    }
  });
};
