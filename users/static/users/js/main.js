document.addEventListener('DOMContentLoaded', function() {
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    const container = document.getElementById('auth-container');

    if (signUpButton) {
        signUpButton.addEventListener('click', () => {
            container.classList.add('right-panel-active');
        });
    }

    if (signInButton) {
        signInButton.addEventListener('click', () => {
            container.classList.remove('right-panel-active');
        });
    }

    // Password visibility toggles
    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const passwordInput = toggle.previousElementSibling;
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                toggle.classList.remove('fa-eye');
                toggle.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                toggle.classList.remove('fa-eye-slash');
                toggle.classList.add('fa-eye');
            }
        });
    });

    // Auto-remove messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.display = 'none';
        }, 5000);
    });
});