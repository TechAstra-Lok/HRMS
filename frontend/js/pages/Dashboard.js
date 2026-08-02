import { apiRequest } from '../api/client.js';

export function DashboardPage() {
  return `
    <section class="card dashboard-card">
      <div class="section-header">
        <div>
          <p class="eyebrow">HRMS workspace</p>
          <h1>Dashboard</h1>
        </div>
        <span class="pill">Live summary</span>
      </div>
      <div class="dashboard-grid">
        <article class="metric-card">
          <h3>Total employees</h3>
          <p id="totalEmployees">—</p>
        </article>
        <article class="metric-card">
          <h3>Today attendance</h3>
          <p id="todayAttendance">—</p>
        </article>
        <article class="metric-card">
          <h3>Monthly payroll</h3>
          <p id="monthlyPayroll">—</p>
        </article>
      </div>
      <div class="dashboard-body">
        <section class="status-card">
          <h2>Operational status</h2>
          <p id="dashboardStatus">Loading the latest HR system health information…</p>
        </section>
        <section class="summary-card">
          <h2>Insights</h2>
          <ul class="stack-list" id="dashboardInsights">
            <li>Loading insights…</li>
          </ul>
        </section>
      </div>
    </section>
  `;
}

DashboardPage.afterRender = async () => {
  const statusLabel = document.getElementById('dashboardStatus');
  const insightsList = document.getElementById('dashboardInsights');

  try {
    const data = await apiRequest('/api/v1/dashboard/stats', { method: 'GET' });
    const payload = data?.data || {};

    document.getElementById('totalEmployees').textContent = payload.total_employees ?? '0';
    document.getElementById('todayAttendance').textContent = payload.today_attendance ?? '0';
    document.getElementById('monthlyPayroll').textContent = payload.monthly_payroll ? `$${payload.monthly_payroll.toLocaleString()}` : '$0';

    statusLabel.textContent = 'Live HR insights are connected to your backend service.';

    const insights = [
      `Current attendance rate: ${payload.attendance_rate ?? 'N/A'}%`,
      `Open tasks: ${payload.pending_tasks ?? 'N/A'}`,
      `Latest update: ${payload.updated_at ? new Date(payload.updated_at).toLocaleString() : 'Now'}`
    ];

    insightsList.innerHTML = insights.map((item) => `<li>${item}</li>`).join('');
  } catch (error) {
    statusLabel.textContent = error.message || 'Unable to load dashboard data.';
    insightsList.innerHTML = '<li>Unable to retrieve live insights. Check your backend connection.</li>';
  }
};
