document.addEventListener('DOMContentLoaded', () => {
    // Sync wishlist toggling icons
    initializeWishlistButtons();
});

function initializeWishlistButtons() {
    // Listen for product bookmark buttons
    const wishlistBtns = document.querySelectorAll('.wishlist-toggle-btn');
    wishlistBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const productId = btn.dataset.productId;
            toggleWishlistAPI(productId, btn);
        });
    });
}

function toggleWishlistAPI(productId, btnElement) {
    fetch('/api/wishlist/toggle', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: parseInt(productId) })
    })
        .then(response => {
            if (response.status === 401) {
                showToast('Please login to add to wishlist.', 'warning');
                throw new Error('Unauthorized');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                const icon = btnElement.querySelector('i');
                if (data.added) {
                    btnElement.classList.add('active');
                    if (icon) {
                        icon.className = 'fas fa-heart text-danger';
                    }
                    showToast(data.message || 'Added to Wishlist!', 'success');
                } else {
                    btnElement.classList.remove('active');
                    if (icon) {
                        icon.className = 'far fa-heart';
                    }
                    showToast(data.message || 'Removed from Wishlist.', 'info');
                }
            } else {
                showToast(data.error || 'Something went wrong.', 'danger');
            }
        })
        .catch(error => {
            console.error('Error toggling wishlist:', error);
        });
}

function updateAlertThreshold(productId, inputElement) {
    const targetPrice = parseFloat(inputElement.value);
    if (isNaN(targetPrice) || targetPrice <= 0) {
        showToast('Please enter a valid price threshold.', 'warning');
        return;
    }

    fetch('/api/wishlist/alert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: parseInt(productId),
            target_price: targetPrice,
            is_active: true
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showToast('Price drop alert threshold configured.', 'success');
            } else {
                showToast(data.error || 'Could not update alert settings.', 'danger');
            }
        })
        .catch(error => console.error('Error updating alert:', error));
}

function removeFromWishlistPage(productId, cardElementId) {
    fetch('/api/wishlist/remove', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: parseInt(productId) })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const el = document.getElementById(cardElementId);
                if (el) {
                    el.style.opacity = '0';
                    setTimeout(() => {
                        el.remove();
                        // If no items left, reload to show empty state
                        const items = document.querySelectorAll('.wishlist-item-card');
                        if (items.length === 0) {
                            window.location.reload();
                        }
                    }, 300);
                }
                showToast('Product deleted from wishlist.', 'info');
            } else {
                showToast(data.error || 'Failed to remove product.', 'danger');
            }
        })
        .catch(error => console.error('Error removing item:', error));
}
