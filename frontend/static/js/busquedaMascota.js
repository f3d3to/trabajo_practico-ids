document.getElementById('buscar').addEventListener('click', function(event) {
    event.preventDefault();

    const especie = document.getElementById('especie').value;
    const nombre = document.getElementById('nombre').value;
    const raza = document.getElementById('raza').value;
    const sexo = document.getElementById('sexo').value;
    const ubicacion = document.getElementById('ubicacion').value;

    let url = '/api/mascotas?';

    if (especie) url += `especie=${especie}&`;
    if (nombre) url += `nombre=${nombre}&`;
    if (raza) url += `raza=${raza}&`;
    if (sexo) url += `sexo=${sexo}&`;
    if (ubicacion && ubicacion !== "") url += `ubicacion=${ubicacion}&`;

    // Elimino el ulltimo &
    url = url.endsWith('&') ? url.slice(0, -1) : url;

    fetch(url, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error al buscar mascotas:', error);
    });
});

//Falta arreglar cosas