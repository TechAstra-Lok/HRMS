import { DashboardPage } from './pages/Dashboard.js';
import { EmployeesPage } from './pages/Employees.js';
import { AttendancePage } from './pages/Attendance.js';
import { PayrollPage } from './pages/Payroll.js';
import { RecruitmentPage } from './pages/Recruitment.js';
import { PerformancePage } from './pages/Performance.js';
import { ReportsPage } from './pages/Reports.js';
import { SettingsPage } from './pages/Settings.js';
import { LoginPage } from './pages/Login.js';
import { NotFoundPage } from './pages/NotFound.js';
import { UnauthorizedPage } from './pages/Unauthorized.js';
import { isAuthenticated } from './api/auth.js';

const routes = {
  dashboard: DashboardPage,
  employees: EmployeesPage,
  attendance: AttendancePage,
  payroll: PayrollPage,
  recruitment: RecruitmentPage,
  performance: PerformancePage,
  reports: ReportsPage,
  settings: SettingsPage,
  login: LoginPage,
  unauthorized: UnauthorizedPage,
};

export function initRouter(target) {
  const path = window.location.hash.replace('#', '') || 'dashboard';

  if (!isAuthenticated() && path !== 'login') {
    window.location.hash = 'login';
    return;
  }

  if (isAuthenticated() && path === 'login') {
    window.location.hash = 'dashboard';
    return;
  }

  const Page = routes[path] || NotFoundPage;
  target.innerHTML = Page();
  if (Page.afterRender) {
    Page.afterRender();
  }
}
