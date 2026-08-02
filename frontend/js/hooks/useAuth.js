import { getCurrentUser, isAuthenticated } from '../api/auth.js';

export function useAuth() {
  return {
    user: getCurrentUser(),
    ready: true,
    authenticated: isAuthenticated()
  };
}
