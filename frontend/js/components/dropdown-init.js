/**
 * Dropdown Initialization Component
 * Asegura que los dropdowns de Flowbite se inicialicen correctamente
 */

// Importar Flowbite explícitamente para asegurar que esté disponible
import { initFlowbite } from 'flowbite';

document.addEventListener('DOMContentLoaded', function() {
  console.log('🔽 Inicializando dropdowns...');

  // Función para inicializar Flowbite
  function initializeFlowbiteComponents() {
    try {
      initFlowbite();
      console.log('✅ Dropdowns inicializados con Flowbite');
      return true;
    } catch (error) {
      console.error('❌ Error inicializando Flowbite:', error);
      return false;
    }
  }

  // Inicializar después de un pequeño delay para asegurar que el DOM esté completamente listo
  setTimeout(() => {
    initializeFlowbiteComponents();
  }, 100);

  // Reinicializar dropdowns cuando se abre el menú móvil
  const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
  if (mobileMenuOverlay) {
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
          if (mobileMenuOverlay.classList.contains('show')) {
            setTimeout(() => {
              initializeFlowbiteComponents();
            }, 150);
          }
        }
      });
    });

    observer.observe(mobileMenuOverlay, {
      attributes: true
    });
  }
});
