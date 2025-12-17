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
        document.getElementById('paymentSection').style.display = 'block';
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

function waterPage() {
    // Hide all page content
    document.querySelectorAll('.page-content').forEach(page => {
        page.classList.remove('active');
    });
    
    // Show waterPage
    document.getElementById('waterPage').classList.add('active');
    
    // Scroll to top
    window.scrollTo(0, 0);
}