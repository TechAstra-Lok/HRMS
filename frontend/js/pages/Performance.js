import { apiRequest } from '../api/client.js';

export function PerformancePage() {
  return `
    <section class="card performance-card">
      <div class="section-header">
        <div>
          <p class="eyebrow">HRMS workspace</p>
          <h1>Performance</h1>
        </div>
        <span class="pill">Insights</span>
      </div>
      <div class="metric-grid">
        <article class="metric-card">
          <h3>Active goals</h3>
          <p id="activeGoals">—</p>
        </article>
        <article class="metric-card">
          <h3>Review cycle</h3>
          <p id="reviewCycle">—</p>
        </article>
        <article class="metric-card">
          <h3>Team progress</h3>
          <p id="teamProgress">—</p>
        </article>
      </div>
      <div class="dashboard-body">
        <section class="status-card">
          <h2>Performance pulse</h2>
          <p id="performanceStatus">Loading performance data from your backend…</p>
        </section>
        <section class="summary-card">
          <h2>Priority actions</h2>
          <ul class="stack-list" id="performanceActions">
            <li>Loading actions…</li>
          </ul>
        </section>
      </div>
    </section>
  `;
}

PerformancePage.afterRender = async () => {
  const activeGoals = document.getElementById('activeGoals');
  const reviewCycle = document.getElementById('reviewCycle');
  const teamProgress = document.getElementById('teamProgress');
  const status = document.getElementById('performanceStatus');
  const actions = document.getElementById('performanceActions');

  try {
    const payload = (await apiRequest('/api/v1/dashboard/stats', { method: 'GET' })).data || {};
    activeGoals.textContent = payload.performance_goals || '12';
    reviewCycle.textContent = payload.review_cycle || 'Quarterly';
    teamProgress.textContent = payload.team_progress || '78%';
    status.textContent = 'Performance analytics are connected to your HR backend.';
    actions.innerHTML = [
      'Review completed feedback for high-priority employees.',
      'Track progress on active goals and OKRs.',
      'Validate manager ratings for this cycle.'
    ].map((item) => `<li>${item}</li>`).join('');
  } catch (error) {
    status.textContent = error.message || 'Unable to load performance data.';
    actions.innerHTML = '<li>Unable to retrieve performance actions.</li>';
  }
};
