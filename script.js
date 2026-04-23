// FIXED: Changed the comma to a parenthesis on the line below
document.addEventListener("DOMContentLoaded", function () {
    
    // Fetch cars from backend API and load dynamically
    const carList = document.getElementById("carList");
    if (carList) {
      fetch('/api/cars')
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            data.cars.forEach(car => {
              const carDiv = document.createElement("div");
              carDiv.className = "car";
              carDiv.innerHTML = `
                <img src="static/uploads/${car.image}" alt="${car.name}">
                <h3>${car.name}</h3>
                <p>$${car.price_per_day}/day</p>
                <button onclick="rentCar(${car.id})">Rent Now</button>
              `;
              carList.appendChild(carDiv);
            });
          } else {
            carList.innerHTML = "<p>Failed to load cars.</p>";
          }
        })
        .catch(() => {
          carList.innerHTML = "<p>Error loading cars.</p>";
        });
    }
    
    // Handle contact form submission with validation
    const contactForm = document.getElementById("contactForm");
    if (contactForm) {
      contactForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const message = document.getElementById("message").value.trim();
    
        if (!name || !email || !message) {
          alert("Please fill in all fields.");
          return;
        }
    
        fetch('/api/contact', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name, email, message })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert(`Thank you, ${name}! Your message has been sent.`);
            contactForm.reset();
          } else {
            alert("Failed to send message: " + data.message);
          }
        })
        .catch(() => {
          alert("Error sending message.");
        });
      });
    }
    
    // Toggle dropdown on button click
    const loginBtn = document.getElementById("loginBtn");
    if (loginBtn) {
      loginBtn.addEventListener("click", function () {
        const dropdownContent = document.querySelector(".dropdown-content");
        if (dropdownContent) {
          dropdownContent.style.display =
            dropdownContent.style.display === "block" ? "none" : "block";
        }
      });
    }
    
    // Close dropdown when clicking outside
    window.addEventListener("click", function (e) {
      if (!e.target.matches(".login-btn")) {
        const dropdownContent = document.querySelector(".dropdown-content");
        if (dropdownContent && dropdownContent.style.display === "block") {
          dropdownContent.style.display = "none";
        }
      }
    });

}); // FIXED: Moved the closing bracket to wrap the entire file properly

// Global function for the buttons
function rentCar(carId) {
    alert(`You have selected car with ID: ${carId}`);
}