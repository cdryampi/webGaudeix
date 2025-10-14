/**
 * Mobile Menu Component
 * Gestión del menú móvil minimalista y responsive
 */

document.addEventListener('DOMContentLoaded', function() {
  const mobileMenuButton = document.getElementById('mobile-menu-button');
  const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
  const closeButton = document.getElementById('mobile-close-btn');

  if (!mobileMenuButton || !mobileMenuOverlay) {
    return;
  }

  // Toggle mobile menu
  function toggleMobileMenu() {
    const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';

    if (isExpanded) {
      closeMobileMenu();
    } else {
      openMobileMenu();
    }
  }

  // Open mobile menu
  function openMobileMenu() {
    mobileMenuOverlay.classList.add('show');
    mobileMenuButton.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden'; // Prevent body scroll

    // Reinitialize Flowbite dropdowns in mobile menu after opening
    if (typeof window.initFlowbite === 'function') {
      setTimeout(() => {
        window.initFlowbite();
      }, 100);
    }
  }

  // Close mobile menu
  function closeMobileMenu() {
    mobileMenuOverlay.classList.remove('show');
    mobileMenuButton.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = ''; // Restore body scroll
  }

  // Event listeners
  mobileMenuButton.addEventListener('click', toggleMobileMenu);

  if (closeButton) {
    closeButton.addEventListener('click', closeMobileMenu);
  }

  // Close on overlay click (outside menu container)
  mobileMenuOverlay.addEventListener('click', function(e) {
    if (e.target === mobileMenuOverlay) {
      closeMobileMenu();
    }
  });

  // Close on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && mobileMenuButton.getAttribute('aria-expanded') === 'true') {
      closeMobileMenu();
    }
  });

  // Close on window resize to desktop
  let resizeTimer;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {
      if (window.innerWidth >= 1024) { // lg breakpoint
        closeMobileMenu();
      }
    }, 250);
  });

  // Close mobile menu when clicking on nav links (only in mobile overlay)
  const mobileNavLinks = mobileMenuOverlay.querySelectorAll('a:not([data-dropdown-toggle])');
  mobileNavLinks.forEach(link => {
    link.addEventListener('click', function() {
      closeMobileMenu();
    });
  });
});
