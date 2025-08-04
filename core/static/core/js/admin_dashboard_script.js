// static/core/js/admin_dashboard_script.js

document.addEventListener('DOMContentLoaded', function () {

    // --- Live Search for Activity Table ---
    const searchInput = document.getElementById('activitySearch');
    const activityTable = document.getElementById('activityTable');
    const tableRows = activityTable.querySelectorAll('tbody tr');
    const noActivityRow = document.getElementById('no-activity-row');

    if (searchInput) {
        searchInput.addEventListener('keyup', function () {
            const searchTerm = searchInput.value.toLowerCase();
            let hasVisibleRows = false;

            tableRows.forEach(row => {
                // Ignore the 'no activity' row if it exists
                if (row.id === 'no-activity-row') return;

                const rowText = row.textContent.toLowerCase();
                if (rowText.includes(searchTerm)) {
                    row.style.display = '';
                    hasVisibleRows = true;
                } else {
                    row.style.display = 'none';
                }
            });

            // Show/hide the 'no activity' row based on search results
            if (noActivityRow && !hasVisibleRows) {
                // If there's a dedicated 'no results' row, you could show it here.
                // For now, we'll just let the table be empty.
            }
        });
    }


    // --- Activity Chart using Chart.js ---
    const ctx = document.getElementById('activityChart');
    if (ctx) {
        // Dummy data - In a real app, you would pass this from your Django view
        // For example, your view could calculate these values and pass them as a JSON string.
        const chartLabels = ['6 days ago', '5 days ago', '4 days ago', '3 days ago', '2 days ago', 'Yesterday', 'Today'];
        const chartData = [5, 9, 3, 5, 2, 3, 10]; // Example: Number of attempts per day

        const isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';
        const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
        const textColor = isDarkMode ? '#ccd6f6' : '#6c757d';

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartLabels,
                datasets: [{
                    label: 'Test Attempts',
                    data: chartData,
                    fill: true,
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    tension: 0.3, // Makes the line smooth
                    pointBackgroundColor: 'rgba(13, 110, 253, 1)',
                    pointBorderColor: '#fff',
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: gridColor },
                        ticks: { color: textColor }
                    },
                    x: {
                        grid: { color: gridColor },
                        ticks: { color: textColor }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

});