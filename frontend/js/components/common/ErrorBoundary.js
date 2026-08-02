export function ErrorBoundary(message = 'Something went wrong') {
  return `
    <div class="error-boundary">
      <h2>Error</h2>
      <p>${message}</p>
    </div>
  `;
}
