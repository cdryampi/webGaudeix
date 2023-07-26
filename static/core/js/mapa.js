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

function initMap() {
  const mapContainer = document.getElementById('map-container');
  const mapLoading = document.getElementById('map-loading');

  fetch('/map/api/map-points/')
    .then(response => response.json())
    .then(data => {
      const map = new google.maps.Map(mapContainer, {
        center: { lat: 41.5179554, lng: 2.3883919 },
        zoom: 14,
        mapTypeId: 'satellite'
      });
      console.log(data);
      data.forEach(point => {

        const marker = new google.maps.Marker({
          position: { lat: point.latitud, lng: point.longitud },
          map: map,
          title: point.titulo,
          icon: {
            path: 'M -1.547 12 l 6.563 -6.609 -1.406 -1.406 -5.156 5.203 -2.063 -2.109 -1.406 1.406 z M 0 0 q 2.906 0 4.945 2.039 t 2.039 4.945 q 0 1.453 -0.727 3.328 t -1.758 3.516 -2.039 3.070 -1.711 2.273 l -0.75 0.797 q -0.281 -0.328 -0.75 -0.867 t -1.688 -2.156 -2.133 -3.141 -1.664 -3.445 -0.75 -3.375 q 0 -2.906 2.039 -4.945 t 4.945 -2.039 z',
            fillColor: getColorForIcon(point.icono),
            fillOpacity: 1,
            strokeWeight: 0,
            rotation: 0,
            scale: 2,
            anchor: new google.maps.Point(0, 20)
          }
        });
        
        const content = `
                        <div class="info-window">
                            <h4 class="info-window-title">${point.titulo}</h4>
                            <p class="info-window-image"><img src="${point.small_thumbnail_url}" alt="${point.titulo}" style="width: 100%; height: 200px; object-fit: cover;"></p>
                            <p class="info-window-description">${truncateDescription(point.descripcion, 20)}</p>
                            <p class="info-window-link">
                              <a href="map/${point.slug}" class="text-danger">Veure més</a>
                            </p>
                        </div>
                          `;

        // Crear el InfoWindow para mostrar el título del marcador
        const infoWindow = new google.maps.InfoWindow({
            content: content
          });


        // Agregar evento de clic al marcador para mostrar el InfoWindow
        marker.addListener('click', () => {
          infoWindow.setContent(infoWindow);
          infoWindow.open(map, marker);
        });

      });

    })
    .catch(() => {
      //document.getElementById('map-error').style.display = 'block';
      // Ocultar el spinner de carga en caso de error
      //mapLoading.style.display = 'none';
      console.log("Error")
    });
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
