import { getEmployees } from '../api/employees.js';

export function EmployeesPage() {
  return `
    <section class="card">
      <div class="section-header">
        <div>
          <p class="eyebrow">HRMS workspace</p>
          <h1>Employees</h1>
        </div>
        <span class="pill">People data</span>
      </div>
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Department</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody id="employeesTableBody">
            <tr><td colspan="4">Loading employees…</td></tr>
          </tbody>
        </table>
      </div>
    </section>
  `;
}

EmployeesPage.afterRender = async () => {
  const tbody = document.getElementById('employeesTableBody');
  try {
    const employees = await getEmployees();
    if (!employees.length) {
      tbody.innerHTML = '<tr><td colspan="4">No employee records found.</td></tr>';
      return;
    }

    tbody.innerHTML = employees
      .map((employee) => `
        <tr>
          <td>${employee.first_name || ''} ${employee.last_name || ''}</td>
          <td>${employee.email || '—'}</td>
          <td>${employee.department || '—'}</td>
          <td>${employee.is_active ? 'Active' : 'Inactive'}</td>
        </tr>
      `)
      .join('');
  } catch (error) {
    tbody.innerHTML = `<tr><td colspan="4">Unable to load employees: ${error.message}</td></tr>`;
  }
};
