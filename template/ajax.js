function ajaxRequest(url, method, data, successCallback, errorCallback) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          successCallback(response);
        } else {
          errorCallback(xhr.status);
        }
      }
    };
    
    xhr.send(JSON.stringify(data));
  }
  
  // Usage example:
  // ajaxRequest('https://api.example.com/endpoint', 'GET', null, handleSuccess, handleError);
  
  function handleSuccess(response) {
    // Handle successful AJAX response
  }
  
  function handleError(status) {
    // Handle AJAX error
  }
  