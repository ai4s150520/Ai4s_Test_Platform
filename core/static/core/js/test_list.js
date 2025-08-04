document.addEventListener("DOMContentLoaded", () => {
  // Get all the necessary elements from the DOM
  const searchInput = document.getElementById("testSearch");
  const categoryFilter = document.getElementById("categoryFilter");
  const sortFilter = document.getElementById("sortFilter");
  const clearButton = document.getElementById("clearFiltersBtn");
  const testContainer = document.getElementById("testListContainer");
  const allTestCards = Array.from(
    testContainer.getElementsByClassName("test-card")
  );
  const noResultsMessage = document.getElementById("noResultsMessage");

  // The main function that handles filtering and sorting
  const updateTestList = () => {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;
    const sortValue = sortFilter.value;

    // 1. FILTER the cards
    let filteredCards = allTestCards.filter((card) => {
      const title = card.dataset.title.toLowerCase();
      const category = card.dataset.category;

      const matchesSearch = title.includes(searchTerm);
      const matchesCategory =
        selectedCategory === "all" || category === selectedCategory;

      return matchesSearch && matchesCategory;
    });

    // 2. SORT the filtered cards
    filteredCards.sort((a, b) => {
      switch (sortValue) {
        case "title-asc":
          return a.dataset.title.localeCompare(b.dataset.title);
        case "title-desc":
          return b.dataset.title.localeCompare(a.dataset.title);
        case "duration-asc":
          return parseInt(a.dataset.duration) - parseInt(b.dataset.duration);
        case "duration-desc":
          return parseInt(b.dataset.duration) - parseInt(a.dataset.duration);
        default:
          return 0; // No sorting
      }
    });

    // 3. UPDATE THE DOM
    // First, hide all cards
    allTestCards.forEach((card) => (card.style.display = "none"));

    // Then, display the filtered and sorted cards
    if (filteredCards.length > 0) {
      filteredCards.forEach((card) => {
        card.style.display = "flex"; // Use flex to match our CSS
        testContainer.appendChild(card); // This re-orders the elements in the DOM
      });
      noResultsMessage.style.display = "none";
    } else {
      noResultsMessage.style.display = "block";
    }
  };

  // Add event listeners to all controls
  searchInput.addEventListener("input", updateTestList);
  categoryFilter.addEventListener("change", updateTestList);
  sortFilter.addEventListener("change", updateTestList);

  // Functionality for the "Clear" button
  clearButton.addEventListener("click", () => {
    searchInput.value = "";
    categoryFilter.value = "all";
    sortFilter.value = "default";
    updateTestList();
  });

  // Initial call in case the browser remembers old values
  updateTestList();
});
