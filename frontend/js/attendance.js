/**
 * Attendance Module
 */

function loadEmployees() {
    apiCall('GET', '/api/employees')
        .then(data => {
            renderEmployeeTable(data.employees);
        })
        .catch(error => {
            console.error('Error loading employees:', error);
            showNotification('Failed to load employees', 'danger');
        });
}

function renderEmployeeTable(employees) {
    const tbody = document.getElementById('employeeTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    employees?.forEach(emp => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td>${emp.employee_id}</td>
            <td>${emp.first_name} ${emp.last_name}</td>
            <td>${emp.email}</td>
            <td>${emp.department || '-'}</td>
            <td>${emp.designation || '-'}</td>
            <td>${getStatusBadge(emp.status)}</td>
            <td>
                <button class="btn btn-primary" onclick="editEmployee('${emp.id}')" style="padding:5px 10px; font-size:12px;">Edit</button>
                <button class="btn btn-danger" onclick="deleteEmployee('${emp.id}')" style="padding:5px 10px; font-size:12px;">Delete</button>
            </td>
        `;
    });
}

function editEmployee(employeeId) {
    apiCall('GET', `/api/employees/${employeeId}`)
        .then(data => {
            const emp = data.employee;
            showModal('Edit Employee', `
                <form id="editEmployeeForm">
                    <div class="form-group">
                        <label>First Name</label>
                        <input type="text" id="editFirstName" value="${emp.first_name}" required>
                    </div>
                    <div class="form-group">
                        <label>Last Name</label>
                        <input type="text" id="editLastName" value="${emp.last_name}" required>
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" id="editEmail" value="${emp.email}" required>
                    </div>
                    <div class="form-group">
                        <label>Phone</label>
                        <input type="tel" id="editPhone" value="${emp.phone || ''}" required>
                    </div>
                    <div class="form-group">
                        <label>Department</label>
                        <input type="text" id="editDepartment" value="${emp.department || ''}">
                    </div>
                    <div class="form-group">
                        <label>Designation</label>
                        <input type="text" id="editDesignation" value="${emp.designation || ''}">
                    </div>
                    <div class="form-group">
                        <label>Salary</label>
                        <input type="number" id="editSalary" value="${emp.salary || ''}" step="0.01">
                    </div>
                </form>
            `, () => {
                const updateData = {
                    first_name: document.getElementById('editFirstName').value,
                    last_name: document.getElementById('editLastName').value,
                    email: document.getElementById('editEmail').value,
                    phone: document.getElementById('editPhone').value,
                    department: document.getElementById('editDepartment').value,
                    designation: document.getElementById('editDesignation').value,
                    salary: parseFloat(document.getElementById('editSalary').value)
                };
                
                apiCall('PUT', `/api/employees/${employeeId}`, updateData)
                    .then(result => {
                        showNotification('Employee updated successfully!', 'success');
                        closeModal();
                        loadEmployees();
                    })
                    .catch(error => {
                        showNotification('Failed to update employee: ' + error.message, 'danger');
                    });
            });
        })
        .catch(error => {
            showNotification('Failed to load employee: ' + error.message, 'danger');
        });
}

function deleteEmployee(employeeId) {
    if (!confirm('Are you sure you want to delete this employee?')) return;
    
    apiCall('DELETE', `/api/employees/${employeeId}`)
        .then(result => {
            showNotification('Employee deleted successfully!', 'success');
            loadEmployees();
        })
        .catch(error => {
            showNotification('Failed to delete employee: ' + error.message, 'danger');
        });
}

function loadDailyAttendance() {
    const date = document.getElementById('attendanceDate').value;
    
    apiCall('GET', `/api/attendance/daily?date=${date}`)
        .then(data => {
            renderAttendanceTable(data.attendance);
        })
        .catch(error => {
            console.error('Error loading attendance:', error);
            showNotification('Failed to load attendance', 'danger');
        });
}

function renderAttendanceTable(records) {
    const tbody = document.getElementById('attendanceTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    records?.forEach(record => {
        const row = tbody.insertRow();
        const checkInTime = record.check_in ? formatTime(record.check_in) : '-';
        const checkOutTime = record.check_out ? formatTime(record.check_out) : '-';
        
        row.innerHTML = `
            <td>${record.employee_name || 'N/A'}</td>
            <td>${formatDate(record.date)}</td>
            <td>${checkInTime}</td>
            <td>${checkOutTime}</td>
            <td>${getStatusBadge(record.status)}</td>
            <td>${record.total_hours?.toFixed(2) || '-'} hrs</td>
        `;
    });
}

function loadLeaves() {
    apiCall('GET', '/api/leaves')
        .then(data => {
            renderLeaveTable(data.leaves);
        })
        .catch(error => {
            console.error('Error loading leaves:', error);
            showNotification('Failed to load leaves', 'danger');
        });
}

function renderLeaveTable(leaves) {
    const tbody = document.getElementById('leaveTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    leaves?.forEach(leave => {
        const row = tbody.insertRow();
        const days = calculateDays(new Date(leave.start_date), new Date(leave.end_date));
        
        row.innerHTML = `
            <td>${leave.employee_name || 'N/A'}</td>
            <td>${leave.leave_type}</td>
            <td>${formatDate(leave.start_date)}</td>
            <td>${formatDate(leave.end_date)}</td>
            <td>${days}</td>
            <td>${getStatusBadge(leave.status)}</td>
            <td>
                ${leave.status === 'pending' ? `
                    <button class="btn btn-success" onclick="approveLeave('${leave.id}')" style="padding:5px 10px; font-size:12px;">Approve</button>
                    <button class="btn btn-danger" onclick="rejectLeave('${leave.id}')" style="padding:5px 10px; font-size:12px;">Reject</button>
                ` : ''}
            </td>
        `;
    });
}

function approveLeave(leaveId) {
    if (!confirm('Approve this leave request?')) return;
    
    apiCall('PUT', `/api/leaves/${leaveId}/approve`, {})
        .then(result => {
            showNotification('Leave approved!', 'success');
            loadLeaves();
        })
        .catch(error => {
            showNotification('Failed to approve leave: ' + error.message, 'danger');
        });
}

function rejectLeave(leaveId) {
    const reason = prompt('Rejection reason:');
    if (!reason) return;
    
    apiCall('PUT', `/api/leaves/${leaveId}/reject`, { rejection_reason: reason })
        .then(result => {
            showNotification('Leave rejected!', 'success');
            loadLeaves();
        })
        .catch(error => {
            showNotification('Failed to reject leave: ' + error.message, 'danger');
        });
}
