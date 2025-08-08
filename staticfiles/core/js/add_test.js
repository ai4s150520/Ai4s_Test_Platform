document.addEventListener('DOMContentLoaded', () => {
    const btnsNext = document.querySelectorAll(".btn-next");
    const btnsPrev = document.querySelectorAll(".btn-prev");
    const progress = document.querySelector(".progress");
    const formSteps = document.querySelectorAll(".form-step");
    const progressSteps = document.querySelectorAll(".progress-step");

    let formStepsNum = 0;

    // "Next" button click handler
    btnsNext.forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            if (validateStep()) {
                formStepsNum++;
                updateFormSteps();
                updateProgressBar();
            }
        });
    });

    // "Previous" button click handler
    btnsPrev.forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            formStepsNum--;
            updateFormSteps();
            updateProgressBar();
        });
    });

    // Updates the form steps (shows/hides them)
    function updateFormSteps() {
        formSteps.forEach(step => {
            step.classList.remove("form-step-active");
        });
        formSteps[formStepsNum].classList.add("form-step-active");
    }

    // Updates the progress bar
    function updateProgressBar() {
        progressSteps.forEach((step, idx) => {
            if (idx < formStepsNum + 1) {
                step.classList.add("progress-step-active");
            } else {
                step.classList.remove("progress-step-active");
            }
        });

        // Update the blue progress line
        const activeSteps = document.querySelectorAll(".progress-step-active");
        const progressWidth = ((activeSteps.length - 1) / (progressSteps.length - 1)) * 100;
        progress.style.width = progressWidth + "%";
    }

    // Basic client-side validation for the current step
    function validateStep() {
        let isValid = true;
        const currentStep = formSteps[formStepsNum];
        const inputs = currentStep.querySelectorAll('input[required], select[required], textarea[required]');

        inputs.forEach(input => {
            // Remove previous error state
            input.classList.remove('input-error');

            if (!input.value.trim()) {
                isValid = false;
                input.classList.add('input-error');
                // You could add a small error message element here if you wanted
            }
        });

        if (!isValid) {
            // Simple alert, but can be replaced with a more elegant notification
            // alert('Please fill out all required fields in this step.');
        }

        return isValid;
    }

    // Add required attributes to form fields from Django for client-side validation
    const djangoForm = document.getElementById('createTestForm');
    const formFields = djangoForm.querySelectorAll('input, select, textarea');
    formFields.forEach(field => {
        // You would need to check which fields are required from your Django form
        // This is a simplified example. For now, let's make title and category required.
        if(field.name === 'title' || field.name === 'category' || field.name === 'duration_in_minutes'){
            field.setAttribute('required', 'required');
        }
    });

});