# Bitcoin Alert System

This project is a Bitcoin alert system that notifies users when the price of Bitcoin reaches a specified threshold. The frontend is built using React.js, and the backend is developed using Python Flask. PostgreSQL is used as the database, and JWT tokens are used for user authentication. SMTP is employed for sending automated emails.

## Features

### User Authentication
- Users can sign up and log in. User data, including email and password, is stored in the SQL database.
- Upon successful login, a JWT token is generated and stored in local storage, along with the email. This token is used for session management and retrieving user details.

### Real-Time Bitcoin Price
- The system uses the CoinMarketCap API to fetch real-time Bitcoin prices.
- The price data is retrieved via a request method, which returns the output in JSON format. The price section is then extracted and displayed.

### Alert System
- Users can set alert values for Bitcoin prices.
- The system stores these alerts in a separate database table, including the alert value and timestamp.
- The system continuously checks the real-time Bitcoin price against the alert values. If the current price exceeds an alert value, an automated email notification is sent to the user.

## Database Structure

### User Database
- Stores user credentials (username, email, password) for authentication.

### Alert Database
- Stores user alerts, including the alert value and timestamp.

## How to Run

### Frontend
Navigate to the frontend directory:
```bash
cd Frontend/my-app
npm install
npm start
