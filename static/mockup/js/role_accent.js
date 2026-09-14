function applyRoleAccentColor() {
  const COLOR_BY_ROLE = { national: 'var(--navy)', pref: 'var(--green)', shokokai: '' };
  const roleSelectEl = document.getElementById('org-role-select');
  const role = roleSelectEl ? roleSelectEl.value : 'shokokai';
  const appShellEl = document.getElementById('app-shell');
  if (!appShellEl) return;
  const color = COLOR_BY_ROLE[role];
  if (color) appShellEl.style.setProperty('--purple', color);
  else appShellEl.style.removeProperty('--purple');
}
window.__applyRoleAccentColor = applyRoleAccentColor;
