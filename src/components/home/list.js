import React, { useEffect, useState } from 'react';
import axios from 'axios';
// import './list_style.css';

const List = () => {
  const [alerts, setAlerts] = useState([]);
  const [email, setEmail] = useState('');

  useEffect(() => {
    const storedEmail = localStorage.getItem('email');
    setEmail(storedEmail);

    const fetchAlerts = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/alerts/list/?email=${storedEmail}`);
        setAlerts(response.data.alerts);
      } catch (error) {
        console.error('Error fetching alerts:', error);
      }
    };

    if (storedEmail) {
      fetchAlerts();
    }
  }, []);

  return (
    <div className="list-container">
      <h1 className="list-title">Hello, {email}</h1>
      <h2 className="list-subtitle">Your Alerts</h2>
      <ul className="alert-list">
        {alerts.map((alert, index) => (
          <li key={index} className="alert-item">
            <span className="alert-value">Alert: ${alert.alert_value}</span>
            <span className="alert-time">Created At: {alert.created_at}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default List;
