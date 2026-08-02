export function Toast(message, type = 'info') {
  return `
    <div class="toast toast-${type}">
      ${message}
    </div>
  `;
}
