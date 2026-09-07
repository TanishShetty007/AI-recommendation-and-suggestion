document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle-btn');
    if (!themeToggle) return;

    // Load active theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateToggleIcon(themeToggle, savedTheme);

    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateToggleIcon(themeToggle, newTheme);
    });
});

function updateToggleIcon(btn, theme) {
    const icon = btn.querySelector('i');
    if (!icon) return;

    if (theme === 'dark') {
        icon.className = 'fas fa-sun text-warning';
    } else {
        icon.className = 'fas fa-moon text-primary';
    }
}
