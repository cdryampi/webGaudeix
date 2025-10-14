/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class', // Habilitar dark mode usando la clase 'dark' en el elemento <html>
  content: [
    "./static/src/**/*.{html,js}",
    "./core/templates/**/*.html",
    "./*/templates/**/*.html",
    "./**/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        // Color principal de Gaudeix
        'gaudeix': {
          DEFAULT: '#3EBFAB',
          light: '#4DCFBB',
          dark: '#2FA999',
        },
      },
    },
  },
};
