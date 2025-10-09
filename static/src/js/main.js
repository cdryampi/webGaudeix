/**
 * Gaudeix - Main JavaScript Entry Point
 *
 * Este archivo es el punto de entrada principal para todo el JavaScript del proyecto.
 * Vite lo procesará y creará un bundle optimizado.
 */

// Importar Tailwind CSS
import "../css/main.css";

console.log("🎨 Gaudeix - Frontend con Tailwind CSS + Vite");

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

// Aquí se importarán los módulos necesarios cuando se creen
// import './modules/menu.js';
// import './modules/carousel.js';
// import './modules/map.js';
