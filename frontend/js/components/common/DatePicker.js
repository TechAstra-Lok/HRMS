export function DatePicker({ id = 'datePicker', label = 'Date' } = {}) {
  return `
    <label class="form-label" for="${id}">${label}</label>
    <input id="${id}" type="date" class="form-input" />
  `;
}
