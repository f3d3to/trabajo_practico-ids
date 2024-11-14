document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map').setView([-34.6037, -58.3816], 13);

    L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    let marker;

    map.on('click', async function (e) {
        const { lat, lng } = e.latlng;

        try {
            const response = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`);
            const data = await response.json();

            const zona = data.address.suburb || "Zona desconocida";
            const barrio = data.address.neighbourhood || data.address.city || data.address.town || "Barrio desconocido";

            document.getElementById('zonaMascota').value = zona;
            document.getElementById('barrioMascota').value = barrio;
            document.getElementById('latitud').value = lat;
            document.getElementById('longitud').value = lng;

            // Coloca o mueve el marcador en la ubicación solo después de tener todos los datos
            if (marker) {
                marker.setLatLng([lat, lng]);
            } else {
                marker = L.marker([lat, lng]).addTo(map);
            }
        } catch (error) {
            console.error('Error al obtener datos de ubicación:', error);
        }
    });
});
