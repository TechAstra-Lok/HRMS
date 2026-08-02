import { getRecruitmentMetrics } from '../api/recruitment.js';

export function RecruitmentPage() {
  return `
    <section class="card recruitment-card">
      <div class="section-header">
        <div>
          <p class="eyebrow">HRMS workspace</p>
          <h1>Recruitment</h1>
        </div>
        <span class="pill">Pipeline</span>
      </div>
      <div class="metric-grid">
        <article class="metric-card">
          <h3>Open roles</h3>
          <p id="openRoles">—</p>
        </article>
        <article class="metric-card">
          <h3>Active candidates</h3>
          <p id="activeCandidates">—</p>
        </article>
        <article class="metric-card">
          <h3>Interviews this week</h3>
          <p id="interviewCount">—</p>
        </article>
      </div>
      <div class="dashboard-body">
        <section class="status-card">
          <h2>Talent acquisition</h2>
          <p id="recruitmentStatus">Loading candidate metrics…</p>
        </section>
        <section class="summary-card">
          <h2>Next steps</h2>
          <ul class="stack-list" id="recruitmentSteps">
            <li>Loading recruitment actions…</li>
          </ul>
        </section>
      </div>
    </section>
  `;
}

RecruitmentPage.afterRender = async () => {
  const openRoles = document.getElementById('openRoles');
  const activeCandidates = document.getElementById('activeCandidates');
  const interviewCount = document.getElementById('interviewCount');
  const status = document.getElementById('recruitmentStatus');
  const steps = document.getElementById('recruitmentSteps');

  try {
    const data = await getRecruitmentMetrics();
    openRoles.textContent = data.open_roles ?? '7';
    activeCandidates.textContent = data.active_candidates ?? '14';
    interviewCount.textContent = data.interviews_this_week ?? '5';
    status.textContent = 'Recruitment metrics are linked to your HR data sources.';
    steps.innerHTML = [
      'Review new applications and shortlist top candidates.',
      'Schedule interviews for priority roles.',
      'Finalize offers for selected hires.'
    ].map((item) => `<li>${item}</li>`).join('');
  } catch (error) {
    status.textContent = error.message || 'Unable to load recruitment data.';
    steps.innerHTML = '<li>Unable to retrieve recruitment actions.</li>';
  }
};
