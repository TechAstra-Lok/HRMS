import { checkIn, checkOut } from '../api/attendance.js';

export function AttendancePage() {
  return `
    <section class="card attendance-card">
      <div class="section-header">
        <div>
          <p class="eyebrow">HRMS workspace</p>
          <h1>Attendance</h1>
        </div>
        <span class="pill">Realtime</span>
      </div>
      <div class="attendance-actions">
        <button id="checkInButton" class="primary-button">Check in</button>
        <button id="checkOutButton" class="secondary-button">Check out</button>
      </div>
      <div class="status-panel">
        <p id="attendanceStatus">Tap an action to record attendance.</p>
      </div>
    </section>
  `;
}

AttendancePage.afterRender = () => {
  const statusPanel = document.getElementById('attendanceStatus');

  document.getElementById('checkInButton')?.addEventListener('click', async () => {
    statusPanel.textContent = 'Recording check-in…';
    try {
      await checkIn(null);
      statusPanel.textContent = 'Check-in recorded successfully.';
    } catch (error) {
      statusPanel.textContent = `Check-in failed: ${error.message}`;
    }
  });

  document.getElementById('checkOutButton')?.addEventListener('click', async () => {
    statusPanel.textContent = 'Recording check-out…';
    try {
      await checkOut(null);
      statusPanel.textContent = 'Check-out recorded successfully.';
    } catch (error) {
      statusPanel.textContent = `Check-out failed: ${error.message}`;
    }
  });
};
