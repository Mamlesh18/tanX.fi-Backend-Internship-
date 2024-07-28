import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Home = () => {
  const [email, setEmail] = useState('');
  const [token, setToken] = useState('');
  const [btcPrice, setBtcPrice] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [alert, setAlert] = useState(''); // State for alert box input

  useEffect(() => {
    // Retrieve email and token from localStorage
    const storedEmail = localStorage.getItem('email');
    const storedToken = localStorage.getItem('token');
    if (storedEmail && storedToken) {
      setEmail(storedEmail);
      setToken(storedToken);
    }

    // Fetch Bitcoin price
    const fetchBtcPrice = async () => {
      try {
        const response = await axios.get('http://localhost:5000/btc-price');
        setBtcPrice(response.data.price);
      } catch (error) {
        console.error('Error fetching Bitcoin price:', error);
        setError('Error fetching Bitcoin price');
      } finally {
        setLoading(false);
      }
    };

    fetchBtcPrice();
  }, []);

  return (
    <div>
      <h1>Welcome, {email}</h1>
      <p>Your token: {token}</p>
      <h2>Bitcoin Price</h2>
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
      {btcPrice && <p>Current BTC Price: ${btcPrice.toFixed(2)}</p>}
      
      <div>
        <label htmlFor="alertBox">Alert Box:</label>
        <input
          type="text"
          id="alertBox"
          value={alert}
          onChange={(e) => setAlert(e.target.value)}
        />
      </div>
    </div>
  );
};

export default Home;
