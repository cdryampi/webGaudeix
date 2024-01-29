// JavaScript
window.addEventListener('scroll', function() {
    var navbar = document.getElementById('navbar');
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    var offset = 50; // Ajusta este valor según tus necesidades
    
    if (scrollTop > offset) {
      navbar.classList.add('fixed-top');
    } else {
      navbar.classList.remove('fixed-top');
    }
  });

  if (document.getElementById('banner-parallax')) {
    const parallaxLink = document.getElementById('banner-parallax');
    parallaxLink.addEventListener('click', scrollToMain);
  
    function scrollToMain(event) {
      event.preventDefault();
      let mainSection = document.getElementById('main-content');
      if (window.location.pathname === '/') {
        // Estás en la página de inicio
        const previusElement = document.getElementById('banner-parallax');
        mainSection = previusElement.parentElement.parentElement.nextElementSibling;
      }
      

      const nextElementTop = mainSection.getBoundingClientRect().top;
      const bodyTop = document.body.getBoundingClientRect().top;
      const offset = 150;
      const scrollToPosition = nextElementTop - bodyTop - offset;

      window.scrollTo({
        behavior: 'smooth',
        top: scrollToPosition,
      });
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    // Obtenemos todos los elementos con la clase .col-especial-subBlog

    const elementos = document.querySelectorAll('.col-especial-subBlog');

    // Iteramos sobre cada elemento y asignamos los estilos correspondientes
    elementos.forEach((elemento, index) => {
      const colorHover = elemento.dataset.color;

      elemento.style.backgroundColor = colorHover;

      elemento.addEventListener('mouseover', () => {
        elemento.style.backgroundColor = colorHover;
        elemento.style.boxShadow = `0 0 10px ${colorHover}`;
      });

      elemento.addEventListener('mouseout', () => {
        elemento.style.backgroundColor = colorHover;
        elemento.style.boxShadow = 'none';
      });
    });
  });



$(document).ready(function(){
    $('.dropdown-submenu a.dropdown-toggle').on("click", function(e){
        $(this).next('ul').toggle();
        e.stopPropagation();
        e.preventDefault();
    });
});
