/**
 * Dashboard Module
 */

let attendanceChart = null;
let departmentChart = null;

function loadDashboard() {
    apiCall('GET', '/api/dashboard/stats')
        .then(data => {
            updateStats(data);
            loadAttendanceChart(data.attendance_chart);
            loadDepartmentChart(data.department_chart);
            load3DVisualization(data.visualization_data);
            loadRecentActivities(data.recent_activities);
        })
        .catch(error => {
            console.error('Error loading dashboard:', error);
            showNotification('Failed to load dashboard data', 'danger');
        });
}

function updateStats(data) {
    document.getElementById('totalEmployees').textContent = data.total_employees || 0;
    document.getElementById('todayAttendance').textContent = data.today_attendance || 0;
    document.getElementById('pendingLeaves').textContent = data.pending_leaves || 0;
    document.getElementById('monthlyPayroll').textContent = formatCurrency(data.monthly_payroll || 0);
}

function loadAttendanceChart(chartData) {
    const ctx = document.getElementById('attendanceChart')?.getContext('2d');
    if (!ctx) return;
    
    if (attendanceChart) attendanceChart.destroy();
    
    attendanceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData?.labels || ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            datasets: [
                {
                    label: 'Present',
                    data: chartData?.present || [0, 0, 0, 0, 0],
                    backgroundColor: '#27AE60'
                },
                {
                    label: 'Absent',
                    data: chartData?.absent || [0, 0, 0, 0, 0],
                    backgroundColor: '#E74C3C'
                },
                {
                    label: 'Late',
                    data: chartData?.late || [0, 0, 0, 0, 0],
                    backgroundColor: '#F39C12'
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function loadDepartmentChart(chartData) {
    const ctx = document.getElementById('departmentChart')?.getContext('2d');
    if (!ctx) return;
    
    if (departmentChart) departmentChart.destroy();
    
    departmentChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: chartData?.labels || ['IT', 'HR', 'Finance', 'Operations'],
            datasets: [{
                data: chartData?.data || [30, 20, 25, 25],
                backgroundColor: [
                    '#4A90D9',
                    '#27AE60',
                    '#F39C12',
                    '#E74C3C'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function load3DVisualization(data) {
    const container = document.getElementById('threeContainer');
    if (!container) return;
    
    // Initialize Three.js scene
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setClearColor(0xffffff, 1);
    container.innerHTML = '';
    container.appendChild(renderer.domElement);
    
    camera.position.z = 150;
    
    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(100, 100, 100);
    scene.add(directionalLight);
    
    // Create attendance cubes
    const cubes = [];
    const attendanceData = data?.attendance || [];
    
    attendanceData.slice(0, 12).forEach((record, index) => {
        const height = (record.percentage / 100) * 50;
        const geometry = new THREE.BoxGeometry(15, height, 15);
        
        let color = 0x27AE60; // Present (Green)
        if (record.status === 'absent') color = 0xE74C3C; // Red
        else if (record.status === 'late') color = 0xF39C12; // Orange
        else if (record.status === 'leave') color = 0x3498DB; // Blue
        
        const material = new THREE.MeshStandardMaterial({ color });
        const cube = new THREE.Mesh(geometry, material);
        
        const x = (index % 4) * 40 - 60;
        const z = Math.floor(index / 4) * 40;
        
        cube.position.set(x, height / 2, z);
        scene.add(cube);
        cubes.push(cube);
    });
    
    // Animation loop
    const animate = () => {
        requestAnimationFrame(animate);
        
        cubes.forEach((cube, index) => {
            cube.rotation.x += 0.005;
            cube.rotation.y += 0.01;
        });
        
        renderer.render(scene, camera);
    };
    
    animate();
    
    // Handle window resize
    window.addEventListener('resize', () => {
        const width = container.clientWidth;
        const height = container.clientHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    });
}

function loadRecentActivities(activities) {
    const container = document.getElementById('recentActivities');
    if (!container) return;
    
    container.innerHTML = '';
    
    activities?.slice(0, 10).forEach(activity => {
        const item = document.createElement('div');
        item.className = 'activity-item';
        
        const iconMap = {
            'login': 'fa-sign-in-alt',
            'logout': 'fa-sign-out-alt',
            'attendance': 'fa-clock',
            'leave': 'fa-calendar-alt',
            'payroll': 'fa-money-bill-wave',
            'employee': 'fa-users',
            'report': 'fa-chart-bar'
        };
        
        const icon = iconMap[activity.action] || 'fa-info-circle';
        
        item.innerHTML = `
            <div class="activity-icon">
                <i class="fas ${icon}"></i>
            </div>
            <div class="activity-content">
                <h4>${activity.action}</h4>
                <p>${new Date(activity.created_at).toLocaleString()}</p>
            </div>
        `;
        
        container.appendChild(item);
    });
}

function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}
