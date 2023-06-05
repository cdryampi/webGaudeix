window.onload = function () {

    function initMap() {
        console.log("hi")
        var ayuntamiento = {
            lat: 41.526067225340036,
            lng: 2.3931021021818424
        };

        var mapOptions = {
            center: ayuntamiento,
            zoom: 10
        };

        var map = new google.maps.Map(document.getElementById('map'), mapOptions);

        var marker = new google.maps.Marker({
            position: ayuntamiento,
            map: map,
            icon: '/static/core/img/icon/ajuntament.png'
        });
        console.log("HI from map.html")
    }
    initMap()
}
