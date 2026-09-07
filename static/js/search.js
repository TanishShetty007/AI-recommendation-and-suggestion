document.addEventListener('DOMContentLoaded', () => {
    // Search page setup
    initializeComparisonCheckboxes();
});

function getCompareList() {
    const listRaw = localStorage.getItem('compare_ids');
    return listRaw ? listRaw.split(',').filter(id => id).map(Number) : [];
}

function saveCompareList(list) {
    localStorage.setItem('compare_ids', list.join(','));
    updateCompareFloatingButton();
}

function initializeComparisonCheckboxes() {
    const checkboxes = document.querySelectorAll('.compare-checkbox');
    const compareList = getCompareList();

    checkboxes.forEach(chk => {
        const id = Number(chk.dataset.productId);

        // Sync state from localStorage
        if (compareList.includes(id)) {
            chk.checked = true;
        }

        chk.addEventListener('change', (e) => {
            let list = getCompareList();
            if (e.target.checked) {
                if (list.length >= 4) {
                    e.target.checked = false;
                    showToast('You can compare a maximum of 4 products at once.', 'warning');
                    return;
                }
                if (!list.includes(id)) {
                    list.push(id);
                }
            } else {
                list = list.filter(item => item !== id);
            }
            saveCompareList(list);
        });
    });

    updateCompareFloatingButton();
}

function updateCompareFloatingButton() {
    const list = getCompareList();
    const floatingBtn = document.getElementById('floating-compare-btn');
    if (!floatingBtn) return;

    if (list.length > 0) {
        floatingBtn.classList.remove('d-none');
        const badge = floatingBtn.querySelector('.badge');
        if (badge) {
            badge.textContent = list.length;
        }

        // Update link href
        const link = floatingBtn.querySelector('a');
        if (link) {
            link.href = `/compare?ids=${list.join(',')}`;
        }
    } else {
        floatingBtn.classList.add('d-none');
    }
}

// Function to clear comparison list
function clearComparison() {
    localStorage.removeItem('compare_ids');
    const checkboxes = document.querySelectorAll('.compare-checkbox');
    checkboxes.forEach(chk => chk.checked = false);
    updateCompareFloatingButton();
    showToast('Comparison list cleared.', 'info');
}
