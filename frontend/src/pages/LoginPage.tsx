import React from 'react';

const LOGIN_URL = `${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'}/auth/login`;

const LoginPage: React.FC = () => {
  return (
    <div className="login-page">
      <div className="login-container">
        <h1>Now Chirping 🎵</h1>
        <p>See what your coworkers are listening to on Spotify, in real-time.</p>
        <div className="auth-section">
          <a href={LOGIN_URL} className="login-button">
            Sign in with Spotify
          </a>
        </div>
        <div className="guest-access">
          <a href="/dashboard" className="guest-link">View Dashboard as Guest</a>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
