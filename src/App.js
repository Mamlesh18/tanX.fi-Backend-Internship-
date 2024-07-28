// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/login/user_login';
import Signup from './components/signup/signup';
import Home from './components/home/home'; // Create a Home component for the landing page
import List from './components/home/list'; // Create a Home component for the landing page

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/signup" element={<Signup />} />
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home />} /> {/* Add the home page route */}
        <Route path="/list" element={<List />} /> {/* Add the home page route */}

      </Routes>
    </Router>
  );
}

export default App;
