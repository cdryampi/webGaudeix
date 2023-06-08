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
  