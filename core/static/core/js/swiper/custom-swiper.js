function initSwiper() {
    let swiper = new Swiper('.swiper-container', {
        loop: true,
        slidesPerView: 1, // Número de tarjetas por slide
        spaceBetween: 10, // Espacio entre tarjetas
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            // Configuración para dispositivos móviles
            374: {
                slidesPerView: 1,
            },
            767: {
                slidesPerView: 3,
            },
            // Configuración para tablets
            991: {
                slidesPerView: 4,
            },
        },
    });
}

function initCollageSwiperCategoriasSeleccion() {
    let collageSwiperCategoriasSeleccion = new Swiper('.swiper-container-collage-categorias-seleccion', {
        loop: true,
        slidesPerView: 1, // Número de tarjetas por slide
        spaceBetween: 20, // Espacio entre tarjetas
        navigation: {
            nextEl: '.custom-next-2',
            prevEl: '.custom-prev-2',
        },
        breakpoints: {
            // Configuración para dispositivos móviles
            374: {
                slidesPerView: 1,
            },
            767: {
                slidesPerView: 3,
            },
            // Configuración para tablets
            991: {
                slidesPerView: 4,
            },
        },
    });
}


document.addEventListener("DOMContentLoaded", function() {
    // Agrupar esta función dentro de una condición
    initSwiper();
    initCollageSwiperCategoriasSeleccion();
    Fancybox.bind('.fancybox', {
        // Opciones de configuración de FancyBox
        groupAll: true,
        });
});
