import { login, saveAuthTokens, isAuthenticated } from '../api/auth.js';
import { sanitize } from '../security/protection.js';

export function LoginPage() {
  return `
    <section class="card auth-card">
      <div class="auth-header">
        <p class="eyebrow">Secure login</p>
        <h1>Welcome back</h1>
        <p>Sign in to access HR, payroll and analytics.
      </div>
      <form id="loginForm" class="auth-form">
        <label for="loginEmail">Email</label>
        <input id="loginEmail" type="email" autocomplete="username" required placeholder="name@company.com" />

        <label for="loginPassword">Password</label>
        <input id="loginPassword" type="password" autocomplete="current-password" required placeholder="••••••••" />

        <button type="submit" class="primary-button">Sign in</button>
        <p class="form-note">Use your enterprise credentials to sign in securely.</p>
      </form>
    </section>
  `;
}

LoginPage.afterRender = () => {
  if (isAuthenticated()) {
    window.location.hash = 'dashboard';
    return;
  }

  const form = document.getElementById('loginForm');
  const submitButton = form?.querySelector('button[type="submit"]');
  const errorMessage = document.createElement('div');
  errorMessage.className = 'form-error';
  form?.appendChild(errorMessage);

  form?.addEventListener('submit', async (event) => {
    event.preventDefault();
    errorMessage.textContent = '';

    const email = sanitize(document.getElementById('loginEmail')?.value.trim() || '');
    const password = document.getElementById('loginPassword')?.value || '';

    if (!email || !password) {
      errorMessage.textContent = 'Email and password are required.';
      return;
    }

    submitButton.disabled = true;
    submitButton.textContent = 'Signing in...';

    try {
      const data = await login(email, password);
      saveAuthTokens(data);
      window.location.hash = 'dashboard';
    } catch (error) {
      errorMessage.textContent = error.message || 'Login failed. Please try again.';
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = 'Sign in';
    }
  });
};
