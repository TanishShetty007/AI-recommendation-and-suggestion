// Chart wrapper helper class for consistent clean styling
const ChartTheme = {
    colors: {
        primary: '#4361ee',
        secondary: '#7209b7',
        accent: '#f77f00',
        success: '#06d6a0',
        warning: '#ffb703',
        gray: '#94a3b8'
    },
    font: 'Poppins'
};

function renderPriceHistoryChart(canvasId, chartData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    // Destroy existing chart if it exists to prevent overlap issues
    if (window.priceHistoryChartInstance) {
        window.priceHistoryChartInstance.destroy();
    }

    const datasets = [];
    const colors = [ChartTheme.colors.primary, ChartTheme.colors.secondary, ChartTheme.colors.accent, ChartTheme.colors.success, '#f72585'];

    let colorIdx = 0;
    let labelDates = [];

    for (const [platform, history] of Object.entries(chartData)) {
        if (history.length > 0 && labelDates.length === 0) {
            labelDates = history.map(item => item.date);
        }

        datasets.push({
            label: platform,
            data: history.map(item => item.price),
            borderColor: colors[colorIdx % colors.length],
            backgroundColor: 'transparent',
            borderWidth: 3,
            tension: 0.3,
            pointBackgroundColor: colors[colorIdx % colors.length],
            pointRadius: 4,
            pointHoverRadius: 6
        });
        colorIdx++;
    }

    window.priceHistoryChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labelDates,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { family: ChartTheme.font, size: 12 },
                        padding: 20
                    }
                },
                tooltip: {
                    padding: 12,
                    titleFont: { family: ChartTheme.font, weight: 'bold' },
                    bodyFont: { family: ChartTheme.font }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { font: { family: ChartTheme.font } }
                },
                y: {
                    grid: { color: 'rgba(0, 0, 0, 0.05)' },
                    ticks: {
                        font: { family: ChartTheme.font },
                        callback: function (value) {
                            return 'Rs.' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}
