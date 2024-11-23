const borrar = document.getElementById("delete-btn")

borrar.addEventListener("click", () =>
    Swal.fire
({
        title: "seguro",
        text: "desea borrar definitivamente?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText:"si",
        cancelButtonText: "no, me equivoque"
    }).then((result) => 
        {
        if (result.isConfirmed) {
            window.location.href = borrar.getAttribute("href")
            Swal.fire({
                title: "¡Borrado!",
                text: "Se ha borrado",
                icon: "success"
            })
        } 
        else if (result.dismiss === Swal.DismissReason.cancel) {
            Swal.fire({
                title: "Cancelado",
                text: "No se eliminó :)",
                icon: "error"
            })
        }
    })
)