// Dark/Light Mode Toggle
// Este script maneja el cambio entre modo oscuro y claro

document.addEventListener('DOMContentLoaded', function() {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
    const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');

    // Verificar si los elementos existen
    if (!themeToggleBtn || !themeToggleLightIcon || !themeToggleDarkIcon) {
        return;
    }

    // Obtener tema guardado en localStorage o usar 'dark' por defecto
    let currentTheme = localStorage.getItem('color-theme') || 'dark';

    // Aplicar tema inicial
    if (currentTheme === 'dark') {
        document.documentElement.classList.add('dark');
        themeToggleLightIcon.classList.remove('hidden');
        themeToggleDarkIcon.classList.add('hidden');
    } else {
        document.documentElement.classList.remove('dark');
        themeToggleLightIcon.classList.add('hidden');
        themeToggleDarkIcon.classList.remove('hidden');
    }

    // Toggle al hacer click
    themeToggleBtn.addEventListener('click', function() {
        // Toggle icons
        themeToggleLightIcon.classList.toggle('hidden');
        themeToggleDarkIcon.classList.toggle('hidden');

        // Toggle dark class
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
    });
});
