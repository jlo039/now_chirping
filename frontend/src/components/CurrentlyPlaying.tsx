import React, { useEffect, useState } from 'react';
import client from '../api/client';

interface Listener {
  name: string;
  artist: string;
  track: string;
  album_art: string | null;
}

const LOGIN_URL = `${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'}/auth/login`;

const CurrentlyPlaying: React.FC = () => {
  const [listeners, setListeners] = useState<Listener[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchListeners = async () => {
    try {
      const response = await client.get<Listener[]>('/users/currently-playing');
      setListeners(response.data);
      setError(null);
    } catch (err: any) {
      console.error('Error fetching currently playing:', err);
      const message = err.response?.data?.detail || err.message || 'Failed to fetch data';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchListeners();
    const interval = setInterval(fetchListeners, 30000); // Poll every 30 seconds
    return () => clearInterval(interval);
  }, []);

  if (loading && listeners.length === 0) {
    return <div className="loading">Loading listeners...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="dashboard-content">
      {listeners.length === 0 ? (
        <p className="empty-state">No one is listening right now.</p>
      ) : (
        <div className="listeners-grid">
          {listeners.map((listener, index) => (
            <div key={index} className="listener-card">
              {listener.album_art && (
                <img src={listener.album_art} alt={listener.track} className="album-art" />
              )}
              <div className="listener-info">
                <span className="user-name">👤 {listener.name}</span>
                <span className="track-name">{listener.track}</span>
                <span className="artist-name">{listener.artist}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CurrentlyPlaying;
