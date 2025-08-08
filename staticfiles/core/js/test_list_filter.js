document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('test-search-input');
    const categoryFilter = document.getElementById('category-filter');
    const difficultyFilter = document.getElementById('difficulty-filter');
    const testCards = document.querySelectorAll('.test-card-wrapper');
    const noResultsMessage = document.getElementById('no-results-message');

    function filterTests() {
        const searchQuery = searchInput.value.toLowerCase();
        const selectedCategory = categoryFilter.value.toLowerCase();
        const selectedDifficulty = difficultyFilter.value.toLowerCase();
        let resultsFound = false;

        testCards.forEach(card => {
            const title = card.dataset.title;
            const category = card.dataset.category;
            const difficulty = card.dataset.difficulty;

            const titleMatch = title.includes(searchQuery);
            const categoryMatch = (selectedCategory === 'all') || (category === selectedCategory);
            const difficultyMatch = (selectedDifficulty === 'all') || (difficulty === selectedDifficulty);

            if (titleMatch && categoryMatch && difficultyMatch) {
                card.style.display = 'block';
                resultsFound = true;
            } else {
                card.style.display = 'none';
            }
        });
        noResultsMessage.style.display = resultsFound ? 'none' : 'block';
    }

    searchInput.addEventListener('keyup', filterTests);
    categoryFilter.addEventListener('change', filterTests);
    difficultyFilter.addEventListener('change', filterTests);
});