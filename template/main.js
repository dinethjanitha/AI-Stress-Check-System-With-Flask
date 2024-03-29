// Global variables
const apiUrl = 'https://api.example.com'; // API URL for AJAX requests

// Common functions
function showAlert(message, type) {
  const alertBox = document.getElementById('alert');
  alertBox.textContent = message;
  alertBox.className = `alert ${type}`;
}

function showLoader() {
  const loader = document.getElementById('loader');
  loader.style.display = 'block';
}

function hideLoader() {
  const loader = document.getElementById('loader');
  loader.style.display = 'none';
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
  // Code to run when the page is fully loaded
});

window.addEventListener('load', function() {
  // Code to run when all the external resources have finished loading (e.g., images, scripts)
});

window.addEventListener('resize', function() {
  // Code to handle window resize events
});

// Other common functions and event listeners can be added here

