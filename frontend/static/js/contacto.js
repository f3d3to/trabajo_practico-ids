document.addEventListener('DOMContentLoaded', function () {
    const btnSubmit = document.querySelector('.contact-button');
    const form = document.querySelector('form');
    
    // mostrar error
    function showError(message) {
        const errorAlert = document.createElement('div');
        errorAlert.className = 'alert alert-danger mt-3';
        errorAlert.innerText = message;
        document.querySelector('.contact-form').appendChild(errorAlert);
        setTimeout(() => errorAlert.remove(), 3000);
    }

    // mostrar  exito
    function showSuccess(message) {
        const successAlert = document.createElement('div');
        successAlert.className = 'alert alert-success mt-3';
        successAlert.innerText = message;
        document.querySelector('.contact-form').appendChild(successAlert);
        setTimeout(() => successAlert.remove(), 3000);
    }

    // Función de validación
    function validateForm() {
        const name = document.querySelector('input[name="nombre"]');
        const email = document.querySelector('input[name="email"]');
        const phone = document.querySelector('input[name="telefono"]');
        const subject = document.querySelector('input[name="asunto"]');
        const message = document.querySelector('textarea[name="mensaje"]');
        
        let isValid = true;
        
        //Validaciones
        if (!name.value) {
            showError('Por favor, ingrese su nombre.');
            isValid = false;
        }

        if (!email.value) {
            showError('Por favor, ingrese su correo.');
            isValid = false;
        }

        if (!phone.value) {
            showError('Por favor, ingrese su número de teléfono.');
            isValid = false;
        }

        if (!subject.value) {
            showError('Por favor, ingrese el asunto.');
            isValid = false;
        }

        if (!message.value) {
            showError('Por favor, ingrese su mensaje.');
            isValid = false;
        }

        return isValid;
    }

    // event de submit del formulario
    btnSubmit.addEventListener('click', (event) => {
        event.preventDefault();
        
        if (validateForm()) {
            showSuccess('¡Mensaje enviado con éxito!');
            // se envia formulaio
            setTimeout(() => {
                form.submit();
            }, 2000);
        }
    });
});
