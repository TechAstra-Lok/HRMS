/**
 * Payroll Module
 */

function loadPayroll() {
    const month = document.getElementById('payrollMonth').value;
    const year = document.getElementById('payrollYear').value;
    
    apiCall('GET', `/api/payroll?month=${month}&year=${year}`)
        .then(data => {
            renderPayrollTable(data.payroll);
        })
        .catch(error => {
            console.error('Error loading payroll:', error);
            showNotification('Failed to load payroll', 'danger');
        });
}

function renderPayrollTable(payrolls) {
    const tbody = document.getElementById('payrollTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    payrolls?.forEach(payroll => {
        const row = tbody.insertRow();
        
        row.innerHTML = `
            <td>${payroll.employee_name || 'N/A'}</td>
            <td>${formatCurrency(payroll.basic_salary)}</td>
            <td>${formatCurrency(payroll.total_allowances)}</td>
            <td>${formatCurrency(payroll.total_deductions)}</td>
            <td>${formatCurrency(payroll.gross_pay)}</td>
            <td><strong>${formatCurrency(payroll.net_pay)}</strong></td>
            <td>${getStatusBadge(payroll.payment_status)}</td>
            <td>
                <button class="btn btn-primary" onclick="viewPayslip('${payroll.id}')" style="padding:5px 10px; font-size:12px;">View</button>
                ${payroll.payment_status === 'pending' ? `
                    <button class="btn btn-success" onclick="markAsPaid('${payroll.id}')" style="padding:5px 10px; font-size:12px;">Mark Paid</button>
                ` : ''}
            </td>
        `;
    });
}

function viewPayslip(payrollId) {
    apiCall('GET', `/api/payroll/${payrollId}`)
        .then(data => {
            const payroll = data.payroll;
            
            const slipContent = `
                <div style="padding: 20px; font-family: Arial, sans-serif;">
                    <h3 style="text-align: center;">PAYSLIP</h3>
                    <hr>
                    
                    <div style="margin-bottom: 20px;">
                        <p><strong>Employee:</strong> ${payroll.employee_name}</p>
                        <p><strong>Period:</strong> ${payroll.month}/${payroll.year}</p>
                        <p><strong>Payment Status:</strong> ${payroll.payment_status}</p>
                    </div>
                    
                    <hr>
                    
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="background: #f0f0f0;">
                                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Earnings</th>
                                <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">Amount</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td style="border: 1px solid #ddd; padding: 8px;">Basic Salary</td>
                                <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">${formatCurrency(payroll.basic_salary)}</td>
                            </tr>
                            ${Object.entries(payroll.allowances || {}).map(([key, value]) => `
                                <tr>
                                    <td style="border: 1px solid #ddd; padding: 8px;">${key}</td>
                                    <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">${formatCurrency(value)}</td>
                                </tr>
                            `).join('')}
                            <tr style="background: #f0f0f0; font-weight: bold;">
                                <td style="border: 1px solid #ddd; padding: 8px;">Total Earnings</td>
                                <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">${formatCurrency(payroll.gross_pay - payroll.total_deductions)}</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                        <thead>
                            <tr style="background: #f0f0f0;">
                                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Deductions</th>
                                <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">Amount</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${Object.entries(payroll.deductions || {}).map(([key, value]) => `
                                <tr>
                                    <td style="border: 1px solid #ddd; padding: 8px;">${key}</td>
                                    <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">${formatCurrency(value)}</td>
                                </tr>
                            `).join('')}
                            <tr>
                                <td style="border: 1px solid #ddd; padding: 8px;">Income Tax</td>
                                <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">${formatCurrency(payroll.tax_amount)}</td>
                            </tr>
                            <tr style="background: #f0f0f0; font-weight: bold;">
                                <td style="border: 1px solid #ddd; padding: 8px;">Total Deductions</td>
                                <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">${formatCurrency(payroll.total_deductions + payroll.tax_amount)}</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <div style="margin-top: 20px; padding: 15px; background: #e8f5e9; border-radius: 4px;">
                        <h4 style="margin-top: 0;">NET PAY: ${formatCurrency(payroll.net_pay)}</h4>
                    </div>
                </div>
            `;
            
            showModal('Payslip', slipContent, () => {
                // Download PDF
                downloadPayslip(payrollId);
            });
        })
        .catch(error => {
            showNotification('Failed to load payslip: ' + error.message, 'danger');
        });
}

function downloadPayslip(payrollId) {
    window.location.href = `/api/payroll/${payrollId}/pdf`;
}

function markAsPaid(payrollId) {
    if (!confirm('Mark this payroll as paid?')) return;
    
    apiCall('PUT', `/api/payroll/${payrollId}/mark-paid`, {})
        .then(result => {
            showNotification('Payroll marked as paid!', 'success');
            closeModal();
            loadPayroll();
        })
        .catch(error => {
            showNotification('Failed to mark as paid: ' + error.message, 'danger');
        });
}
