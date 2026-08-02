export function UnauthorizedPage() {
  return `
    <section class="card">
      <div class="section-header">
        <div>
          <p class="eyebrow">Access denied</p>
          <h1>Unauthorized</h1>
        </div>
      </div>
      <p>You do not have permission to access this resource.</p>
      <p>If you think this is a mistake, sign out and sign back in.</p>
    </section>
  `;
}
