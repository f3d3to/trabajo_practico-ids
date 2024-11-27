const borrar = document.getElementById("delete-btn");

borrar.addEventListener("click", (event) => {
    // agregando esto ya funciona
    event.preventDefault();

    Swal.fire({
        title: "¿Está seguro?",
        text: "¿Desea borrar definitivamente?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar",
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = borrar.href;
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            Swal.fire({
                title: "Cancelado",
                text: "No se eliminó la mascota.",
                icon: "error",
            });
        }
    });
});
