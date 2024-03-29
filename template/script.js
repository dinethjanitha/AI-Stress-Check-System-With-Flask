// Get all navigation links
const navLinks = document.querySelectorAll('nav ul li a');

// Add click event listener to each navigation link
navLinks.forEach(link => {
  link.addEventListener('click', navigateToPage);
});

// Navigate to the selected page
function navigateToPage(event) {
  event.preventDefault();

  // Get the target page from the link's href attribute
  const targetPage = event.target.getAttribute('href');

  // Load the target page
  loadPage(targetPage);
}

// Load the specified page
function loadPage(page) {
  // Create a new XMLHttpRequest object
  const xhr = new XMLHttpRequest();

  // Set up the request
  xhr.open('GET', page, true);

  // Handle the response
  xhr.onload = function() {
    if (xhr.status === 200) {
      // Extract the HTML content from the response
      const responseHtml = xhr.responseText;

      // Replace the current page's content with the new page's content
      document.documentElement.innerHTML = responseHtml;

      // Update the browser history with the new page
      history.pushState({}, '', page);

      // Execute any necessary JavaScript code for the new page
      executePageScripts();
    }
  };

  // Send the request
  xhr.send();
}

// Execute any necessary JavaScript code for the current page
function executePageScripts() {
  // Add your page-specific JavaScript code here
}

// Listen for popstate event (back/forward buttons)
window.addEventListener('popstate', function() {
  // Get the current page from the URL
  const currentPage = window.location.pathname.split('/').pop();

  // Load the current page
  loadPage(currentPage);
});
