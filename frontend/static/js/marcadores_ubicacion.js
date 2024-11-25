
document.getElementById('busquedaForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const queryParams = new URLSearchParams();

    formData.forEach((value, key) => {
        if (value) { // Agrega solo si el valor no está vacío
            queryParams.append(key, value);
        }
    });

    const actionUrl = form.action + '?' + queryParams.toString();
    window.location.href = actionUrl;
});

const map = L.map('map').setView([-34.6037, -58.3816], 12);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

function obtenerIconoPorEspecie(especie) {
    let iconUrl;
    switch (especie) {
        case 'perro':
            iconUrl = '/static/images/perro.png';
            break;
        case 'gato':
            iconUrl = '/static/images/gato.png';
            break;
        default:
            iconUrl = '/static/images/bird.png';
            break;
    }

    return L.icon({
        iconUrl: iconUrl,
        iconSize: [38, 38],
        iconAnchor: [19, 38],
        popupAnchor: [0, -38]
    });
}

if (mascotas && Array.isArray(mascotas)) {
    mascotas.forEach(mascota => {
        const { id, latitud, longitud, nombre, especie, raza, estado, color, zona, barrio, informacion_contacto, fecha_publicacion, foto_url} = mascota;

        if (latitud && longitud) {
            const iconoMascota = obtenerIconoPorEspecie(especie);

            const marker = L.marker([latitud, longitud], { icon: iconoMascota }).addTo(map);

            marker.on('click', () => {
                document.getElementById('nombre-mascota-title').textContent = nombre || 'N/A';
                document.getElementById('mascota-foto').src = foto_url || '';
                document.getElementById('mascota-nombre').textContent = nombre || 'N/A';
                document.getElementById('mascota-especie').textContent = especie || 'N/A';
                document.getElementById('mascota-raza').textContent = raza || 'N/A';
                document.getElementById('mascota-estado').textContent = estado || 'N/A';
                document.getElementById('mascota-color').textContent = color || 'N/A';
                document.getElementById('mascota-zona').textContent = zona || 'N/A';
                document.getElementById('mascota-contacto').textContent = informacion_contacto || 'N/A';
                document.getElementById('mascota-barrio').textContent = barrio || 'N/A';
                document.getElementById('mascota-fecha-publicacion').textContent = fecha_publicacion || 'N/A';

                const offcanvas = new bootstrap.Offcanvas(document.getElementById('offcanvasRight'));
                offcanvas.show();
            });
        }
    });
} else {
    console.error("No se encontraron datos de mascotas para mostrar en el mapa.");
}
