// ============================================================
// NAVBAR — active state is handled by Flask/Jinja2 in base.html
// ============================================================

// Scroll to Top
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Show/Hide Back to Top Button
window.addEventListener('scroll', function () {
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        backToTop.style.display = window.pageYOffset > 300 ? 'flex' : 'none';
    }
});

// ============================================================
// PRELOADER
// ============================================================
window.addEventListener('load', function () {
    const overlay = document.querySelector('.loading-overlay');
    if (overlay) overlay.classList.add('disappear');
});

// ============================================================
// CONTACT FORM
// ============================================================
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
        // Form posts to Flask — let it submit normally
        // This handler only exists for any additional client-side work
    });
}

// ============================================================
// DONATION PAGE
// ============================================================
(function () {
    // Only run on donation page
    if (!document.getElementById('donationForm')) return;

    let selectedAmount = null;

    // Preset amount buttons
    document.querySelectorAll('.amount-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.amount-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            if (this.dataset.amount === 'custom') {
                document.getElementById('customAmountSection').style.display = 'block';
                document.getElementById('customAmount').focus();
                selectedAmount = null;
            } else {
                document.getElementById('customAmountSection').style.display = 'none';
                document.getElementById('customAmount').value = '';
                selectedAmount = parseFloat(this.dataset.amount);
                updateSummary(selectedAmount);
            }
        });
    });

    // Custom amount input
    const customAmountInput = document.getElementById('customAmount');
    if (customAmountInput) {
        customAmountInput.addEventListener('input', function () {
            const val = parseFloat(this.value);
            selectedAmount = (val >= 1 && val <= 100000) ? val : null;
            updateSummary(selectedAmount);
        });
    }

    // Anonymous checkbox
    const anonymousCheckbox = document.getElementById('anonymous');
    if (anonymousCheckbox) {
        anonymousCheckbox.addEventListener('change', function () {
            const fields = document.getElementById('donorInfoFields');
            const inputs = fields.querySelectorAll('input, select');
            const emailField = document.getElementById('email');

            if (this.checked) {
                inputs.forEach(field => {
                    if (field.id !== 'email') {
                        field.removeAttribute('required');
                        field.value = '';
                        field.disabled = true;
                        field.style.opacity = '0.5';
                    }
                });
                emailField.disabled = false;
                emailField.setAttribute('required', 'required');
                emailField.style.opacity = '1';
                emailField.focus();
            } else {
                inputs.forEach(field => {
                    field.disabled = false;
                    field.style.opacity = '1';
                });
                ['firstName', 'lastName', 'email', 'phone', 'country'].forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.setAttribute('required', 'required');
                });
            }
        });
    }

    // Form submit — validate amount then populate hidden field
    const donationForm = document.getElementById('donationForm');
    if (donationForm) {
        donationForm.addEventListener('submit', function (e) {
            const customVisible = document.getElementById('customAmountSection').style.display !== 'none';
            if (customVisible) {
                selectedAmount = parseFloat(document.getElementById('customAmount').value) || null;
            }
            if (!selectedAmount || selectedAmount < 1) {
                e.preventDefault();
                const errorEl = document.getElementById('amountError');
                if (errorEl) errorEl.style.display = 'block';
                window.scrollTo({ top: 0, behavior: 'smooth' });
                return;
            }
            const errorEl = document.getElementById('amountError');
            if (errorEl) errorEl.style.display = 'none';
            document.getElementById('selectedAmount').value = selectedAmount;
        });
    }

    function updateSummary(amount) {
        const el = document.getElementById('paymentSummary');
        if (!el) return;
        if (amount && amount >= 1) {
            document.getElementById('summaryAmount').textContent =
                'GH₵' + amount.toLocaleString('en-GH', { minimumFractionDigits: 2 });
            el.style.display = 'block';
        } else {
            el.style.display = 'none';
        }
    }
})();

// ============================================================
// SCROLL ANIMATIONS
// ============================================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card, .thematic-card, .project-card, .testimonial-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// ============================================================
// COUNTER ANIMATION (Stats Section)
// ============================================================
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const originalText = element.textContent;
    // Detect if there's a '+' suffix
    const hasPlusSuffix = originalText.includes('+');
    const suffix = hasPlusSuffix ? '+' : '';
    const increment = target / (duration / 16);

    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target + suffix;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start) + suffix;
        }
    }, 16);
}

const statsObserver = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumbers = entry.target.querySelectorAll('.stat-box h2');
            statNumbers.forEach(stat => {
                const raw = stat.textContent.replace(/[^0-9]/g, '');
                const target = parseInt(raw);
                if (!isNaN(target)) animateCounter(stat, target);
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const statsSection = document.querySelector('.stats-section');
if (statsSection) statsObserver.observe(statsSection);

// ============================================================
// SMOOTH SCROLL FOR ANCHOR LINKS
// ============================================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Close mobile navbar when a link is clicked
document.querySelectorAll('.navbar-nav .nav-link, .navbar-nav .dropdown-item').forEach(link => {
    link.addEventListener('click', function () {
        const navbarCollapse = document.querySelector('.navbar-collapse');
        if (navbarCollapse && navbarCollapse.classList.contains('show')) {
            navbarCollapse.classList.remove('show');
        }
    });
});