
  function initMap() {
    const mapContainer = document.getElementById('map-container');
    const mapLoading = document.getElementById('map-loading');

    fetch('/map/api/map-points/')
      .then(response => response.json())
      .then(data => {
        const map = new google.maps.Map(mapContainer, {
          center: { lat: 41.123456, lng: 2.987654 },
          zoom: 10
        });
        console.log(data)
        data.forEach(point => {
          const marker = new google.maps.Marker({
            position: { lat: point.latitud, lng: point.longitud },
            map: map,
            title: point.titulo
          });
        });

        // Ocultar el spinner de carga
        mapLoading.style.display = 'none';
      })
      .catch(() => {
        document.getElementById('map-error').style.display = 'block';
        // Ocultar el spinner de carga en caso de error
        mapLoading.style.display = 'none';
      });
  }
