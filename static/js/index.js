// Custom button functionality
document.getElementById('customBtn').addEventListener('click', function() {
    // Remove active class from all buttons
    document.querySelectorAll('.amount-btn').forEach(b => b.classList.remove('active'));
    // Add active class to custom button
    this.classList.add('active');
    // Show custom amount section
    document.getElementById('customAmountSection').style.display = 'block';
    // Focus on input field
    document.getElementById('customAmount').focus();
});

// Amount button selection (for preset amounts)
document.querySelectorAll('.amount-btn').forEach(btn => {
    if(btn.id !== 'customBtn') {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.amount-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            // Hide custom amount section when preset amount is selected
            document.getElementById('customAmountSection').style.display = 'none';
            document.getElementById('customAmount').value = '';
        });
    }
});

// Continue button functionality
document.getElementById('continueBtn').addEventListener('click', function() {
    // Check if custom button is active and custom amount is empty
    const customBtn = document.getElementById('customBtn');
    const customAmount = document.getElementById('customAmount');
    
    if(customBtn.classList.contains('active') && !customAmount.value) {
        alert('Please enter a custom amount');
        customAmount.focus();
        return;
    }
    
    // Validate form fields
    const form = document.getElementById('donationForm');
    if (form.checkValidity()) {
        // remove amount and personal information section
        document.getElementById('amount-per-info').style.display = 'none';
        // Show payment section
        document.getElementById('paymentSection').style.display = 'flex';
        // Smooth scroll to payment section
        document.getElementById('paymentSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
        // Show validation messages
        form.reportValidity();
    }
});

// Anonymous donation toggle
document.getElementById('anonymous').addEventListener('change', function() {
    const donorFields = document.getElementById('donorInfoFields');
    const fields = donorFields.querySelectorAll('input, select');
    const emailField = document.getElementById('email');
    
    if(this.checked) {
        // Keep full opacity - no greying out
        donorFields.style.opacity = '1';
        donorFields.style.pointerEvents = 'auto';
        
        fields.forEach(field => {
            if(field.id !== 'email') {
                // Disable and clear non-email fields
                field.removeAttribute('required');
                field.value = '';
                field.disabled = true;
                field.style.opacity = '0.5';
                field.style.pointerEvents = 'none';
            }
        });
        
        // Email remains active and required
        emailField.disabled = false;
        emailField.setAttribute('required', 'required');
        emailField.style.opacity = '1';
        emailField.style.pointerEvents = 'auto';
        // Auto-focus on email field
        emailField.focus();
        
    } else {
        // Restore all fields
        donorFields.style.opacity = '1';
        donorFields.style.pointerEvents = 'auto';
        
        fields.forEach(field => {
            field.disabled = false;
            field.style.opacity = '1';
            field.style.pointerEvents = 'auto';
        });
        
        // Restore required attributes
        document.getElementById('firstName').setAttribute('required', 'required');
        document.getElementById('lastName').setAttribute('required', 'required');
        document.getElementById('email').setAttribute('required', 'required');
        document.getElementById('phone').setAttribute('required', 'required');
        document.getElementById('country').setAttribute('required', 'required');
    }
});

// Donate Now button
document.getElementById('donateBtn').addEventListener('click', function() {
    alert('Processing payment via Paystack...');
    // Add Paystack integration here
});


// Page Navigation
function showPage(pageName) {
    // Hide all pages
    const pages = document.querySelectorAll('.page-content');
    pages.forEach(page => page.classList.remove('active'));
    
    // Show selected page
    const targetPage = document.getElementById(pageName + 'Page');
    if (targetPage) {
        targetPage.classList.add('active');
    }

    // Reset donate page when it's shown
    if(pageName === 'donate') {
        const paymentSection = document.getElementById('paymentSection');
        const amountPerInfo = document.getElementById('amount-per-info');
        
        if(paymentSection) {
            paymentSection.classList.add('hidden');
        }
        if(amountPerInfo) {
            amountPerInfo.classList.remove('hidden');
            amountPerInfo.style.display = 'flex';
        }
        document.getElementById('donationForm').reset();
        document.querySelectorAll('.amount-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('customAmountSection').style.display = 'none';
    }
    
    // FORCE remove active from EVERYTHING first
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelectorAll('.dropdown-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Now ONLY add active to the parent dropdown
    // Changed pageId to pageName throughout
    if(pageName === 'about' || pageName === 'team') {
        document.getElementById('aboutDropdown').classList.add('active');
    } 
    else if(pageName === 'climate' || pageName === 'water' || pageName === 'environment' || 
            pageName === 'youth' || pageName === 'education' || pageName === 'research') {
        document.getElementById('thematicDropdown').classList.add('active');
    } 
    else if(pageName === 'news' || pageName === 'publications') {
        document.getElementById('resourcesDropdown').classList.add('active');
    } 
    else if(pageName === 'contact' || pageName === 'volunteer' || pageName === 'partners') {
        document.getElementById('touchDropdown').classList.add('active');
    }
    else if(pageName === 'home') {
        document.querySelector('.nav-link[onclick*="home"]').classList.add('active');
    }
    else if(pageName === 'projects') {
        document.querySelector('.nav-link[onclick*="projects"]').classList.add('active');
    }
    else if(pageName === 'media') {
        document.querySelector('.nav-link[onclick*="media"]').classList.add('active');
    }
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Close mobile menu if open
    const navbarCollapse = document.querySelector('.navbar-collapse');
    if (navbarCollapse.classList.contains('show')) {
        navbarCollapse.classList.remove('show');
    }
    
    return false;
}

// Set active state on page load
document.addEventListener('DOMContentLoaded', function() {
    showPage('home');
});


// Scroll to Top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Show/Hide Back to Top Button
window.addEventListener('scroll', function() {
    const backToTop = document.getElementById('backToTop');
    if (window.pageYOffset > 300) {
        backToTop.style.display = 'flex';
    } else {
        backToTop.style.display = 'none';
    }
});

// Contact Form Submission
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        subject: document.getElementById('subject').value,
        message: document.getElementById('message').value
    };

    // Here you would send to Flask backend
    console.log('Contact Form Data:', formData);
    
    // Example Flask endpoint: fetch('/api/contact', { method: 'POST', body: JSON.stringify(formData) })
    
    alert('Thank you for your message! We will get back to you soon.');
    this.reset();
});

// Amount button selection
document.querySelectorAll('.amount-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.amount-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        document.getElementById('customAmount').value = '';
    });
});

// Custom amount input
document.getElementById('customAmount').addEventListener('input', function() {
    if(this.value) {
        document.querySelectorAll('.amount-btn').forEach(b => b.classList.remove('active'));
    }
});




// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        }
    });
});

// Animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards for animation
document.querySelectorAll('.feature-card, .thematic-card, .project-card, .testimonial-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Counter Animation
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target + '+';
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start) + '+';
        }
    }, 16);
}

// Animate stats when visible
const statsObserver = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumbers = entry.target.querySelectorAll('.stat-box h2');
            statNumbers.forEach(stat => {
                const target = parseInt(stat.textContent);
                animateCounter(stat, target);
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const statsSection = document.querySelector('.stats-section');
if (statsSection) {
    statsObserver.observe(statsSection);
}

// Show preloader
function showPreloader() {
  const overlay = document.querySelector('.loading-overlay');
  if (overlay) {
    overlay.style.display = 'flex';
  }
}

// Hide preloader
function hidePreloader() {
  const overlay = document.querySelector('.loading-overlay');
  if (overlay) {
    overlay.style.display = 'none';
  }
}

// Show preloader only on initial page load
let hasLoadedOnce = false;

if (!hasLoadedOnce) {
  showPreloader();
}

// Hide preloader when page is fully loaded
window.addEventListener('load', () => {
  hidePreloader();
  hasLoadedOnce = true;
});

hidePreloader();
