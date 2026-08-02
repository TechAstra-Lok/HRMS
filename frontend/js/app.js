// ========================================
// MAIN APPLICATION
// ========================================

class App {
    constructor() {
        this.init();
    }

    init() {
        console.log('🚀 Enterprise HRMS v3.0 initialized');
        this.setupGlobalEventListeners();
        this.setupKeyboardShortcuts();
        this.setupSearch();
        this.loadUserData();
        this.startAutoRefresh();
    }

    setupGlobalEventListeners() {
        // Handle page visibility change
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.onPageVisible();
            }
        });

        // Handle online/offline status
        window.addEventListener('online', () => {
            showToast('Back online!', 'success');
        });

        window.addEventListener('offline', () => {
            showToast('You are offline. Some features may not work.', 'warning');
        });

        // Handle errors
        window.addEventListener('error', (e) => {
            console.error('Global error:', e.error);
            if (e.error && !e.error.isTrusted) {
                showToast('An unexpected error occurred. Please try again.', 'error');
            }
        });

        // Handle unhandled promise rejections
        window.addEventListener('unhandledrejection', (e) => {
            console.error('Unhandled rejection:', e.reason);
            showToast('An unexpected error occurred. Please try again.', 'error');
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Alt+1-9 for navigation
            if (e.altKey && e.key >= '1' && e.key <= '9') {
                e.preventDefault();
                const pages = ['dashboard', 'employees', 'attendance', 'payroll', 'leaves', 'recruitment', 'performance', 'reports', 'settings'];
                const index = parseInt(e.key) - 1;
                if (pages[index]) {
                    navigateTo(pages[index]);
                }
            }

            // Ctrl+Shift+D for dark mode toggle
            if (e.ctrlKey && e.shiftKey && e.key === 'D') {
                e.preventDefault();
                themeManager.toggle();
            }

            // Ctrl+Shift+R for refresh
            if (e.ctrlKey && e.shiftKey && e.key === 'R') {
                e.preventDefault();
                refreshDashboard();
            }
        });
    }

    setupSearch() {
        const searchInput = document.getElementById('globalSearch');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                const query = e.target.value.trim();
                if (query.length > 2) {
                    searchTimeout = setTimeout(() => {
                        this.performSearch(query);
                    }, 500);
                }
            });

            searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.performSearch(searchInput.value.trim());
                }
            });
        }
    }

    performSearch(query) {
        if (!query) return;
        showToast(`Searching for: "${query}"`, 'info');
        // Implement search logic here
    }

    loadUserData() {
        // Simulate loading user data
        const user = {
            name: 'Admin User',
            role: 'Super Admin',
            avatar: 'https://ui-avatars.com/api/?name=Admin+User&background=4F46E5&color=fff&size=80'
        };

        // Update UI with user data
        document.querySelectorAll('.user-name').forEach(el => {
            el.textContent = user.name;
        });
        document.querySelectorAll('.user-role').forEach(el => {
            el.textContent = user.role;
        });
        document.querySelectorAll('.user-avatar img, .user-profile-top img').forEach(el => {
            if (el.tagName === 'IMG') {
                el.src = user.avatar;
            }
        });
    }

    startAutoRefresh() {
        // Auto-refresh dashboard every 5 minutes
        setInterval(() => {
            const activePage = document.querySelector('.page.active');
            if (activePage && activePage.id === 'page-dashboard') {
                refreshDashboard();
            }
        }, 300000); // 5 minutes
    }

    onPageVisible() {
        // Refresh data when page becomes visible
        const activePage = document.querySelector('.page.active');
        if (activePage && activePage.id === 'page-dashboard') {
            refreshDashboard();
        }
    }
}

// Initialize app
const app = new App();

// Export for debugging
window.app = app;

console.log('✨ Enterprise HRMS v3.0 ready');
console.log('📖 Keyboard shortcuts:');
console.log('  Alt+1-9: Navigate pages');
console.log('  Ctrl+Shift+D: Toggle dark mode');
console.log('  Ctrl+Shift+R: Refresh dashboard');
console.log('  Ctrl+K: Focus search');
console.log('  ESC: Close modals');