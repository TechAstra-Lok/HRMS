import { getReportsMetrics } from '../api/reports.js';

export function ReportsPage() {
  return `
    <section class="card reports-card">
      <div class="section-header">
        <div>
          <p class="eyebrow">HRMS workspace</p>
          <h1>Reports</h1>
        </div>
        <span class="pill">Data</span>
      </div>
      <div class="metric-grid">
        <article class="metric-card">
          <h3>Live exports</h3>
          <p id="liveExports">—</p>
        </article>
        <article class="metric-card">
          <h3>Open dashboards</h3>
          <p id="openDashboards">—</p>
        </article>
        <article class="metric-card">
          <h3>Audit-ready</h3>
          <p id="auditReady">—</p>
        </article>
      </div>
      <div class="dashboard-body">
        <section class="status-card">
          <h2>Reporting engine</h2>
          <p id="reportsStatus">Loading report availability…</p>
        </section>
        <section class="summary-card">
          <h2>Common reports</h2>
          <ul class="stack-list" id="reportsList">
            <li>Loading reports…</li>
          </ul>
        </section>
      </div>
    </section>
  `;
}

ReportsPage.afterRender = async () => {
  const liveExports = document.getElementById('liveExports');
  const openDashboards = document.getElementById('openDashboards');
  const auditReady = document.getElementById('auditReady');
  const status = document.getElementById('reportsStatus');
  const list = document.getElementById('reportsList');

  try {
    const data = await getReportsMetrics();
    liveExports.textContent = data.reports_export_count ?? '3';
    openDashboards.textContent = data.dashboard_count ?? '4';
    auditReady.textContent = data.audit_ready ? 'Yes' : 'No';
    status.textContent = 'Reporting modules are powered by backend data.';
    list.innerHTML = [
      'Employee overview',
      'Attendance trends',
      'Payroll summaries',
      'Compliance audit logs'
    ].map((item) => `<li>${item}</li>`).join('');
  } catch (error) {
    status.textContent = error.message || 'Unable to load report availability.';
    list.innerHTML = '<li>Unable to retrieve report options.</li>';
  }
};
