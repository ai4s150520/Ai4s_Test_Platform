// static/core/js/manage_test_script.js

document.addEventListener('DOMContentLoaded', function () {
    /**
     * Accordion functionality: Opens one item, closes others.
     */
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const currentItem = header.parentElement;
            const isAlreadyActive = currentItem.classList.contains('active');

            // Deactivate all accordion items
            document.querySelectorAll('.accordion-item').forEach(item => {
                item.classList.remove('active');
                item.querySelector('.accordion-header').setAttribute('aria-expanded', 'false');
            });

            // If the clicked item wasn't already open, open it.
            if (!isAlreadyActive) {
                currentItem.classList.add('active');
                header.setAttribute('aria-expanded', 'true');
            }
        });
    });

    /**
     * Toggles the visibility of the panel for adding a single question.
     */
    const addQuestionBtn = document.getElementById('addQuestionBtn');
    const addQuestionPanel = document.getElementById('addQuestionPanel');
    const cancelBtn = document.getElementById('cancelBtn');

    // Only run this logic if all required elements are on the page
    if (addQuestionBtn && addQuestionPanel && cancelBtn) {
        addQuestionBtn.addEventListener('click', () => {
            addQuestionPanel.classList.add('visible');
            addQuestionPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    
        cancelBtn.addEventListener('click', () => {
            addQuestionPanel.classList.remove('visible');
        });
    }

    /**
     * Adds a confirmation prompt before deleting a single question.
     */
    const deleteQuestionForms = document.querySelectorAll('.delete-form');
    deleteQuestionForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const confirmation = confirm('Are you sure you want to delete this question? This action cannot be undone.');
            if (!confirmation) {
                e.preventDefault(); // Stop the form submission if user clicks "Cancel"
            }
        });
    });
    
    /**
     * Adds a more serious confirmation prompt before deleting an entire test.
     */
    const deleteTestForm = document.getElementById('deleteTestForm');
    if (deleteTestForm) {
        deleteTestForm.addEventListener('submit', function(e) {
            const confirmation = confirm('ARE YOU ABSOLUTELY SURE?\n\nThis will permanently delete the entire test, including all questions, answers, and user results. This action cannot be undone.');
            if (!confirmation) {
                e.preventDefault(); // Stop the form from submitting
            }
        });
    }
});