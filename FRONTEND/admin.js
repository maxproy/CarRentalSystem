// Consolidated admin.js with unified login and form submission logic

document.getElementById("loginForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  // Remove client-side hardcoded check, rely on backend validation
  fetch('/api/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Store username in localStorage for session management
      localStorage.setItem("adminUsername", username);
      // Optionally, store a session flag instead of password
      localStorage.setItem("isAdminLoggedIn", "true");
      document.getElementById("loginContainer").style.display = "none";
      document.getElementById("adminContainer").style.display = "block";
    } else {
      alert("Invalid username or password");
    }
  })
  .catch(() => {
    alert("Error during login.");
  });
});

function showForm(formId) {
  const forms = document.querySelectorAll(".form-container");
  forms.forEach((form) => (form.style.display = "none"));
  document.getElementById(formId).style.display = "block";
}

// Manage Cars Form Submission
document.getElementById("carForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const name = document.getElementById("carModel").value;
  const brand = document.getElementById("carBrand").value;
  const year = document.getElementById("carYear").value;
  const price_per_day = document.getElementById("carPrice").value;
  const image = document.getElementById("carPhoto").value; // For simplicity, just filename

  const formData = new FormData();
  formData.append('name', name);
  formData.append('brand', brand);
  formData.append('year', year);
  formData.append('price_per_day', price_per_day);
  formData.append('image', image);

  fetch('/api/cars', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert(`Car Added: ${name} (${brand}), Year: ${year}, Price: $${price_per_day}/day`);
      document.getElementById("carForm").reset();
    } else {
      alert("Failed to add car: " + data.message);
    }
  })
  .catch(() => {
    alert("Error adding car.");
  });
});

// Manage Users Form Submission
document.getElementById("userForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const name = document.getElementById("userName").value;
  const email = document.getElementById("userEmail").value;
  const password = document.getElementById("userPassword").value;

  fetch('/api/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name, email, password })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert(`User Added: ${name}, Email: ${email}`);
      document.getElementById("userForm").reset();
    } else {
      alert("Failed to add user: " + data.message);
    }
  })
  .catch(() => {
    alert("Error adding user.");
  });
});

// Manage Rentals Form Submission
document.getElementById("rentalForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const car_id = document.getElementById("rentalCarId").value;
  const user_id = document.getElementById("rentalUserId").value;
  const start_date = document.getElementById("rentalStartDate").value;
  const end_date = document.getElementById("rentalEndDate").value;

  fetch('/api/rentals', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ car_id, user_id, start_date, end_date })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert(`Rental Added: Car ID: ${car_id}, User ID: ${user_id}, Dates: ${start_date} to ${end_date}`);
      document.getElementById("rentalForm").reset();
    } else {
      alert("Failed to add rental: " + data.message);
    }
  })
  .catch(() => {
    alert("Error adding rental.");
  });
});

// Remove Rental Logic
function removeRental() {
  const rentalId = document.getElementById("rentalCarId").value;
  if (!rentalId) {
    alert("Please enter a Rental ID to remove a rental.");
    return;
  }

  fetch('/api/rentals/' + rentalId, {
    method: 'DELETE'
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert("Rental removed successfully.");
      document.getElementById("rentalForm").reset();
    } else {
      alert("Failed to remove rental: " + data.message);
    }
  })
  .catch(() => {
    alert("Error removing rental.");
  });
}
