// Dark/Light Mode Toggle
// Este script maneja el cambio entre modo oscuro y claro

document.addEventListener('DOMContentLoaded', function() {
    // Desktop theme toggle
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
    const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');

    // Mobile theme toggle
    const themeToggleBtnMobile = document.getElementById('theme-toggle-mobile');
    const themeToggleLightIconMobile = document.getElementById('theme-toggle-light-icon-mobile');
    const themeToggleDarkIconMobile = document.getElementById('theme-toggle-dark-icon-mobile');

    // Función para aplicar el tema y actualizar iconos
    function applyTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.classList.add('dark');
            // Desktop icons
            if (themeToggleLightIcon) themeToggleLightIcon.classList.remove('hidden');
            if (themeToggleDarkIcon) themeToggleDarkIcon.classList.add('hidden');
            // Mobile icons
            if (themeToggleLightIconMobile) themeToggleLightIconMobile.classList.remove('hidden');
            if (themeToggleDarkIconMobile) themeToggleDarkIconMobile.classList.add('hidden');
        } else {
            document.documentElement.classList.remove('dark');
            // Desktop icons
            if (themeToggleLightIcon) themeToggleLightIcon.classList.add('hidden');
            if (themeToggleDarkIcon) themeToggleDarkIcon.classList.remove('hidden');
            // Mobile icons
            if (themeToggleLightIconMobile) themeToggleLightIconMobile.classList.add('hidden');
            if (themeToggleDarkIconMobile) themeToggleDarkIconMobile.classList.remove('hidden');
        }
    }

    // Obtener tema guardado en localStorage o usar 'dark' por defecto
    let currentTheme = localStorage.getItem('color-theme') || 'dark';

    // Aplicar tema inicial
    applyTheme(currentTheme);

    // Función para toggle del tema
    function toggleTheme() {
        const newTheme = document.documentElement.classList.contains('dark') ? 'light' : 'dark';
        localStorage.setItem('color-theme', newTheme);
        applyTheme(newTheme);
    }

    // Toggle al hacer click en el botón desktop
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', toggleTheme);
    }

    // Toggle al hacer click en el botón móvil
    if (themeToggleBtnMobile) {
        themeToggleBtnMobile.addEventListener('click', toggleTheme);
    }
});
