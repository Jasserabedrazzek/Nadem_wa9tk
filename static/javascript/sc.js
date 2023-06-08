// Assuming you have a form with the ID "loginForm"
const form = document.getElementById("loginForm");

// Add event listener for form submission
form.addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent the default form submission behavior
  
  // Get the values from the form inputs
  const telephone = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  
  // Create an object to hold the form data
  const formData = {
    telephone: telephone,
    password: password
  };
  
  // Make an AJAX request to the server
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/is_login/" + telephone, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        // Successful login, redirect to home.html
        window.location.href = "/home.html";
      } else {
        // Incorrect telephone number or password, display error message
        alert("Incorrect telephone number or password. Please try again.");
      }
    }
  };
  
  // Send the form data as JSON
  xhr.send(JSON.stringify(formData));
});
