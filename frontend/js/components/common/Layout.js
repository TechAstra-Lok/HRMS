export function Layout() {
  return `
    <div class="shell">
      <header class="app-header">
        <div class="brand">
          <span class="brand-mark">HRMS</span>
          <div>
            <h1>Enterprise HRMS</h1>
            <p>People operations, payroll, performance and reporting in one place.</p>
          </div>
        </div>
        <div id="headerActions" class="header-actions"></div>
      </header>
      <nav class="nav" id="nav"></nav>
      <main id="page" class="page-content"></main>
    </div>
  `;
}
