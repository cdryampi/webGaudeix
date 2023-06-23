document.addEventListener('DOMContentLoaded', async function() {
    var videosContainer = document.getElementById('videos-container-home');
    var videoLinks;
    var scrollPosition = {
        top: window.pageYOffset || document.documentElement.scrollTop,
        left: window.pageXOffset || document.documentElement.scrollLeft
      };
      

    try {
        var response = await fetch("/api/portada-video/");
        var data = await response.json();
        videoLinks = data.videos;
        console.log(data.videos);
        cargarVideo(0);
    } catch (error) {
        console.error("Error al obtener los enlaces de video:", error);
    }

    function cargarVideo(index) {
        if (index >= videoLinks.length) {
            index = 0; // Vuelve al primer video cuando se haya reproducido el último
        }

        var currentVideoElement = document.createElement('video');
        currentVideoElement.src = videoLinks[index];
        currentVideoElement.controls = false;
        currentVideoElement.loop = false;
        currentVideoElement.muted = true;
        currentVideoElement.playsInline = true;

        currentVideoElement.addEventListener('ended', function() {
            currentVideoElement.style.display = 'none';
            setTimeout(function() {
                videosContainer.removeChild(currentVideoElement);
                cargarVideo(index + 1);

                window.scrollTo(scrollPosition.left, scrollPosition.top);
            }, 500);
        });

        videosContainer.appendChild(currentVideoElement);
        currentVideoElement.play();
        currentVideoElement.style.opacity = 1;

        setTimeout(function() {
            superponerVideo(index + 1);
        }, 500);
    }

    function superponerVideo(index) {
        if (index >= videoLinks.length) {
            index = 0; // Vuelve al primer video cuando se haya reproducido el último
        }

        var nextVideoElement = document.createElement('video');
        nextVideoElement.src = videoLinks[index];
        nextVideoElement.controls = false;
        nextVideoElement.loop = false;
        nextVideoElement.muted = true;
        nextVideoElement.playsInline = true;
        nextVideoElement.style.opacity = 0;

        nextVideoElement.addEventListener('loadedmetadata', function() {
            var currentVideoElement = videosContainer.querySelector('video');
            currentVideoElement.style.display = 'none';
            setTimeout(function() {
                videosContainer.removeChild(currentVideoElement);
                currentVideoElement = nextVideoElement;
                nextVideoElement = null;
            }, 500);

            // Restaurar la posición de desplazamiento
            window.scrollTo(scrollPosition.left, scrollPosition.top);
        });

        nextVideoElement.addEventListener('ended', function() {
            superponerVideo(index + 1);
        });

        nextVideoElement.load();
        videosContainer.appendChild(nextVideoElement);
        nextVideoElement.play();
        nextVideoElement.style.opacity = 1;
    }
    
    window.addEventListener('scroll', function() {
        scrollPosition.top = window.pageYOffset || document.documentElement.scrollTop;
        scrollPosition.left = window.pageXOffset || document.documentElement.scrollLeft;
    });
});
