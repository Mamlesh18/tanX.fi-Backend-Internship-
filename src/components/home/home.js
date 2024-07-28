import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Use useNavigate instead of useHistory
import './home_style.css';

const Home = () => {
  const [email, setEmail] = useState('');
  const [token, setToken] = useState('');
  const [btcPrice, setBtcPrice] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [alert, setAlert] = useState('');
  const [savedAlert, setSavedAlert] = useState(null);
  const navigate = useNavigate(); // Initialize useNavigate

  useEffect(() => {
    const storedEmail = localStorage.getItem('email');
    const storedToken = localStorage.getItem('token');
    if (storedEmail && storedToken) {
      setEmail(storedEmail);
      setToken(storedToken);
    }

    const fetchBtcPrice = async () => {
      try {
        const response = await axios.get('http://localhost:5000/btc-price');
        const currentPrice = response.data.price;
        setBtcPrice(currentPrice);

        if (savedAlert && currentPrice > parseFloat(savedAlert)) {
          await axios.post('http://localhost:5000/submit-data', {
            email,
            alert: savedAlert
          });
        }
      } catch (error) {
        console.error('Error fetching Bitcoin price:', error);
        setError('Error fetching Bitcoin price');
      } finally {
        setLoading(false);
      }
    };

    fetchBtcPrice();

    const interval = setInterval(fetchBtcPrice, 10000);
    return () => clearInterval(interval);
  }, [savedAlert]);

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:5000/alerts/create/', {
        email,
        alert
      });
      setSavedAlert(alert);
      console.log(response.data.message);
    } catch (error) {
      console.error('Error submitting data:', error);
    }
  };

  const handleDelete = async () => {
    try {
      const response = await axios.post('http://localhost:5000/alerts/delete/', {
        email
      });
      setSavedAlert(null);
      console.log(response.data.message);
    } catch (error) {
      console.error('Error deleting alert:', error);
    }
  };

  const navigateToList = () => {
    navigate('/list'); // Use navigate instead of history.push
  };

  return (
    <div className="container">
      <div className="header">
        <h1 className="title">Welcome, {email}</h1>
        {/* <p className="subtitle">Your token: {token}</p> */}
      </div>
      <div className="price-section">
        <h2>Bitcoin Price</h2>
        {loading && <p>Loading...</p>}
        {error && <p>{error}</p>}
        {btcPrice && <p className="price">Current BTC Price: ${btcPrice.toFixed(2)}</p>}
      </div>
      <div className="alert-box">
        <label htmlFor="alertBox" className="alert-label">Alert Box:</label>
        <input
          type="text"
          id="alertBox"
          className="alert-input"
          value={alert}
          onChange={(e) => setAlert(e.target.value)}
        />
        <button onClick={handleSubmit} className="submit-button">Submit Alert</button>
      </div>
      {savedAlert && (
        <div className="alert-display">
          <p>Saved Alert: ${savedAlert}</p>
          <button onClick={handleDelete} className="delete-button">Delete Alert</button>
        </div>
      )}
      <button onClick={navigateToList} className="list-button">View All Alerts</button>
    </div>
  );
};

export default Home;
