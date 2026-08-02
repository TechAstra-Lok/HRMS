export function Loading({ message = 'Loading…' } = {}) {
  return `
    <div class="loading-card">
      <span class="loading-spinner"></span>
      <span>${message}</span>
    </div>
  `;
}
