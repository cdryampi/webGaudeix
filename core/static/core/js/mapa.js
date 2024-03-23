function truncateDescription(description, wordCount) {
  // Convertir la descripción en un array de palabras
  const words = description.split(' ');

  // Verificar si la descripción ya tiene menos de `wordCount` palabras
  if (words.length <= wordCount) {
    return description;
  }

  // Obtener las primeras `wordCount` palabras y unirlas nuevamente en una cadena
  const truncatedWords = words.slice(0, wordCount);
  const truncatedDescription = truncatedWords.join(' ');

  // Agregar puntos suspensivos al final de la descripción truncada
  const finalDescription = truncatedDescription + '...';

  return finalDescription;
}

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
    "marker",
  );
  const mapContainer = document.getElementById('map-container');
  const mapLoading = document.getElementById('map-loading');

  fetch('/map/api/map-points/')
    .then(response => response.json())
    .then(data => {
      const map = new Map(mapContainer, {
        center: { lat: 41.5179554, lng: 2.3883919 },
        zoom: 14,
        mapTypeId: 'satellite',
        mapId: "4504f8b37365c3d0"
      });

      data.forEach(point => {
        const marker = new AdvancedMarkerElement({
          position: { lat: point.latitud, lng: point.longitud },
          map: map,
          title: point.titulo,
          content: buildContent(point),
        });
        // Agregar evento de clic al marcador para mostrar el InfoWindow

        marker.addListener('click', ({ domEvent, latLng }) => {
          // Centra el mapa en la posición del marcador cuando se hace clic
          map.panTo(new google.maps.LatLng({ lat: latLng.lat(), lng: latLng.lng() }));

          // Ajusta la vista del mapa para mejorar la visibilidad del marcador
          // Este valor '100' es un ejemplo; ajusta según la necesidad de tu diseño/UI
          map.panBy(0, -180);

          // Activa la lógica de resaltado para el marcador seleccionado
          toggleHighlight(marker, point);
        });

      });

    })
    .catch((error) => {
      //document.getElementById('map-error').style.display = 'block';
      // Ocultar el spinner de carga en caso de error
      //mapLoading.style.display = 'none';
      console.log(error);
    });
}



function toggleHighlight(markerView, property) {
  if (markerView.content.classList.contains("highlight")) {
    markerView.content.classList.remove("highlight");
    markerView.zIndex = null;
  } else {
    markerView.content.classList.add("highlight");
    markerView.zIndex = 1;
  }
}

function buildContent(property) {
  // Crea el contenedor principal para el contenido del marcador.


  const baseURL = `${window.location.protocol}//${window.location.host}`;

  const googleMapsIcon = '<i class="fas fa-map-marked-alt px-1" aria-hidden="true"></i>';
  const internalLinkIcon = '<i class="fas fa-link px-1" aria-hidden="true"></i>';
  
  const content = document.createElement("div");
  content.className = "property";

  // Icono según el tipo de propiedad.
  const iconMapping = {
    patrimoni: "fas fa-landmark",
    jaciments: "fas fa-archway",
    platges: "fas fa-umbrella-beach",
    informació: "fas fa-info-circle",
    // Añade más iconos según necesites.
  };

  // Obtiene la clase del icono basado en el tipo de propiedad.
  const iconClass = iconMapping[property.icono] || "fas fa-question";

  // Crea el contenido HTML dinámico.
  content.innerHTML = `
    <div class="icon">
        <i class="${iconClass}" aria-hidden="true"></i>
    </div>
    <div class="details">
        <div class="address address text-center text-uppercase text-primary h6">${property.titulo}</div>
        <div class="description">${truncateDescription(property.descripcion, 20)}</div>
        <div class="features">
            <div>
                <i class="fas fa-camera fa-lg mb-2" aria-hidden="true" title="image"></i>
                <span class="fa-sr-only">image</span>
                <img src="${property.small_thumbnail_url}" alt="${property.titulo}" style="width: 100%; height: 200px; object-fit: cover;">
            </div>
                <div class="row justify-content-center">
                  ${property.enlace_google_maps ? `<div class="info-window-link py-2">${googleMapsIcon}<a class="link-opacity-100" href="${property.enlace_google_maps}" 
                  target="_blank" rel="noopener noreferrer">Google Maps</a></div>` : ''}
                  <div class="info-window-link py-2">${internalLinkIcon}<a href="${baseURL}/map/${property.slug}/" target="_blank" rel="noopener noreferrer">${property.titulo}</a></div>
                </div>
            </div>
            
        </div>
    </div>
  `;
  setTimeout(() => {
    const links = content.querySelectorAll('a');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.stopPropagation(); // Previene la propagación del evento
            // Opcionalmente, maneja el clic aquí, por ejemplo, abriendo el enlace en una nueva pestaña
            // Esto podría no ser necesario si ya estás usando target="_blank" en tus enlaces
            console.log("click inside");
        });
    });
}, 0);
  return content;
}



function getColorForIcon(icono) {
  switch (icono) {
    case 'platges':
      return '#007BFF'; // Rojo
    case 'informació':
      return '#17A2B8'; // Verde
    case 'jaciments':
      return '#FFC107'; // Azul
    case 'patrimoni':
      return '#6C757D'; // Amarillo
    default:
      return '#000000'; // Negro por defecto
  }
}

window.initMap = initMap;
