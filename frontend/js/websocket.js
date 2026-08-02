/**
 * WebSocket Connection Manager
 */

let socket = null;

function connectWebSocket() {
    const token = localStorage.getItem('accessToken');
    const tenantId = localStorage.getItem('tenantId');
    
    socket = io({
        auth: {
            token,
            tenant_id: tenantId
        },
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        reconnectionAttempts: 5
    });
    
    socket.on('connect', () => {
        socket.emit('join_tenant', { tenant_id: tenantId });
        socket.emit('join_user', { user_id: AppState.currentUser.id });
    });
    
    socket.on('disconnect', () => {
        // WebSocket disconnected
    });
    
    socket.on('attendance_update', (data) => {
        showNotification(`${data.employee_name} checked in/out`, 'info');
        
        if (AppState.currentPage === 'attendance') {
            loadDailyAttendance();
        }
    });
    
    socket.on('leave_notification', (data) => {
        showNotification(`Leave request from ${data.employee_name}`, 'info');
        
        if (AppState.currentPage === 'leaves') {
            loadLeaves();
        }
    });
    
    socket.on('notification', (data) => {
        showNotification(data.message, data.type);
        updateNotificationBadge();
    });
    
    socket.on('attendance_alert', (data) => {
        showNotification(data.message, 'warning');
    });
    
    socket.on('error', () => {
        // Handle WebSocket errors internally.
    });
}

function updateNotificationBadge() {
    // Fetch unread notifications count
    apiCall('GET', '/api/notifications/unread-count')
        .then(result => {
            const badge = document.getElementById('notificationBadge');
            badge.textContent = result.count || 0;
        })
        .catch(error => console.error('Error fetching notifications:', error));
}

function broadcastMessage(message) {
    if (socket && socket.connected) {
        socket.emit('send_message', {
            message,
            timestamp: new Date().toISOString()
        });
    }
}
