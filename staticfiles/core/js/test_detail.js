document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('testForm');
  const warningMsg = document.getElementById('warningMsg');

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const questions = document.querySelectorAll('.question-card');
    let allAnswered = true;

    warningMsg.style.display = 'none'; // Hide warning initially

    questions.forEach(question => {
      const qid = question.id.split('-')[1];

      // Check MCQ
      const inputs = question.querySelectorAll(`input[name="question_${qid}"]`);
      const textarea = question.querySelector('textarea[name="question_' + qid + '"]');

      let answered = false;
      if (inputs.length > 0) {
        // For MCQ: check if any radio is checked
        answered = Array.from(inputs).some(input => input.checked);
      } else if (textarea) {
        // For text: check if textarea has value
        answered = textarea.value.trim().length > 0;
      }

      if (!answered) {
        allAnswered = false;
        // Highlight unanswered question card
        question.style.borderColor = '#d32f2f';
        question.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } else {
        question.style.borderColor = '#1976d2';
      }
    });

    if (!allAnswered) {
      warningMsg.style.display = 'block';
      return false; // Prevent form submission
    }

    // If all answered, submit form
    form.submit();
  });
});
