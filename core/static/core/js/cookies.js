  // Función para guardar la cookie al hacer clic en el botón
  
  function acceptCookies() {
    // Crea una nueva fecha con 365 días a partir de la fecha actual
    var expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + 365);

    // Establece la cookie "cookie_accepted" con valor "true" y fecha de expiración de 365 días
    document.cookie = "cookie_accepted=true"+"; expires=" + expirationDate.toUTCString() + "; path=/; Secure; SameSite=Strict";
    // Oculta el mensaje de política de cookies
    document.querySelector(".cookies-message-container").style.display = "none";
  }

  function showAlert() {
    if (!getCookieValue("alertShown")) {
        $('#modal-alerta').modal('show');
        $('#modal-alerta').css("display","block");
        setCookie("alertShown", "true", 10); // Establece la cookie para 10 minutos
    }
  }

  // Función que se ejecuta cuando el documento ha cargado completamente
  function onDocumentLoad() {
    var cookiesMessageContainer = document.querySelector(".cookies-message-container");
    var cookieAccepted = getCookieValue("cookie_accepted");
    if (cookieAccepted && cookieAccepted === "true") {
      // La cookie "cookie_accepted" existe y su valor es "true", ocultar el componente
      
      if (cookiesMessageContainer) {
        cookiesMessageContainer.style.display = "none";
      }else{
        cookiesMessageContainer.classList.add("fixed-cookie-message");
      }
    } else {
      // La cookie "cookie_accepted" no existe o su valor no es "true", mostrar el componente
      //acceptCookies();
      cookiesMessageContainer.classList.add("fixed-cookie-message");
    }
    showAlert();
  }

  // Función para obtener el valor de una cookie por su nombre
  function getCookieValue(cookieName) {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.startsWith(cookieName + "=")) {
        return cookie.substring(cookieName.length + 1);
      }
    }
    return null;
  }


  function setCookie(name, value, durationInMinutes) {
    var expirationDate = new Date();
    expirationDate.setTime(expirationDate.getTime() + (durationInMinutes * 60 * 1000));
    document.cookie = name + "=" + value + "; expires=" + expirationDate.toUTCString() + "; path=/; Secure; SameSite=Strict";
  }

  // Agrega un event listener para el evento 'DOMContentLoaded' que llama a la función onDocumentLoad
  document.addEventListener("DOMContentLoaded", onDocumentLoad);