 Car Rental Management System

## Overview

The Car Rental Management System is a web-based application designed to streamline the operations of a car rental business. The system provides a secure platform for both administrators and users, enabling smooth management, booking, and tracking of rental vehicles. 

## Features

### User Authentication
- **Login System:** Both admins and users can securely log in to the system.
- **Role-Based Access:** Admins have advanced management privileges, while users can view available cars and make rental requests.

### Admin Features
- **Manage Cars:**
  - Add new cars to the system with detailed information (make, model, year, price, etc.).
  - Update existing car details.
  - Delete cars that are no longer available.
- **Rental Records:**
  - View all rental transactions and their statuses.
  - Search and filter rental history by user, car, or rental date.
  - Monitor the availability of cars.
- **User Management:** View registered users and manage their access if required.
- **Reports:** Access summary reports on rentals, car usage, and user activity.

### User Features
- **Browse Cars:** View a list of available cars with detailed specifications and pricing.
- **Book Rentals:** Request to rent a car for specific dates.
- **View Rental History:** See current and past rental records.
- **Profile Management:** Update personal information and view account status.

## Technologies Used
- **Frontend:** (HTML,CSS,JS)
- **Backend:** (FLASK,PYTHON)
- **Database:** (SQLITE)
- **Authentication:** (JWT)

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/car-rental-management-system.git
   cd car-rental-management-system
   ```

2. **Install dependencies:**
   ```sh
   # For backend
   cd backend
   npm install
   # For frontend
   cd ../frontend
   npm install
   ```

3. **Configure environment variables:**  
   Create a `.env` file in both `backend` and `frontend` directories as needed (see `.env.example`).

4. **Start the application:**
   ```sh
   # Start backend
   cd backend
   npm start
   # Start frontend
   cd ../frontend
   npm start
   ```

5. **Access the app:**  
   Open your browser and navigate to `http://localhost:3000` (or your configured port).

### Setting Admin Credentials

To set or change the admin username and password, use the provided `create_admin.py` script:

```sh
python create_admin.py <username> <password>
```

For example, to create an admin user with username `admin` and password `admin123`:

```sh
python create_admin.py admin admin123
```

This script will add the admin user to the database with the password securely hashed.
   npm install

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## Contact

For questions or support, contact [isaacmuraya254@gmail.com].
