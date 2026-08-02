import { apiRequest } from '../api/client.js';
import { getCurrentUser, isAuthenticated } from '../api/auth.js';

export function SettingsPage() {
  return `
    <section class="card settings-card">
      <div class="section-header">
        <div>
          <p class="eyebrow">HRMS workspace</p>
          <h1>Settings</h1>
        </div>
        <span class="pill">Configuration</span>
      </div>
      <div class="dashboard-body">
        <section class="status-card">
          <h2>User profile</h2>
          <div id="userProfileDetails">Loading current user information…</div>
        </section>
        <section class="summary-card">
          <h2>Security toolbox</h2>
          <ul class="stack-list">
            <li>Manage access and role assignments.</li>
            <li>Review multi-tenant controls.</li>
            <li>Audit authentication and session settings.</li>
          </ul>
        </section>
      </div>
    </section>
  `;
}

SettingsPage.afterRender = async () => {
  const profile = document.getElementById('userProfileDetails');

  try {
    const response = await apiRequest('/api/v1/auth/verify', { method: 'GET' });
    const user = response.data || getCurrentUser() || {};
    profile.innerHTML = `
      <p><strong>Name:</strong> ${user?.first_name || user?.name || 'N/A'} ${user?.last_name || ''}</p>
      <p><strong>User ID:</strong> ${user?.user_id || 'N/A'}</p>
      <p><strong>Tenant ID:</strong> ${user?.tenant_id || 'N/A'}</p>
      <p><strong>Roles:</strong> ${(user?.roles || []).join(', ') || 'N/A'}</p>
      ${isAuthenticated() ? '<p>Authentication status: connected</p>' : '<p>Authentication status: guest</p>'}
    `;
  } catch (error) {
    const user = getCurrentUser() || {};
    profile.innerHTML = `
      <p><strong>Name:</strong> ${user?.first_name || user?.name || 'N/A'} ${user?.last_name || ''}</p>
      <p><strong>User ID:</strong> ${user?.user_id || 'N/A'}</p>
      <p><strong>Tenant ID:</strong> ${user?.tenant_id || 'N/A'}</p>
      <p><strong>Roles:</strong> ${(user?.roles || []).join(', ') || 'N/A'}</p>
      <p class="form-error">${error.message || 'Unable to verify user session.'}</p>
    `;
  }
};
