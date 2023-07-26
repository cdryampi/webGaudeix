function lazyLoadBG() {
  $('.lazy-bg.bg-lazy').each(function() {
    const container = $(this);

    if (
      container.offset().top <= $(window).scrollTop() + $(window).height() &&
      container.offset().top + container.height() >= $(window).scrollTop()
    ) {
      // Si el contenedor es visible en la ventana, cargamos la imagen de fondo
      const src = container.attr('data-src');
      container.css('background-image', `url('${src}')`);

      container.removeClass('lazy-bg');
    }
    if (!$('.lazy-bg.bg-lazy').length) {
      $(document).off('scroll', lazyLoadBG);
      $(window).off('resize', lazyLoadBG);
    }
  });
}


function lazyLoadImages() {
  $('.lazy-load',).each(function() {
    const container = $(this);
    const image = container.find('.lazy-load-img');

    if (
      container.offset().top <= $(window).scrollTop() + $(window).height() &&
      container.offset().top + container.height() >= $(window).scrollTop()
    ) {
      // Si el contenedor de la imagen es visible en la ventana, cargamos las imágenes
      const srcset = image.attr('data-srcset');
      image.attr('srcset', srcset);

      // También puedes aplicar la clase "loaded" a la imagen si lo deseas
      // image.addClass('loaded');

      container.removeClass('lazy-load');
    }
  });

  // Elimina el evento scroll después de que todas las imágenes hayan sido cargadas
  if (!$('.lazy-load').length) {
    $(document).off('scroll', lazyLoadImages);
    $(window).off('resize', lazyLoadImages);
  }
}

// Escucha el evento scroll y carga las imágenes cuando sea necesario
$(document).on('scroll', lazyLoadImages, lazyLoadBG);
$(window).on('resize', lazyLoadImages, lazyLoadBG);

// Carga las imágenes visibles al cargar la página
$(window).on('load', lazyLoadImages,lazyLoadBG);
