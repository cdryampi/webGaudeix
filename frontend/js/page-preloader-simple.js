/**
 * Gaudeix - Simple Page Preloader
 *
 * Preloader simple y efectivo sin dependencias externas complicadas.
 * Muestra un overlay con logo mientras la página carga.
 */

console.log('🎨 Simple Preloader: Inicializando...');

// ============================================
// Configuración
// ============================================
const CONFIG = {
  minDisplayTime: 2500,  // 2.5 segundos mínimo
  hideDelay: 400,        // Tiempo de fade-out
};

// ============================================
// Estado del preloader
// ============================================
let startTime = Date.now();
let isPageLoaded = false;
let preloaderElement = null;

// ============================================
// Crear preloader HTML
// ============================================
const createPreloader = () => {
  // Crear elemento si no existe
  if (!preloaderElement) {
    preloaderElement = document.querySelector('.page-preloader');
  }

  if (!preloaderElement) {
    console.log('✨ Creando HTML del preloader...');

    const preloader = document.createElement('div');
    preloader.className = 'page-preloader active';
    preloader.innerHTML = `
      <div class="preloader-content">
        <img class="preloader-logo"
             src="/static/core/img/logos/logo-cabrera-white.png"
             alt="Gaudeix Cabrera de Mar" />

        <h2 class="preloader-title">Gaudeix Cabrera de Mar</h2>

        <div class="preloader-spinner">
          <div class="spinner-circle"></div>
        </div>

        <p class="preloader-text">Carregant<span class="loading-dots"></span></p>
      </div>
    `;

    document.body.appendChild(preloader);
    preloaderElement = preloader;

    // Bloquear scroll
    document.body.style.overflow = 'hidden';

    console.log('✅ Preloader creado e insertado');
  }
};

// ============================================
// Ocultar preloader
// ============================================
const hidePreloader = () => {
  if (!preloaderElement) return;

  const elapsedTime = Date.now() - startTime;
  const remainingTime = Math.max(0, CONFIG.minDisplayTime - elapsedTime);

  console.log(`⏱️ Tiempo transcurrido: ${elapsedTime}ms, esperando ${remainingTime}ms más...`);

  setTimeout(() => {
    console.log('✅ Ocultando preloader...');

    // Fade out
    preloaderElement.classList.remove('active');
    preloaderElement.classList.add('hidden');

    // Restaurar scroll
    document.body.style.overflow = '';

    // Eliminar del DOM después del fade-out
    setTimeout(() => {
      if (preloaderElement && preloaderElement.parentNode) {
        preloaderElement.remove();
        preloaderElement = null;
        console.log('🎉 Preloader eliminado del DOM');
      }
    }, CONFIG.hideDelay);
  }, remainingTime);
};

// ============================================
// Event Listeners
// ============================================

// Cuando el DOM está listo
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    console.log('📄 DOMContentLoaded');
    createPreloader();
  });
} else {
  // Si ya está cargado
  createPreloader();
}

// Cuando la página se carga completamente (incluyendo imágenes, CSS, etc.)
window.addEventListener('load', () => {
  console.log('🎉 Window Load - Página completamente cargada');
  isPageLoaded = true;
  hidePreloader();
});

// Fallback: si algo falla, ocultar después de 5 segundos
setTimeout(() => {
  if (preloaderElement && preloaderElement.classList.contains('active')) {
    console.warn('⚠️ Preloader tomó demasiado tiempo, forzando ocultación...');
    hidePreloader();
  }
}, 5000);

console.log('✨ Simple Preloader: Configurado');

export default { createPreloader, hidePreloader };
