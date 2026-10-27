// Dashboard chart palette matching brand colors:
// Primary:   #F3E308 (Yellow)
// Secondary: #6C8494 (Steel Blue-Grey)
// Accent:    #B8BFC1 (Silver)
// Dark Base: #2C4C5C (Teal-Navy)

document.addEventListener('DOMContentLoaded', () => {
    initializeDashboardCharts();
});

function initializeDashboardCharts() {
    const trendsCtx = document.getElementById('searchTrendsChart');
    const categoryCtx = document.getElementById('categoriesChart');

    // Bail out early if neither canvas exists
    if (!trendsCtx && !categoryCtx) return;

    fetch('/api/dashboard/analytics')
        .then(res => {
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json();
        })
        .then(data => {
            if (data.status !== 'success') {
                console.warn('Dashboard analytics: unexpected status', data.status);
                return;
            }

            // ── 1. Search Trends Line Chart ──────────────────────
            if (trendsCtx && data.search_trends) {
                new Chart(trendsCtx, {
                    type: 'line',
                    data: {
                        labels: data.search_trends.labels,
                        datasets: [{
                            label: 'Searches',
                            data: data.search_trends.data,
                            borderColor: '#2C4C5C',
                            backgroundColor: 'rgba(243, 227, 8, 0.15)',
                            borderWidth: 2.5,
                            fill: true,
                            tension: 0.45,
                            pointBackgroundColor: '#F3E308',
                            pointBorderColor: '#2C4C5C',
                            pointBorderWidth: 2,
                            pointRadius: 5,
                            pointHoverRadius: 7
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                backgroundColor: '#2C4C5C',
                                titleColor: '#F3E308',
                                bodyColor: '#B8BFC1',
                                borderColor: 'rgba(243, 227, 8, 0.3)',
                                borderWidth: 1,
                                padding: 10,
                                cornerRadius: 8
                            }
                        },
                        scales: {
                            x: {
                                grid: { display: false },
                                ticks: {
                                    font: { family: 'Poppins', size: 11 },
                                    color: '#6C8494'
                                }
                            },
                            y: {
                                beginAtZero: true,
                                grid: { color: 'rgba(108, 132, 148, 0.1)' },
                                ticks: {
                                    font: { family: 'Poppins', size: 11 },
                                    color: '#6C8494',
                                    stepSize: 5
                                }
                            }
                        }
                    }
                });
            }

            // ── 2. Category Doughnut Chart ────────────────────────
            if (categoryCtx && data.categories) {
                new Chart(categoryCtx, {
                    type: 'doughnut',
                    data: {
                        labels: data.categories.labels,
                        datasets: [{
                            data: data.categories.data,
                            backgroundColor: [
                                '#F3E308',   // Primary Yellow  – Mobiles
                                '#2C4C5C',   // Dark Teal-Navy  – Laptops
                                '#6C8494',   // Steel Blue-Grey – Electronics
                                '#B8BFC1',   // Silver          – Fashion
                                '#a0a8ab'    // Muted Silver    – Others
                            ],
                            borderWidth: 0,
                            hoverOffset: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'right',
                                labels: {
                                    boxWidth: 13,
                                    padding: 14,
                                    font: { family: 'Poppins', size: 11 },
                                    color: '#2C4C5C'
                                }
                            },
                            tooltip: {
                                backgroundColor: '#2C4C5C',
                                titleColor: '#F3E308',
                                bodyColor: '#B8BFC1',
                                borderColor: 'rgba(243, 227, 8, 0.3)',
                                borderWidth: 1,
                                padding: 10,
                                cornerRadius: 8,
                                callbacks: {
                                    label: (ctx) => ` ${ctx.label}: ${ctx.parsed}%`
                                }
                            }
                        },
                        cutout: '72%'
                    }
                });
            }
        })
        .catch(err => {
            console.error('Dashboard analytics fetch error:', err);
            // Render empty state placeholders so the page doesn't break
            [trendsCtx, categoryCtx].forEach(ctx => {
                if (ctx) {
                    ctx.parentElement.innerHTML =
                        '<p class="text-center text-secondary py-4" style="font-size:0.85rem;">' +
                        '<i class="fas fa-exclamation-circle me-1"></i>Could not load chart data.</p>';
                }
            });
        });
}
