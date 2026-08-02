export function Modal(title, content) {
  return `
    <div class="modal-backdrop">
      <div class="modal-card">
        <header>
          <h2>${title}</h2>
        </header>
        <div class="modal-content">${content}</div>
      </div>
    </div>
  `;
}
