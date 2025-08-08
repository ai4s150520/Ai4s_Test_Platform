// static/core/js/take_test_script.js
document.addEventListener('DOMContentLoaded', () => {
    const examForm = document.getElementById('examForm');
    const timerElement = document.getElementById('timer');
    const progressBar = document.getElementById('progressBar');
    const questions = document.querySelectorAll('.question-card');
    const totalQuestions = questions.length;
    
    // Timer
    let timeLeft = parseInt(timerElement.textContent.split(':')[1]) * 60;
    const interval = setInterval(() => {
        if (timeLeft <= 0) {
            clearInterval(interval);
            alert('Time is up! Submitting your answers.');
            examForm.submit();
        } else {
            timeLeft--;
            const minutes = Math.floor(timeLeft / 60);
            let seconds = timeLeft % 60;
            seconds = seconds < 10 ? '0' + seconds : seconds;
            timerElement.textContent = `Time Left: ${minutes}:${seconds}`;
        }
    }, 1000);

    // Progress Bar
    function updateProgressBar() {
        const answeredQuestions = document.querySelectorAll('input[type="radio"]:checked').length;
        const progressPercent = (answeredQuestions / totalQuestions) * 100;
        progressBar.style.width = progressPercent + '%';
    }
    examForm.addEventListener('change', updateProgressBar);
    updateProgressBar(); // Initial check

    // Confirmation Modal
    const submitBtn = document.getElementById('submitBtn');
    const modalBackdrop = document.getElementById('confirmationModalBackdrop');
    const cancelSubmitBtn = document.getElementById('cancelSubmitBtn');
    const confirmSubmitBtn = document.getElementById('confirmSubmitBtn');

    submitBtn.addEventListener('click', (e) => {
        e.preventDefault();
        modalBackdrop.classList.add('visible');
    });

    cancelSubmitBtn.addEventListener('click', () => {
        modalBackdrop.classList.remove('visible');
    });

    confirmSubmitBtn.addEventListener('click', () => {
        examForm.submit();
    });
});