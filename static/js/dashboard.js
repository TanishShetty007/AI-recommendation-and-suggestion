document.addEventListener('DOMContentLoaded', () => {
    // If we are on the dashboard, load charts
    initializeDashboardCharts();
});

function initializeDashboardCharts() {
    const trendsCtx = document.getElementById('searchTrendsChart');
    const categoryCtx = document.getElementById('categoriesChart');

    if (!trendsCtx && !categoryCtx) return;

    fetch('/api/dashboard/analytics')
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                // 1. Search Trends Line Chart
                if (trendsCtx && data.search_trends) {
                    new Chart(trendsCtx, {
                        type: 'line',
                        data: {
                            labels: data.search_trends.labels,
                            datasets: [{
                                label: 'Searches Conducted',
                                data: data.search_trends.data,
                                borderColor: '#4361ee',
                                backgroundColor: 'rgba(67, 97, 238, 0.1)',
                                borderWidth: 3,
                                fill: true,
                                tension: 0.4,
                                pointBackgroundColor: '#4361ee'
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: { display: false }
                            },
                            scales: {
                                x: { grid: { display: false } },
                                y: { beginAtZero: true, grid: { color: 'rgba(0, 0, 0, 0.05)' } }
                            }
                        }
                    });
                }

                // 2. Category Share Doughnut Chart
                if (categoryCtx && data.categories) {
                    new Chart(categoryCtx, {
                        type: 'doughnut',
                        data: {
                            labels: data.categories.labels,
                            datasets: [{
                                data: data.categories.data,
                                backgroundColor: [
                                    '#4361ee', // Mobiles
                                    '#7209b7', // Laptops
                                    '#ffb703', // Electronics
                                    '#06d6a0', // Fashion
                                    '#94a3b8'  // Others
                                ],
                                borderWidth: 0
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    position: 'right',
                                    labels: {
                                        boxWidth: 15,
                                        padding: 15,
                                        font: { family: 'Poppins', size: 12 }
                                    }
                                }
                            },
                            cutout: '75%'
                        }
                    });
                }
            }
        })
        .catch(err => console.error('Database loading error for dashboard details:', err));
}
