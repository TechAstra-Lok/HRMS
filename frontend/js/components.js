// ========================================
// COMPONENT FUNCTIONS
// ========================================

// Toast System
function showToast(message, type = 'info', duration = 4000) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div class="toast-icon">
            <i class="fas ${icons[type] || icons.info}"></i>
        </div>
        <div class="toast-content">${message}</div>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        if (toast.parentElement) {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100px)';
            setTimeout(() => toast.remove(), 300);
        }
    }, duration);
}

// Modal System
function showModal(options) {
    const {
        title = 'Modal',
        body = '',
        confirmText = 'Confirm',
        cancelText = 'Cancel',
        onConfirm = null,
        onCancel = null,
        showFooter = true
    } = options;

    const overlay = document.getElementById('modalOverlay');
    const titleEl = document.getElementById('modalTitle');
    const bodyEl = document.getElementById('modalBody');
    const footerEl = document.getElementById('modalFooter');
    const confirmBtn = document.getElementById('modalConfirmBtn');

    titleEl.textContent = title;
    bodyEl.innerHTML = body;

    if (showFooter) {
        footerEl.style.display = 'flex';
        confirmBtn.textContent = confirmText;
    } else {
        footerEl.style.display = 'none';
    }

    // Set confirm handler
    confirmBtn.onclick = () => {
        if (onConfirm) onConfirm();
        closeModal();
    };

    // Set cancel handler
    const cancelBtn = footerEl.querySelector('.btn-secondary');
    if (cancelBtn) {
        cancelBtn.onclick = () => {
            if (onCancel) onCancel();
            closeModal();
        };
    }

    overlay.classList.add('show');
}

function closeModal() {
    document.getElementById('modalOverlay').classList.remove('show');
}

// Sidebar Toggle
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
    sidebar.classList.remove('open');
}

function toggleMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
}

// Notification Panel
function toggleNotifications() {
    const panel = document.getElementById('notificationPanel');
    panel.classList.toggle('show');
}

// Close dropdowns on outside click
document.addEventListener('click', (e) => {
    // Close notification panel
    const panel = document.getElementById('notificationPanel');
    const btn = document.getElementById('notificationBtn');
    if (panel && btn) {
        if (!panel.contains(e.target) && !btn.contains(e.target)) {
            panel.classList.remove('show');
        }
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+K or Cmd+K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.getElementById('globalSearch');
        if (searchInput) {
            searchInput.focus();
            searchInput.select();
        }
    }

    // Escape key
    if (e.key === 'Escape') {
        closeModal();
        const panel = document.getElementById('notificationPanel');
        if (panel) panel.classList.remove('show');
    }
});

// ========================================
// INITIALIZATION
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    // Sidebar toggle
    const toggleBtn = document.getElementById('sidebarToggle');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleSidebar);
    }

    // Mobile menu toggle
    const menuToggle = document.getElementById('menuToggle');
    if (menuToggle) {
        menuToggle.addEventListener('click', toggleMobileSidebar);
    }

    // Notification toggle
    const notifBtn = document.getElementById('notificationBtn');
    if (notifBtn) {
        notifBtn.addEventListener('click', toggleNotifications);
    }

    // Navigation items
    document.querySelectorAll('.nav-item[data-page]').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = item.dataset.page;
            navigateTo(page);
        });
    });

    // Logout
    document.getElementById('logoutBtn')?.addEventListener('click', (e) => {
        e.preventDefault();
        showConfirmDialog({
            title: 'Logout',
            message: 'Are you sure you want to logout?',
            onConfirm: () => {
                showToast('Logged out successfully', 'success');
                // Redirect to login
            }
        });
    });

    // User settings button
    document.getElementById('userSettingsBtn')?.addEventListener('click', (e) => {
        e.stopPropagation();
        showToast('User settings coming soon', 'info');
    });
});

// Navigation function
function navigateTo(page) {
    // Update active nav item
    document.querySelectorAll('.nav-item[data-page]').forEach(item => {
        item.classList.remove('active');
    });
    const activeItem = document.querySelector(`.nav-item[data-page="${page}"]`);
    if (activeItem) activeItem.classList.add('active');

    // Update page visibility
    document.querySelectorAll('.page').forEach(p => {
        p.classList.remove('active');
    });
    const targetPage = document.getElementById(`page-${page}`);
    if (targetPage) targetPage.classList.add('active');

    // Update breadcrumb
    const titleMap = {
        dashboard: 'Dashboard',
        employees: 'Employees',
        attendance: 'Attendance',
        payroll: 'Payroll',
        leaves: 'Leaves',
        recruitment: 'Recruitment',
        performance: 'Performance',
        reports: 'Reports',
        analytics: 'AI Analytics',
        settings: 'Settings'
    };
    document.getElementById('pageTitle').textContent = titleMap[page] || page;

    // Close mobile sidebar
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.remove('open');

    // Show toast for navigation
    showToast(`Navigated to ${titleMap[page] || page}`, 'info', 1500);
}

// Confirm Dialog
function showConfirmDialog(options) {
    const {
        title = 'Confirm',
        message = 'Are you sure?',
        confirmText = 'Yes',
        cancelText = 'Cancel',
        type = 'info',
        onConfirm = null,
        onCancel = null
    } = options;

    const icons = {
        warning: 'fa-exclamation-triangle',
        danger: 'fa-times-circle',
        info: 'fa-info-circle',
        success: 'fa-check-circle'
    };

    const body = `
        <div style="text-align: center; padding: 20px 0;">
            <i class="fas ${icons[type] || icons.info}" 
               style="font-size: 48px; color: ${type === 'danger' ? 'var(--danger)' : type === 'warning' ? 'var(--warning)' : 'var(--primary)'}; margin-bottom: 16px;"></i>
            <h4 style="margin-bottom: 8px;">${message}</h4>
        </div>
    `;

    showModal({
        title,
        body,
        confirmText,
        cancelText,
        onConfirm,
        onCancel
    });
}

// Export functions globally
window.showToast = showToast;
window.showModal = showModal;
window.closeModal = closeModal;
window.showConfirmDialog = showConfirmDialog;
window.navigateTo = navigateTo;
window.toggleSidebar = toggleSidebar;
window.toggleMobileSidebar = toggleMobileSidebar;
window.toggleNotifications = toggleNotifications;