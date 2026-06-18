import React from 'react';
import CurrentlyPlaying from '../components/CurrentlyPlaying';
import { Link } from 'react-router-dom';

const DashboardPage: React.FC = () => {
  return (
    <div className="dashboard-page">
      <nav className="top-nav">
        <Link to="/" className="nav-logo">Now Chirping 🎵</Link>
        <Link to="/" className="nav-link">Back to Login</Link>
      </nav>
      <CurrentlyPlaying />
    </div>
  );
};

export default DashboardPage;
