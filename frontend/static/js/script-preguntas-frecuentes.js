function toggleAnswer(element) {
    // Cambia la clase «activa» en la pregunta seleccionada
    element.classList.toggle("active");
    
    // Obtener el icono y cambiar el texto entre «+» y «-»
    const icon = element.querySelector(".icon");
    icon.textContent = icon.textContent === "+" ? "-" : "+";
}
