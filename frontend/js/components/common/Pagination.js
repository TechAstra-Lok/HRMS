export function Pagination({ currentPage = 1, totalPages = 1 } = {}) {
  const pages = Array.from({ length: totalPages }, (_, index) => index + 1);
  return `
    <div class="pagination">
      ${pages
        .map(
          (page) => `<button class="pagination-button ${page === currentPage ? 'active' : ''}" data-page="${page}">${page}</button>`
        )
        .join('')}
    </div>
  `;
}
