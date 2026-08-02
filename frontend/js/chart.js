// Chart Management
class ChartManager {
    constructor() {
        this.charts = {};
        this.init();
    }

    init() {
        this.createAttendanceChart();
        this.createDepartmentChart();
        this.createMiniSparklines();
    }

    createAttendanceChart() {
        const ctx = document.getElementById('attendanceChart');
        if (!ctx) return;

        const labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        const present = [45, 52, 48, 55, 50, 42, 38];
        const absent = [5, 3, 7, 2, 8, 5, 4];
        const late = [3, 2, 4, 1, 5, 6, 2];
        const leave = [2, 1, 2, 3, 1, 2, 1];

        this.charts.attendance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Present',
                        data: present,
                        backgroundColor: '#22C55E',
                        borderRadius: 4,
                        borderSkipped: false
                    },
                    {
                        label: 'Absent',
                        data: absent,
                        backgroundColor: '#EF4444',
                        borderRadius: 4,
                        borderSkipped: false
                    },
                    {
                        label: 'Late',
                        data: late,
                        backgroundColor: '#F59E0B',
                        borderRadius: 4,
                        borderSkipped: false
                    },
                    {
                        label: 'Leave',
                        data: leave,
                        backgroundColor: '#3B82F6',
                        borderRadius: 4,
                        borderSkipped: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            padding: 20,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(255,255,255,0.9)',
                        titleColor: '#1E293B',
                        bodyColor: '#475569',
                        borderColor: '#E2E8F0',
                        borderWidth: 1,
                        cornerRadius: 8,
                        padding: 12,
                        boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)'
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        stacked: true
                    },
                    y: {
                        grid: {
                            color: 'rgba(0,0,0,0.05)'
                        },
                        stacked: true,
                        beginAtZero: true
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });
    }

    createDepartmentChart() {
        const ctx = document.getElementById('departmentChart');
        if (!ctx) return;

        const data = {
            labels: ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations'],
            datasets: [{
                data: [45, 30, 25, 20, 15, 35],
                backgroundColor: [
                    '#4F46E5',
                    '#22C55E',
                    '#F59E0B',
                    '#EC4899',
                    '#8B5CF6',
                    '#14B8A6'
                ],
                borderWidth: 0,
                hoverOffset: 8
            }]
        };

        this.charts.department = new Chart(ctx, {
            type: 'doughnut',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 16,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(255,255,255,0.9)',
                        titleColor: '#1E293B',
                        bodyColor: '#475569',
                        borderColor: '#E2E8F0',
                        borderWidth: 1,
                        cornerRadius: 8,
                        padding: 12,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                            }
                        }
                    }
                }
            }
        });
    }

    createMiniSparklines() {
        // Mini charts for stat cards
        document.querySelectorAll('.mini-chart').forEach((el, index) => {
            const data = this.generateSparklineData();
            const colors = ['#4F46E5', '#22C55E', '#F59E0B', '#8B5CF6', '#EC4899', '#14B8A6'];
            
            // Create small canvas
            const canvas = document.createElement('canvas');
            canvas.width = 80;
            canvas.height = 30;
            el.appendChild(canvas);

            const ctx = canvas.getContext('2d');
            const gradient = ctx.createLinearGradient(0, 0, 80, 0);
            gradient.addColorStop(0, colors[index % colors.length] + '40');
            gradient.addColorStop(1, colors[index % colors.length] + '10');

            // Draw sparkline
            ctx.beginPath();
            ctx.strokeStyle = colors[index % colors.length];
            ctx.lineWidth = 2;
            ctx.fillStyle = gradient;

            const max = Math.max(...data);
            const min = Math.min(...data);
            const range = max - min || 1;

            ctx.moveTo(0, 30 - ((data[0] - min) / range) * 25);
            for (let i = 1; i < data.length; i++) {
                const x = (i / (data.length - 1)) * 80;
                const y = 30 - ((data[i] - min) / range) * 25;
                ctx.lineTo(x, y);
            }
            ctx.stroke();

            // Fill area
            const lastX = 80;
            const lastY = 30 - ((data[data.length - 1] - min) / range) * 25;
            ctx.lineTo(lastX, 30);
            ctx.lineTo(0, 30);
            ctx.closePath();
            ctx.fill();
        });
    }

    generateSparklineData() {
        const data = [];
        for (let i = 0; i < 20; i++) {
            data.push(Math.random() * 100 + 20);
        }
        return data;
    }

    updateCharts() {
        // Update attendance chart with random data
        if (this.charts.attendance) {
            const datasets = this.charts.attendance.data.datasets;
            datasets.forEach(dataset => {
                dataset.data = dataset.data.map(() => Math.floor(Math.random() * 50) + 20);
            });
            this.charts.attendance.update();
        }
    }
}

// Initialize charts
const chartManager = new ChartManager();

// Global functions
window.toggleChartType = function() {
    const chart = chartManager.charts.attendance;
    if (chart) {
        const currentType = chart.config.type;
        chart.config.type = currentType === 'bar' ? 'line' : 'bar';
        chart.update();
        showToast(`Switched to ${chart.config.type} view`, 'info');
    }
};

window.toggleDonutView = function() {
    const chart = chartManager.charts.department;
    if (chart) {
        const currentType = chart.config.type;
        chart.config.type = currentType === 'doughnut' ? 'pie' : 'doughnut';
        chart.update();
        showToast(`Switched to ${chart.config.type} view`, 'info');
    }
};

window.refreshDashboard = function() {
    chartManager.updateCharts();
    showToast('Dashboard refreshed!', 'success');
};

window.exportReport = function() {
    showToast('Report exported successfully!', 'success');
};

window.showAddEmployee = function() {
    showModal({
        title: 'Add New Employee',
        body: `
            <div class="form-group">
                <label>Full Name</label>
                <input type="text" class="form-control" placeholder="Enter full name">
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" class="form-control" placeholder="Enter email">
            </div>
            <div class="form-group">
                <label>Department</label>
                <select class="form-control">
                    <option>Engineering</option>
                    <option>Sales</option>
                    <option>Marketing</option>
                    <option>HR</option>
                </select>
            </div>
            <div class="form-group">
                <label>Designation</label>
                <input type="text" class="form-control" placeholder="Enter designation">
            </div>
        `,
        confirmText: 'Add Employee',
        onConfirm: () => {
            showToast('Employee added successfully!', 'success');
        }
    });
};