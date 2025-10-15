/**
 * Gaudeix - Sistema de Preload con NProgress
 *
 * Implementa una barra de progreso profesional que se muestra durante
 * la carga de la página y navegación entre páginas.
 */

import NProgress from "nprogress";
import "nprogress/nprogress.css";

// ============================================
// Configuración de NProgress
// ============================================
NProgress.configure({
  // Mostrar el spinner de carga
  showSpinner: true,

  // Velocidad de la animación (ms)
  speed: 400,

  // Velocidad mínima de incremento
  trickleSpeed: 200,

  // Mínimo porcentaje de incremento
  minimum: 0.08,

  // Selector del contenedor padre
  parent: "body",
});

// ============================================
// Personalización de estilos
// ============================================
const style = document.createElement("style");
style.textContent = `
  /* Barra de progreso principal */
  #nprogress .bar {
    background: #2563eb !important; /* Azul Tailwind - ajusta según tu paleta */
    height: 3px;
    box-shadow: 0 0 10px #2563eb, 0 0 5px #2563eb;
  }

  /* Spinner de carga */
  #nprogress .spinner-icon {
    border-top-color: #2563eb !important;
    border-left-color: #2563eb !important;
  }

  /* Efecto de brillo en la barra */
  #nprogress .peg {
    box-shadow: 0 0 10px #2563eb, 0 0 5px #2563eb !important;
  }

  /* Posicionamiento del spinner */
  #nprogress .spinner {
    top: 15px;
    right: 15px;
  }

  /* Animación suave */
  #nprogress {
    pointer-events: none;
  }

  /* Asegurar que esté por encima de todo */
  #nprogress {
    z-index: 9999999;
  }

  /* Ocultar spinner en móviles si lo deseas */
  @media (max-width: 768px) {
    #nprogress .spinner {
      display: none;
    }
  }
`;
document.head.appendChild(style);

// ============================================
// Eventos del ciclo de vida de la página
// ============================================

// Iniciar el preload INMEDIATAMENTE cuando se carga este script
NProgress.start();
console.log("🚀 NProgress: Iniciado");

// Progreso al 40% cuando el DOM está listo
document.addEventListener("DOMContentLoaded", () => {
  NProgress.set(0.4);
  console.log("📊 NProgress: DOM cargado (40%)");
});

// Completar cuando la página está totalmente cargada
window.addEventListener("load", () => {
  NProgress.done();
  console.log("✅ NProgress: Página completamente cargada");
});

// ============================================
// Interceptar clics en enlaces para mostrar progreso
// ============================================
document.addEventListener("click", (e) => {
  const link = e.target.closest("a");

  // Solo procesar enlaces internos que no sean # o javascript:
  if (
    link &&
    link.href &&
    !link.href.startsWith("javascript:") &&
    !link.href.includes("#") &&
    link.hostname === window.location.hostname &&
    !link.hasAttribute("download") &&
    !link.target &&
    !link.hasAttribute("data-no-preload")
  ) {
    // Mostrar progreso antes de navegar
    NProgress.start();
    console.log("🔗 NProgress: Navegando a", link.href);
  }
});

// ============================================
// Progreso automático con AJAX/Fetch
// ============================================

// Interceptar fetch (para peticiones AJAX)
const originalFetch = window.fetch;
window.fetch = function (...args) {
  NProgress.start();
  return originalFetch.apply(this, args).finally(() => {
    NProgress.done();
  });
};

// Interceptar XMLHttpRequest (para AJAX tradicional)
const originalOpen = XMLHttpRequest.prototype.open;
XMLHttpRequest.prototype.open = function () {
  this.addEventListener("loadstart", () => NProgress.start());
  this.addEventListener("loadend", () => NProgress.done());
  originalOpen.apply(this, arguments);
};

console.log("✨ NProgress preloader inicializado correctamente");
