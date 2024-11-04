document.addEventListener('DOMContentLoaded', function () {
    const sections = document.querySelectorAll('.form-section');
    const btnNext = document.querySelector('.btn-next');
    const btnPrev = document.querySelector('.btn-prev');
    let currentStep = 0;

    // Variables para almacenar las selecciones
    let selectedPetType = null;
    let selectedGender = null;

    function showStep(step) {
        sections.forEach((section, index) => {
            section.style.display = (index === step) ? 'block' : 'none';
        });
        btnPrev.style.display = (step === 0) ? 'none' : 'inline-block';

        if (step === sections.length - 1) {
            if (!document.querySelector('.btn-save')) {
                const saveButton = document.createElement('button');
                saveButton.type = 'button';
                saveButton.className = 'btn btn-success btn-save';
                saveButton.innerText = "Guardar";
                saveButton.addEventListener('click', handleSave);
                btnNext.replaceWith(saveButton);
            }
        } else {
            let nextButton = document.querySelector('.btn-next');
            if (!nextButton) {
                nextButton = document.createElement('button');
                nextButton.type = 'button';
                nextButton.className = 'btn btn-primary rounded-circle nav-btn btn-next';
                nextButton.innerHTML = '<i class="bi bi-arrow-right"></i>';
                nextButton.addEventListener('click', nextStep);

                const saveButton = document.querySelector('.btn-save');
                if (saveButton) saveButton.replaceWith(nextButton);
            }
        }
    }

    function validateCurrentStep() {
        const inputs = sections[currentStep].querySelectorAll('input, textarea, select');

        // Validar campos de texto, textarea y select
        for (let input of inputs) {
            if (input.hasAttribute('required') && !input.value) {
                input.classList.add('is-invalid');
                return false;
            } else {
                input.classList.remove('is-invalid');
            }
        }

        // Validar que el tipo de mascota esté seleccionado en el paso correspondiente
        if (currentStep === 0 && !selectedPetType) {
            showError('Por favor, selecciona un tipo de mascota.');
            return false;
        }

        // Validar que el género esté seleccionado en el paso correspondiente
        if (currentStep === 1 && !selectedGender) {
            showError('Por favor, selecciona el género de la mascota.');
            return false;
        }

        return true;
    }

    function nextStep() {
        if (!validateCurrentStep()) {
            return;
        }
        if (currentStep < sections.length - 1) {
            currentStep++;
            showStep(currentStep);
        }
    }

    function prevStep() {
        if (currentStep > 0) {
            currentStep--;
            showStep(currentStep);
        }
    }

    function showError(message) {
        const errorAlert = document.createElement('div');
        errorAlert.className = 'alert alert-danger mt-3';
        errorAlert.innerText = message;
        document.querySelector('.container').appendChild(errorAlert);
        setTimeout(() => errorAlert.remove(), 3000);
    }

    function alertSuccess(message) {
        const successAlert = document.createElement('div');
        successAlert.className = 'alert alert-success mt-3';
        successAlert.innerText = message;
        document.querySelector('.container').appendChild(successAlert);
        setTimeout(() => successAlert.remove(), 3000);
    }

    function handleSave() {
        if (!validateCurrentStep()) {
            showError('Por favor, completa todos los campos requeridos.');
            return;
        }

        alertSuccess('Datos de la mascota guardados con éxito!');

        resetForm();

        setTimeout(() => {
            window.location.reload();
        }, 2000); // 2 segundos de retraso
    }

    function resetForm() {
        const inputs = document.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            if (input.type === 'checkbox' || input.type === 'radio') {
                input.checked = false;
            } else {
                input.value = '';
            }
        });

        document.querySelectorAll('.pet-type-button, .gender-button').forEach(button => {
            button.classList.remove('selected');
        });

        selectedPetType = null;
        selectedGender = null;
    }

    btnNext.addEventListener('click', nextStep);
    btnPrev.addEventListener('click', prevStep);

    document.querySelectorAll('.pet-type-button').forEach(button => {
        button.addEventListener('click', () => selectPetType(button, button.dataset.type));
    });
    document.querySelectorAll('.gender-button').forEach(button => {
        button.addEventListener('click', () => selectGender(button, button.dataset.gender));
    });

    function selectPetType(button, type) {
        selectedPetType = type;
        document.querySelectorAll('.pet-type-button').forEach(btn => btn.classList.remove('selected'));
        button.classList.add('selected');
    }

    function selectGender(button, gender) {
        selectedGender = gender;
        document.querySelectorAll('.gender-button').forEach(btn => btn.classList.remove('selected'));
        button.classList.add('selected');
    }

    showStep(currentStep);
});
