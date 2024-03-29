function validateForm() {
    const form = document.getElementById('myForm');
    const inputs = form.querySelectorAll('input, select, textarea');
    let isValid = true;
  
    inputs.forEach(function(input) {
      if (input.hasAttribute('required') && input.value.trim() === '') {
        isValid = false;
        showError(input, 'This field is required.');
      }
  
      if (input.getAttribute('type') === 'email' && !validateEmail(input.value)) {
        isValid = false;
        showError(input, 'Please enter a valid email address.');
      }
    });
  
    return isValid;
  }
  
  function showError(input, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
  
    const parent = input.parentElement;
    parent.appendChild(errorDiv);
  }
  
  function removeError(input) {
    const parent = input.parentElement;
    const errorDiv = parent.querySelector('.error-message');
    if (errorDiv) {
      parent.removeChild(errorDiv);
    }
  }
  
  function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  }
  
  // Usage example:
  // const isValid = validateForm();
  