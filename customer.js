// --- Form Toggling Logic ---
document.getElementById("showRegisterBtn").addEventListener("click", function(e) {
    e.preventDefault();
    document.getElementById("loginContainer").style.display = "none";
    document.getElementById("registerContainer").style.display = "block";
});

document.getElementById("showLoginBtn").addEventListener("click", function(e) {
    e.preventDefault();
    document.getElementById("registerContainer").style.display = "none";
    document.getElementById("loginContainer").style.display = "block";
});

// --- Registration Logic ---
document.getElementById("registerForm").addEventListener("submit", function(e) {
    e.preventDefault();
    const name = document.getElementById("regName").value;
    const email = document.getElementById("regEmail").value;
    const password = document.getElementById("regPassword").value;

    fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Account created successfully! You can now log in.");
            document.getElementById("registerForm").reset();
            // Switch back to login view automatically
            document.getElementById("registerContainer").style.display = "none";
            document.getElementById("loginContainer").style.display = "block";
        } else {
            alert("Registration failed: " + data.message);
        }
    })
    .catch(() => alert("Error connecting to the server."));
});

// --- Login Logic ---
document.getElementById("loginForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: username, password: password }) // Now sending real password
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      document.getElementById("loginContainer").style.display = "none";
      document.getElementById("dashboardContainer").style.display = "block";
      document.getElementById("customerName").innerText = username;
      loadCars(); // Fetch available cars once logged in
    } else {
      alert("Login failed: " + data.message);
    }
  })
  .catch(() => alert("Could not connect to server. Is app.py running?"));
});

// --- Logout Logic ---
document.getElementById("logoutBtn").addEventListener("click", function() {
    document.getElementById("loginContainer").style.display = "block";
    document.getElementById("dashboardContainer").style.display = "none";
    document.getElementById("loginForm").reset();
});

// --- Load Real Cars from Database ---
function loadCars() {
    const grid = document.getElementById("carGrid");
    grid.innerHTML = "<p>Loading available cars...</p>"; 

    fetch('/api/cars')
    .then(response => response.json())
    .then(data => {
        if (data.success && data.cars.length > 0) {
            grid.innerHTML = ""; // Clear loading text
            data.cars.forEach(car => {
                const card = document.createElement("div");
                card.className = "car-card";
                
                // Construct the image path pointing to your Flask static folder
                const imagePath = `/static/uploads/${car.image}`;
                
                card.innerHTML = `
                    <img src="${imagePath}" alt="${car.name}" style="width:100%; border-radius: 5px; height: 150px; object-fit: cover; margin-bottom: 10px;">
                    <h4 style="margin: 0;">${car.brand} ${car.name}</h4>
                    <p style="margin: 5px 0; color: #666;">Year: ${car.year}</p>
                    <p style="margin: 5px 0;"><strong>$${car.price_per_day} / day</strong></p>
                    <button style="margin-top: 10px;" onclick="alert('Booking feature for Car ID ${car.id} coming soon!')">Rent Now</button>
                `;
                grid.appendChild(card);
            });
        } else {
            grid.innerHTML = "<p>No cars available right now.</p>";
        }
    })
    .catch(() => {
        grid.innerHTML = "<p>Error loading cars. Please try again later.</p>";
    });
}