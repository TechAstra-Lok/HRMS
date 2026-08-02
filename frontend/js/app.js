import { Layout } from './components/common/Layout.js';
import { initRouter } from './routes.js';
import { protect, sanitize } from './security/protection.js';
import { isAuthenticated, logout, getCurrentUser } from './api/auth.js';
import './config.js';

const navItems = [
  { title: 'Dashboard', route: 'dashboard' },
  { title: 'Employees', route: 'employees' },
  { title: 'Attendance', route: 'attendance' },
  { title: 'Payroll', route: 'payroll' },
  { title: 'Recruitment', route: 'recruitment' },
  { title: 'Performance', route: 'performance' },
  { title: 'Reports', route: 'reports' },
  { title: 'Settings', route: 'settings' }
];

function buildNav(navElement) {
  if (!isAuthenticated()) {
    navElement.innerHTML = '';
    navElement.style.display = 'none';
    return;
  }

  navElement.style.display = 'flex';
  const currentHash = window.location.hash.replace('#', '') || 'dashboard';
  navElement.innerHTML = navItems
    .map(
      (item) => `
        <button class="${item.route === currentHash ? 'active' : ''}" data-route="${item.route}">
          ${sanitize(item.title)}
        </button>`
    )
    .join('');

  navElement.querySelectorAll('button').forEach((button) => {
    button.addEventListener('click', () => {
      navElement.querySelectorAll('button').forEach((b) => b.classList.remove('active'));
      button.classList.add('active');
      window.location.hash = button.dataset.route;
      initRouter(document.getElementById('page'));
    });
  });
}

function updateHeader(headerElement) {
  const user = getCurrentUser();
  if (!user) {
    headerElement.innerHTML = `
      <div class="header-actions__item">
        <button class="secondary-button" data-route="login">Sign in</button>
      </div>
    `;
    headerElement.querySelector('button[data-route]')?.addEventListener('click', () => {
      window.location.hash = 'login';
    });
    return;
  }

  headerElement.innerHTML = `
    <div class="user-chip">
      <span>${sanitize(user.first_name || user.email || 'User')}</span>
      <button id="logoutButton" class="link-button">Sign out</button>
    </div>
  `;
  document.getElementById('logoutButton')?.addEventListener('click', async () => {
    await logout();
    buildNav(document.getElementById('nav'));
    updateHeader(document.getElementById('headerActions'));
    window.location.hash = 'login';
    initRouter(document.getElementById('page'));
  });
}

window.addEventListener('DOMContentLoaded', () => {
  protect();
  const app = document.getElementById('app');
  app.innerHTML = Layout();

  const nav = document.getElementById('nav');
  const headerActions = document.getElementById('headerActions');

  buildNav(nav);
  updateHeader(headerActions);

  window.addEventListener('hashchange', () => {
    buildNav(nav);
    updateHeader(headerActions);
    initRouter(document.getElementById('page'));
  });

  initRouter(document.getElementById('page'));
});
