const INACTIVITY_TIMEOUT = 25 * 60 * 1000;
const CHECK_INTERVAL = 1000;
let lastActivity = Date.now();

const resetTimer = () => {
  lastActivity = Date.now();
};

const disableConsole = () => {
  const noop = () => {}; 
  window.console = {
    log: noop,
    info: noop,
    warn: noop,
    error: noop,
    debug: noop,
    trace: noop,
    table: noop,
    group: noop,
    groupEnd: noop,
    time: noop,
    timeEnd: noop,
  };
};

const blockSensitivePaste = (event) => {
  const target = event.target;
  if (target.matches('input[type="password"], input[data-sensitive], textarea[data-sensitive]')) {
    event.preventDefault();
  }
};

const protect = () => {
  disableConsole();

  document.addEventListener('contextmenu', (event) => event.preventDefault());
  document.addEventListener('keydown', (event) => {
    const forbidden = ['F12', 'Control', 'Shift', 'Meta'];
    if (event.key === 'F12' || (event.ctrlKey && event.shiftKey && ['I', 'J', 'C'].includes(event.key.toUpperCase()))) {
      event.preventDefault();
      event.stopPropagation();
    }
  });

  document.addEventListener('mousemove', resetTimer);
  document.addEventListener('keydown', resetTimer);
  document.addEventListener('touchstart', resetTimer);
  document.addEventListener('click', resetTimer);
  document.addEventListener('copy', resetTimer);
  document.addEventListener('paste', blockSensitivePaste);

  window.setInterval(() => {
    if (Date.now() - lastActivity > INACTIVITY_TIMEOUT) {
      window.location.href = '/logout';
    }
  }, CHECK_INTERVAL);
};

const sanitize = (value) => {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;');
};

const createSecureRequest = async (path, options = {}) => {
  const csrfToken = document.cookie.split('; ').find((cookie) => cookie.startsWith('csrf_token='))?.split('=')[1] || '';
  const headers = {
    'Content-Type': 'application/json',
    'X-CSRF-Token': csrfToken,
    ...options.headers,
  };
  const config = {
    ...options,
    credentials: 'include',
    headers,
  };
  return fetch(path, config);
};

export { protect, sanitize, createSecureRequest };
