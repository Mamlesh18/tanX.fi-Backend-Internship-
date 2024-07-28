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
```
## Backend

In the `app.py` file, replace the placeholders for the email password and CoinMarketCap API key with your credentials.

### Run the Flask backend:

```bash
python app.py
```

## Environment Variables
Make sure to set the necessary environment variables for the database connection, email credentials, and API keys.

## SMTP and Mail Automation
The system uses SMTP for sending automated emails when alert conditions are met. Ensure that your SMTP server credentials are correctly configured in the backend.

## API Key
The CoinMarketCap API key is required to fetch real-time Bitcoin prices. Ensure that you have a valid API key and that it is correctly configured in the backend.
![Bitcoin Alert System](images/bitcoin_alert.png)

## Prerequisites
Node.js and npm for the frontend.
Python 3 and Flask for the backend.
PostgreSQL for the database.

## Additional Notes
Ensure that you have the necessary CORS configurations if the frontend and backend are hosted on different domains.
Consider securing your JWT tokens and other sensitive information using environment variables or a secure vault.
Implement rate limiting and error handling for the API requests to handle potential issues with the CoinMarketCap API.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
