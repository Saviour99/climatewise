// Anonymous donation toggle
document.getElementById('anonymous').addEventListener('change', function() {
    const donorFields = document.getElementById('donorInfoFields');
    const fields = donorFields.querySelectorAll('input, select');
    
    if(this.checked) {
        donorFields.style.opacity = '0.5';
        donorFields.style.pointerEvents = 'none';
        fields.forEach(field => {
            field.removeAttribute('required');
            field.value = '';
            field.disabled = true;
        });
        
    } else {
        donorFields.style.opacity = '1';
        donorFields.style.pointerEvents = 'auto';
        fields.forEach(field => {
            field.disabled = false;
        });
        document.getElementById('firstName').setAttribute('required', 'required');
        document.getElementById('lastName').setAttribute('required', 'required');
        document.getElementById('email').setAttribute('required', 'required');
        document.getElementById('country').setAttribute('required', 'required');
    }
});

// Form submission
document.getElementById('donationForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const isAnonymous = document.getElementById('anonymous').checked;
    if(isAnonymous) {
        alert('Thank you for your generous anonymous donation! Redirecting to payment...');
    } else {
        alert('Thank you for your generous donation! Redirecting to payment...');
    }
});
