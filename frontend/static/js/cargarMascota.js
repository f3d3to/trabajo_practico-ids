document.addEventListener('DOMContentLoaded', function () {
    const sections = document.querySelectorAll('.form-section');
    const btnNext = document.querySelector('.btn-next');
    const btnPrev = document.querySelector('.btn-prev');
    const btnSubmit = document.querySelector('button[type="submit"]');
    let currentStep = 0;

    let selectedPetType = null;
    let selectedGender = null;

    function showStep(step) {
        sections.forEach((section, index) => {
            section.style.display = (index === step) ? 'block' : 'none';
        });

        btnPrev.style.display = (step === 0) ? 'none' : 'inline-block';
        btnNext.style.display = (step === sections.length - 1) ? 'none' : 'inline-block';
        btnSubmit.style.display = (step === sections.length - 1) ? 'inline-block' : 'none';
    }

    function validateCurrentStep() {
        const inputs = sections[currentStep].querySelectorAll('input, select');
        let isValid = true;

        inputs.forEach(input => {
            if (input.hasAttribute('required') && !input.value) {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });

        if (currentStep === 0 && !selectedPetType) {
            showError('Por favor, selecciona un tipo de mascota.');
            isValid = false;
        }

        if (currentStep === 1 && !selectedGender) {
            showError('Por favor, selecciona el género de la mascota.');
            isValid = false;
        }

        return isValid;
    }

    function nextStep() {
        if (validateCurrentStep()) {
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

    function showSuccess(message) {
        const successAlert = document.createElement('div');
        successAlert.className = 'alert alert-success mt-3';
        successAlert.innerText = message;
        document.querySelector('.container').appendChild(successAlert);
        setTimeout(() => successAlert.remove(), 3000);
    }

    function selectPetType(button, type) {
        selectedPetType = type;
        document.querySelector('input[name="especie"]').value = type;
        document.querySelectorAll('.form-section:nth-child(1) .btn-outline-secondary').forEach(btn => btn.classList.remove('selected'));
        button.classList.add('selected');
    }

    function selectGender(button, gender) {
        selectedGender = gender;
        document.querySelector('input[name="genero"]').value = gender;
        document.querySelectorAll('.form-section:nth-child(2) .btn-outline-secondary').forEach(btn => btn.classList.remove('selected'));
        button.classList.add('selected');
    }

    btnNext.addEventListener('click', nextStep);
    btnPrev.addEventListener('click', prevStep);

    document.querySelectorAll('.form-section:nth-child(1) .btn-outline-secondary').forEach(button => {
        const type = button.querySelector('input[name="especie"]').value;
        button.addEventListener('click', () => selectPetType(button, type));
    });

    document.querySelectorAll('.form-section:nth-child(2) .btn-outline-secondary').forEach(button => {
        const gender = button.querySelector('input[name="genero"]').value;
        button.addEventListener('click', () => selectGender(button, gender));
    });

    showStep(currentStep);

    btnSubmit.addEventListener('click', (event) => {
        event.preventDefault();
        if (validateCurrentStep()) {
            showSuccess('Datos guardados con éxito!');
            setTimeout(() => {
                document.querySelector('form').submit();
            }, 2000);
        }
    });
});
