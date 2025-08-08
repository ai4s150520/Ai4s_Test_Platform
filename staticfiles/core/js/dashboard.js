document.addEventListener("DOMContentLoaded", () => {
  // --- FEATURE 1: PERFORMANCE CHART ---
  const ctx = document.getElementById("performanceChart");

  // Check if the chart canvas and data exist before creating the chart
  if (
    ctx &&
    typeof attemptLabels !== "undefined" &&
    typeof attemptScores !== "undefined" &&
    attemptLabels.length > 0
  ) {
    new Chart(ctx, {
      type: "line", // A line chart is great for showing trends
      data: {
        labels: attemptLabels, // X-axis labels (e.g., dates)
        datasets: [
          {
            label: "Score %",
            data: attemptScores, // Y-axis data (the scores)
            fill: true,
            backgroundColor: "rgba(0, 123, 255, 0.1)",
            borderColor: "rgba(0, 123, 255, 1)",
            tension: 0.3, // Makes the line slightly curved
            pointBackgroundColor: "rgba(0, 123, 255, 1)",
            pointRadius: 5,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 100, // Scores are percentage based
            ticks: {
              callback: function (value) {
                return value + "%"; // Add a '%' sign to the Y-axis
              },
            },
          },
        },
        plugins: {
          legend: {
            display: false, // Hide the legend as there's only one dataset
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                return `Score: ${context.parsed.y}%`;
              },
            },
          },
        },
      },
    });
  } else if (ctx) {
    // If there's no data, you can show a message on the canvas
    const context = ctx.getContext("2d");
    context.textAlign = "center";
    context.textBaseline = "middle";
    context.font = "16px Arial";
    context.fillText(
      "Take a test to see your performance chart!",
      ctx.width / 2,
      ctx.height / 2
    );
  }

  // --- FEATURE 2: LIVE SEARCH FOR AVAILABLE TESTS ---
  const searchInput = document.getElementById("test-search-input");
  const testList = document.getElementById("available-tests-list");

  if (searchInput && testList) {
    const testItems = testList.getElementsByClassName("test-item");

    searchInput.addEventListener("input", (e) => {
      const searchTerm = e.target.value.toLowerCase();

      // Loop through all the test list items
      Array.from(testItems).forEach((item) => {
        const testTitle = item
          .querySelector(".test-info strong")
          .textContent.toLowerCase();
        const testCategory = item
          .querySelector(".test-info span")
          .textContent.toLowerCase();

        // If the title or category includes the search term, show it. Otherwise, hide it.
        if (
          testTitle.includes(searchTerm) ||
          testCategory.includes(searchTerm)
        ) {
          item.style.display = "flex";
        } else {
          item.style.display = "none";
        }
      });
    });
  }
});
