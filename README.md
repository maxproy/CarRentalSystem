# Car Rental System

A comprehensive car rental management system designed to streamline vehicle rentals, reservations, and customer management.

## Features

- **Vehicle Management**: Track and manage your rental fleet with detailed vehicle information
- **Customer Management**: Maintain customer profiles and rental history
- **Reservation System**: Easy booking and scheduling of vehicles
- **Billing & Payments**: Automated invoice generation and payment processing
- **Reporting**: Generate detailed rental and financial reports
- **User Authentication**: Secure login and role-based access control

## Prerequisites

Before you begin, ensure you have the following installed:
- Java 11 or higher
- Maven 3.6.0 or higher
- MySQL 5.7 or higher
- Git

## Installation

1. **Clone the repository**  
```bash
git clone https://github.com/maxproy/CarRentalSystem.git
cd CarRentalSystem
```

2. **Configure the database**  
   - Create a MySQL database named `car_rental_db`  
   - Update database credentials in `application.properties` or `application.yml`

3. **Build the project**  
```bash
mvn clean install
```

4. **Run the application**  
```bash
mvn spring-boot:run
```

The application will start on `http://localhost:8080`

## Usage

### Admin Panel
- Access the admin dashboard at `/admin`
- Manage vehicles, customers, and reservations
- View reports and analytics

### Customer Portal
- Create an account or log in at `/login`
- Browse available vehicles
- Make and manage reservations
- View rental history and invoices

## API Endpoints

### Vehicles
- `GET /api/vehicles` - List all vehicles
- `POST /api/vehicles` - Add new vehicle
- `GET /api/vehicles/{id}` - Get vehicle details
- `PUT /api/vehicles/{id}` - Update vehicle
- `DELETE /api/vehicles/{id}` - Delete vehicle

### Reservations
- `GET /api/reservations` - List all reservations
- `POST /api/reservations` - Create new reservation
- `GET /api/reservations/{id}` - Get reservation details
- `PUT /api/reservations/{id}` - Update reservation
- `DELETE /api/reservations/{id}` - Cancel reservation

### Customers
- `GET /api/customers` - List all customers
- `POST /api/customers` - Register new customer
- `GET /api/customers/{id}` - Get customer details
- `PUT /api/customers/{id}` - Update customer

## Configuration

Key configuration options in `application.properties`:

```properties
# Database Configuration
spring.datasource.url=jdbc:mysql://localhost:3306/car_rental_db
spring.datasource.username=root
spring.datasource.password=password

# Server Port
server.port=8080

# JWT Configuration
jwt.secret=your_secret_key
jwt.expiration=86400000
```

## Project Structure

```
CarRentalSystem/
├── src/main/java/
│   ├── controller/      # API controllers
│   ├── service/         # Business logic
│   ├── repository/      # Data access layer
│   ├── model/           # Entity classes
│   └── config/          # Configuration classes
├── src/main/resources/
│   ├── application.properties
│   └── static/          # Frontend resources
├── pom.xml              # Maven dependencies
└── README.md
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@carrentalsystem.com or open an issue in the repository.

## Authors

- **Max Proy** - Initial work - [GitHub Profile](https://github.com/maxproy)

## Acknowledgments

- Spring Boot framework
- MySQL database
- Bootstrap for UI components