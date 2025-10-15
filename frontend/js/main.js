/**
 * Gaudeix - Main JavaScript Entry Point
 *
 * Este archivo es el punto de entrada principal para todo el JavaScript del proyecto.
 * Vite lo procesará y creará un bundle optimizado.
 */

// ============================================
// IMPORTANTE: Page Preloader PRIMERO
// ============================================
// Importar el preloader de página completa ANTES que cualquier otra cosa
// Esto bloqueará la pantalla con una animación hasta que todo esté cargado
import "./page-preloader-simple.js";

// ============================================
// Preload de progreso (barra superior)
// ============================================
// Importar el sistema de preload de NProgress para navegación
import "./preload.js";

// ============================================
// Imports principales
// ============================================

// Importar Tailwind CSS
import "../css/main.css";

// Importar Flowbite para componentes UI interactivos
import "flowbite";

// Importar componentes personalizados
import "./components/theme-toggle.js";
import "./components/mobile-menu.js";
import "./components/dropdown-init.js";

console.log("🎨 Gaudeix - Frontend con Tailwind CSS + Vite + Flowbite");

// Importar dinámicamente los templates para content scanning de Tailwind v4
// Esto permite que Tailwind detecte las clases usadas en los templates Django

// Glob import de todos los templates HTML para que Tailwind los escanee
const templates = import.meta.glob(
  [
    "../../core/templates/**/*.html",
    "../../*/templates/**/*.html",
    "../../**/templates/**/*.html",
  ],
  { query: "?raw", import: "default", eager: false }
);

console.log(
  `📄 Templates detectados para Tailwind: ${Object.keys(templates).length}`
);
