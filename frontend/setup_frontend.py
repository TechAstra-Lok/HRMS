from pathlib import Path
import shutil
import textwrap

root = Path(r'd:/Project/HRMS System/frontend')
root.mkdir(parents=True, exist_ok=True)

# Remove old Vite/React-style folders if they exist.
for rel in ['src', 'tsconfig.json', 'tailwind.config.js']:
    path = root / rel
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()

# Create directories.
paths = [
    'css', 'js/api', 'js/components/common', 'js/components/dashboard', 'js/components/3d',
    'js/components/employees', 'js/components/attendance', 'js/components/payroll',
    'js/components/recruitment', 'js/components/performance', 'js/components/reports',
    'js/components/administration', 'js/components/employee-self-service', 'js/components/chat',
    'js/hooks', 'js/context', 'js/store/slices', 'js/utils', 'js/pages', 'public', 'tests/unit',
    'tests/integration', 'tests/e2e'
]
for p in paths:
    target = root / p
    if target.exists() and not target.is_dir():
        target.unlink()
    target.mkdir(parents=True, exist_ok=True)


def write(path_str, content):
    path = root / path_str
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + '\n', encoding='utf-8')

write('index.html', '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Enterprise HRMS</title>
    <link rel="stylesheet" href="/css/style.css" />
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/js/app.js"></script>
  </body>
</html>
''')

write('package.json', '''
{
  "name": "enterprise-hrms-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "vite": "^5.4.10"
  }
}
''')

write('vite.config.js', '''
import { defineConfig } from 'vite';

export default defineConfig({
  server: { port: 3000, open: false },
  preview: { port: 4173 }
});
''')

write('.env.example', '''
VITE_API_BASE_URL=http://localhost:5000
VITE_WS_URL=ws://localhost:5000
''')

write('.eslintrc.js', '''
module.exports = {
  env: { browser: true, es2021: true },
  extends: ['eslint:recommended'],
  parserOptions: { ecmaVersion: 2021, sourceType: 'module' }
};
''')

write('.prettierrc', '''
{
  "singleQuote": true,
  "semi": true,
  "trailingComma": "es5"
}
''')

write('README.md', '''
# Enterprise HRMS Frontend

This frontend scaffold provides a modular JavaScript structure for the HRMS experience, including authentication, dashboard, employee, attendance, payroll, recruitment, reporting, administration, and employee self-service modules.
''')

css_files = {
    'css/style.css': '''
    :root { color-scheme: dark; --bg: #07111f; --panel: #0f172a; --text: #e2e8f0; --muted: #94a3b8; --accent: #38bdf8; }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: Inter, system-ui, sans-serif; background: var(--bg); color: var(--text); }
    #app { min-height: 100vh; }
    .shell { padding: 24px; }
    .card { background: var(--panel); border: 1px solid #1e293b; border-radius: 16px; padding: 20px; }
    .nav { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px; }
    .nav button { border: none; border-radius: 999px; padding: 10px 14px; background: #1e293b; color: var(--text); cursor: pointer; }
    .nav button.active { background: var(--accent); color: #072136; }
    ''',
    'css/auth.css': '.auth-card { max-width: 420px; margin: 80px auto; }',
    'css/dashboard.css': '.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin: 16px 0; }',
    'css/employees.css': '.employee-list { display: grid; gap: 12px; }',
    'css/attendance.css': '.attendance-panel { display: grid; gap: 16px; }',
    'css/payroll.css': '.payroll-summary { display: grid; gap: 12px; }',
    'css/leaves.css': '.leave-card { padding: 12px; border-radius: 12px; background: #111827; }',
    'css/reports.css': '.report-grid { display: grid; gap: 12px; }',
    'css/settings.css': '.settings-grid { display: grid; gap: 16px; }',
    'css/components.css': '.module-card { padding: 16px; background: #0f172a; border-radius: 14px; }',
    'css/responsive.css': '@media (max-width: 768px) { .shell { padding: 12px; } }',
    'css/variables.css': ':root { --radius: 14px; --spacing: 16px; }',
}
for rel, content in css_files.items():
    write(rel, content)

write('js/config.js', '''
export const config = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  wsUrl: import.meta.env.VITE_WS_URL || 'ws://localhost:5000'
};
''')

write('js/api/client.js', '''
import { config } from '../config.js';

export async function request(path, options = {}) {
  const response = await fetch(`${config.apiBaseUrl}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  });
  return response.json();
}
''')

write('js/api/auth.js', '''
export async function login(email, password) {
  return { success: true, message: 'Login placeholder', email, password };
}
''')

write('js/api/employees.js', '''
export async function getEmployees() {
  return [];
}
''')

write('js/api/attendance.js', '''
export async function getAttendance() {
  return [];
}
''')

write('js/api/payroll.js', '''
export async function getPayrollSummary() {
  return { netPay: 0 };
}
''')

write('js/api/recruitment.js', '''
export async function getRecruitmentData() {
  return [];
}
''')

write('js/api/reports.js', '''
export async function getReports() {
  return [];
}
''')

write('js/api/websocket.js', '''
export function connectWebSocket(url) {
  return { url, connected: false };
}
''')

components_common = {
    'js/components/common/Layout.js': '''
    export function Layout() {
      return `
        <div class="shell">
          <nav class="nav" id="nav"></nav>
          <main id="page"></main>
        </div>
      `;
    }
    ''',
    'js/components/common/Loading.js': 'export function Loading() { return `<div class="card">Loading…</div>`; }\n',
    'js/components/common/ErrorBoundary.js': 'export function ErrorBoundary(message = "Something went wrong") { return `<div class="card">${message}</div>`; }\n',
    'js/components/common/Modal.js': 'export function Modal(title, content) { return `<div class="card"><h3>${title}</h3><p>${content}</p></div>`; }\n',
    'js/components/common/Toast.js': 'export function Toast(message) { return `<div class="card">${message}</div>`; }\n',
    'js/components/common/ConfirmDialog.js': 'export function ConfirmDialog(message) { return `<div class="card"><p>${message}</p><button>Confirm</button></div>`; }\n',
    'js/components/common/Pagination.js': 'export function Pagination() { return `<div class="card">Pagination</div>`; }\n',
    'js/components/common/SearchBar.js': 'export function SearchBar() { return `<input type="search" placeholder="Search" />`; }\n',
    'js/components/common/DatePicker.js': 'export function DatePicker() { return `<input type="date" />`; }\n',
    'js/components/common/NepaliDatePicker.js': 'export function NepaliDatePicker() { return `<input type="text" placeholder="YYYY-MM-DD" />`; }\n',
}
for rel, content in components_common.items():
    write(rel, content)

component_titles = {
    'js/components/dashboard/Dashboard.js': 'Dashboard',
    'js/components/dashboard/AnalyticsCards.js': 'Analytics',
    'js/components/dashboard/AttendanceChart.js': 'Attendance Chart',
    'js/components/dashboard/PayrollChart.js': 'Payroll Chart',
    'js/components/dashboard/EmployeeDistribution.js': 'Employee Distribution',
    'js/components/dashboard/RecentActivities.js': 'Recent Activities',
    'js/components/dashboard/QuickActions.js': 'Quick Actions',
    'js/components/3d/Scene3D.js': '3D Scene',
    'js/components/3d/AttendanceHeatmap3D.js': 'Attendance Heatmap 3D',
    'js/components/3d/OrgChart3D.js': 'Org Chart 3D',
    'js/components/3d/GlobeVisualization.js': 'Globe Visualization',
    'js/components/3d/ResourceBubbleChart3D.js': 'Resource Bubble Chart 3D',
    'js/components/employees/EmployeeList.js': 'Employee List',
    'js/components/employees/EmployeeCard.js': 'Employee Card',
    'js/components/employees/EmployeeForm.js': 'Employee Form',
    'js/components/employees/EmployeeProfile.js': 'Employee Profile',
    'js/components/employees/EmployeeFilters.js': 'Employee Filters',
    'js/components/employees/EmployeeImport.js': 'Employee Import',
    'js/components/attendance/AttendanceTable.js': 'Attendance Table',
    'js/components/attendance/CheckInOut.js': 'Check In / Out',
    'js/components/attendance/AttendanceCalendar.js': 'Attendance Calendar',
    'js/components/attendance/ShiftManagement.js': 'Shift Management',
    'js/components/attendance/LeaveApplication.js': 'Leave Application',
    'js/components/attendance/LeaveApproval.js': 'Leave Approval',
    'js/components/attendance/BiometricDevices.js': 'Biometric Devices',
    'js/components/attendance/ManualAttendance.js': 'Manual Attendance',
    'js/components/payroll/PayrollDashboard.js': 'Payroll Dashboard',
    'js/components/payroll/PayrollCalculator.js': 'Payroll Calculator',
    'js/components/payroll/PayslipGenerator.js': 'Payslip Generator',
    'js/components/payroll/SalaryStructure.js': 'Salary Structure',
    'js/components/payroll/TaxCalculator.js': 'Tax Calculator',
    'js/components/payroll/BenefitsManagement.js': 'Benefits Management',
    'js/components/payroll/PayrollReports.js': 'Payroll Reports',
    'js/components/recruitment/JobRequisitions.js': 'Job Requisitions',
    'js/components/recruitment/JobPostings.js': 'Job Postings',
    'js/components/recruitment/CandidateManagement.js': 'Candidate Management',
    'js/components/recruitment/ResumeParser.js': 'Resume Parser',
    'js/components/recruitment/InterviewScheduler.js': 'Interview Scheduler',
    'js/components/recruitment/AssessmentManager.js': 'Assessment Manager',
    'js/components/recruitment/Onboarding.js': 'Onboarding',
    'js/components/performance/PerformanceReviews.js': 'Performance Reviews',
    'js/components/performance/GoalTracking.js': 'Goal Tracking',
    'js/components/performance/OKRManagement.js': 'OKR Management',
    'js/components/performance/FeedbackSystem.js': 'Feedback System',
    'js/components/performance/SkillMatrix.js': 'Skill Matrix',
    'js/components/performance/CareerPath.js': 'Career Path',
    'js/components/reports/ReportBuilder.js': 'Report Builder',
    'js/components/reports/CustomDashboards.js': 'Custom Dashboards',
    'js/components/reports/ScheduledReports.js': 'Scheduled Reports',
    'js/components/reports/DataExport.js': 'Data Export',
    'js/components/reports/AnalyticsHub.js': 'Analytics Hub',
    'js/components/administration/TenantManagement.js': 'Tenant Management',
    'js/components/administration/UserManagement.js': 'User Management',
    'js/components/administration/RoleManagement.js': 'Role Management',
    'js/components/administration/SystemSettings.js': 'System Settings',
    'js/components/administration/AuditLogs.js': 'Audit Logs',
    'js/components/administration/BackupManagement.js': 'Backup Management',
    'js/components/employee-self-service/MyProfile.js': 'My Profile',
    'js/components/employee-self-service/MyAttendance.js': 'My Attendance',
    'js/components/employee-self-service/MyLeaves.js': 'My Leaves',
    'js/components/employee-self-service/MyPayslips.js': 'My Payslips',
    'js/components/employee-self-service/MyTeam.js': 'My Team',
    'js/components/employee-self-service/MyDocuments.js': 'My Documents',
    'js/components/chat/ChatBot.js': 'Chat Bot',
    'js/components/chat/EmployeeChat.js': 'Employee Chat',
    'js/components/chat/ChatHistory.js': 'Chat History',
}
for rel, title in component_titles.items():
    name = Path(rel).stem
    write(rel, f'export function {name}() {{ return `<div class="module-card"><h2>{title}</h2><p>Placeholder content.</p></div>`; }}\n')

hooks = {
    'js/hooks/useAuth.js': 'export function useAuth() { return { user: null, ready: true }; }\n',
    'js/hooks/useTenant.js': 'export function useTenant() { return { tenant: null }; }\n',
    'js/hooks/useWebSocket.js': 'export function useWebSocket() { return { connected: false }; }\n',
    'js/hooks/usePermissions.js': 'export function usePermissions() { return { can: () => true }; }\n',
    'js/hooks/useNotification.js': 'export function useNotification() { return { notify: () => {} }; }\n',
    'js/hooks/useQuery.js': 'export function useQuery() { return {}; }\n',
    'js/hooks/useMutation.js': 'export function useMutation() { return {}; }\n',
    'js/hooks/useDebounce.js': 'export function useDebounce(value) { return value; }\n',
    'js/hooks/useLocalStorage.js': 'export function useLocalStorage(key, initial) { return [initial, () => {}]; }\n',
}
for rel, content in hooks.items():
    write(rel, content)

context = {
    'js/context/AuthContext.js': 'export const AuthContext = { currentUser: null };\n',
    'js/context/TenantContext.js': 'export const TenantContext = { tenant: null };\n',
    'js/context/ThemeContext.js': 'export const ThemeContext = { theme: "dark" };\n',
    'js/context/NotificationContext.js': 'export const NotificationContext = { notify: () => {} };\n',
    'js/context/WebsocketContext.js': 'export const WebsocketContext = { socket: null };\n',
}
for rel, content in context.items():
    write(rel, content)

write('js/store/store.js', 'export const store = { getState: () => ({}) };\n')
store_slices = {
    'js/store/slices/authSlice.js': 'export const authSlice = { status: "idle" };\n',
    'js/store/slices/employeeSlice.js': 'export const employeeSlice = { employees: [] };\n',
    'js/store/slices/attendanceSlice.js': 'export const attendanceSlice = { records: [] };\n',
    'js/store/slices/payrollSlice.js': 'export const payrollSlice = { summary: null };\n',
    'js/store/slices/uiSlice.js': 'export const uiSlice = { activePage: "dashboard" };\n',
    'js/store/slices/notificationSlice.js': 'export const notificationSlice = { items: [] };\n',
}
for rel, content in store_slices.items():
    write(rel, content)

utils = {
    'js/utils/dateUtils.js': 'export function formatDate(value) { return value || ""; }\n',
    'js/utils/nepaliDateUtils.js': 'export function formatNepaliDate(value) { return value || ""; }\n',
    'js/utils/validation.js': 'export function validateEmail(email) { return /@/.test(email); }\n',
    'js/utils/formatters.js': 'export function formatCurrency(value) { return `Rs. ${value || 0}`; }\n',
    'js/utils/permissions.js': 'export function canAccess() { return true; }\n',
    'js/utils/constants.js': 'export const ROUTES = ["dashboard", "employees", "attendance", "payroll", "reports", "settings"];\n',
    'js/utils/helpers.js': 'export function slugify(value) { return value.toLowerCase().replace(/\\s+/g, "-"); }\n',
}
for rel, content in utils.items():
    write(rel, content)

pages = {
    'js/pages/Login.js': 'export function LoginPage() { return `<section class="card auth-card"><h1>Login</h1><p>Welcome to Enterprise HRMS.</p></section>`; }\n',
    'js/pages/Dashboard.js': 'export function DashboardPage() { return `<section class="card"><h1>Dashboard</h1><p>Overview placeholder.</p></section>`; }\n',
    'js/pages/Employees.js': 'export function EmployeesPage() { return `<section class="card"><h1>Employees</h1></section>`; }\n',
    'js/pages/Attendance.js': 'export function AttendancePage() { return `<section class="card"><h1>Attendance</h1></section>`; }\n',
    'js/pages/Payroll.js': 'export function PayrollPage() { return `<section class="card"><h1>Payroll</h1></section>`; }\n',
    'js/pages/Recruitment.js': 'export function RecruitmentPage() { return `<section class="card"><h1>Recruitment</h1></section>`; }\n',
    'js/pages/Performance.js': 'export function PerformancePage() { return `<section class="card"><h1>Performance</h1></section>`; }\n',
    'js/pages/Reports.js': 'export function ReportsPage() { return `<section class="card"><h1>Reports</h1></section>`; }\n',
    'js/pages/Settings.js': 'export function SettingsPage() { return `<section class="card"><h1>Settings</h1></section>`; }\n',
    'js/pages/NotFound.js': 'export function NotFoundPage() { return `<section class="card"><h1>404</h1></section>`; }\n',
    'js/pages/Unauthorized.js': 'export function UnauthorizedPage() { return `<section class="card"><h1>401</h1></section>`; }\n',
}
for rel, content in pages.items():
    write(rel, content)

write('js/routes.js', '''
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
  const Page = routes[path] || NotFoundPage;
  target.innerHTML = Page();
}
''')

write('js/app.js', '''
import { Layout } from './components/common/Layout.js';
import { initRouter } from './routes.js';
import './config.js';

const app = document.getElementById('app');
app.innerHTML = Layout();

const nav = document.getElementById('nav');
nav.innerHTML = `
  <button class="active" data-route="dashboard">Dashboard</button>
  <button data-route="employees">Employees</button>
  <button data-route="attendance">Attendance</button>
  <button data-route="payroll">Payroll</button>
  <button data-route="recruitment">Recruitment</button>
  <button data-route="performance">Performance</button>
  <button data-route="reports">Reports</button>
  <button data-route="settings">Settings</button>
`;

nav.querySelectorAll('button').forEach((button) => {
  button.addEventListener('click', () => {
    nav.querySelectorAll('button').forEach((b) => b.classList.remove('active'));
    button.classList.add('active');
    window.location.hash = button.dataset.route;
    initRouter(document.getElementById('page'));
  });
});

window.addEventListener('hashchange', () => initRouter(document.getElementById('page')));
initRouter(document.getElementById('page'));
''')

for rel in ['public/favicon.ico', 'public/manifest.json', 'public/robots.txt']:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if rel.endswith('.ico'):
        path.write_bytes(b'')
    else:
        path.write_text('{"name":"Enterprise HRMS"}' if rel.endswith('manifest.json') else 'User-agent: *\nDisallow:', encoding='utf-8')

write('tests/unit/example.test.js', 'export function example() { return true; }\n')
write('tests/integration/example.test.js', 'export function example() { return true; }\n')
write('tests/e2e/example.test.js', 'export function example() { return true; }\n')

print('frontend scaffold created')
