document.addEventListener('DOMContentLoaded', () => {
    // Navbar Scroll Effect
    const navbar = document.querySelector('.navbar-custom');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 30) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Scroll Animations (Intersection Observer)
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    if (animateElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated', entry.target.dataset.animation || 'fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        animateElements.forEach(el => observer.observe(el));
    }

    // Auto-dismiss Flash Messages
    const flashes = document.querySelectorAll('.alert-dismissible');
    flashes.forEach(flash => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(flash);
            bsAlert.close();
        }, 5000);
    });
});

// Global Toast Notification Helper
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-white bg-${type} border-0 show m-2`;
    toastEl.role = 'alert';
    toastEl.ariaLive = 'assertive';
    toastEl.ariaAtomic = 'true';

    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    container.appendChild(toastEl);

    // Auto remove from DOM
    setTimeout(() => {
        toastEl.classList.remove('show');
        setTimeout(() => toastEl.remove(), 300);
    }, 4000);
}
