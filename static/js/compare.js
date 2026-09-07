document.addEventListener('DOMContentLoaded', () => {
    // If on compare page, analyze differences
    highlightPricingDifferences();

    // Wire up remove buttons
    const removeButtons = document.querySelectorAll('.remove-compare-btn');
    removeButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = Number(e.currentTarget.dataset.productId);
            removeProductFromComparison(id);
        });
    });
});

function removeProductFromComparison(id) {
    const listRaw = localStorage.getItem('compare_ids');
    if (!listRaw) return;

    let list = listRaw.split(',').filter(x => x).map(Number);
    list = list.filter(item => item !== id);

    localStorage.setItem('compare_ids', list.join(','));

    // Refresh page with new IDs
    if (list.length > 0) {
        window.location.href = `/compare?ids=${list.join(',')}`;
    } else {
        window.location.href = '/search';
    }
}

function highlightPricingDifferences() {
    // Find rows with price cells
    const rows = document.querySelectorAll('.compare-row-specs');

    rows.forEach(row => {
        const specName = row.dataset.specName;
        // If it is Price row, find lowest value and highlight it
        if (specName === 'Price') {
            const cells = row.querySelectorAll('.compare-cell-val');
            let minPrice = Infinity;
            let minCell = null;

            cells.forEach(cell => {
                const text = cell.textContent.replace('Rs.', '').replace(/,/g, '').trim();
                const price = parseFloat(text);

                if (!isNaN(price) && price < minPrice) {
                    minPrice = price;
                    minCell = cell;
                }
            });

            if (minCell) {
                minCell.classList.add('highlight-best-value');
                const badge = document.createElement('span');
                badge.className = 'badge bg-success ms-2';
                badge.innerHTML = '<i class="fas fa-tags me-1"></i>Best Store Deal';
                minCell.appendChild(badge);
            }
        }
    });
}
