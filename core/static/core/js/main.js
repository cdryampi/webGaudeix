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
      
      const mainSection = document.getElementById('banner-parallax');
      console.log(mainSection);
      const nextElement = mainSection.parentElement.parentElement.nextElementSibling;
      console.log(nextElement);
      const nextElementTop = nextElement.getBoundingClientRect().top;
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