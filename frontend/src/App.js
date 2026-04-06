import React, { useState } from 'react';
import { Container, Form, InputGroup, Button, Spinner, Alert } from 'react-bootstrap';
import axios from 'axios';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [profile, setProfile] = useState(null);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setProfile(null);

    try {
      // Здесь будет вызов вашего API для анализа профиля
      const response = await axios.get(`/api/twitter/user/${username}/metrics`);
      setProfile(response.data);
    } catch (err) {
      setError('Не удалось загрузить профиль. Проверьте username.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Навигация */}
      <nav className="nav-bar">
        <div className="nav-content">
          <a href="/" className="logo">CryptoCV</a>
          <div className="nav-links">
            <a href="#features">Features</a>
            <a href="#crypto-trends">Crypto Trends</a>
            <a href="#share">Share CV</a>
          </div>
        </div>
      </nav>

      {/* Главный экран */}
      {!profile && (
        <div className="hero">
          <Container>
            <div className="hero-content">
              <div className="badge-text">POWERED BY TWITTER API</div>
              <h1 className="hero-title">
                THIS IS YOUR<br />
                <span className="gradient-text">CRYPTO TWITTER CV</span>
              </h1>
              <p className="hero-subtitle">
                Analyze your crypto Twitter profile and generate a shareable resume.<br />
                Track your influence, engagement, and crypto presence.
              </p>

              <Form onSubmit={handleAnalyze} className="search-form">
                <InputGroup className="search-input">
                  <InputGroup.Text className="at-sign">@</InputGroup.Text>
                  <Form.Control
                    type="text"
                    placeholder="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="username-input"
                  />
                  <Button type="submit" className="analyze-btn" disabled={loading}>
                    {loading ? (
                      <Spinner animation="border" size="sm" />
                    ) : (
                      <>Analyze <span className="arrow">→</span></>
                    )}
                  </Button>
                </InputGroup>
              </Form>

              {error && <Alert variant="danger" className="error-alert">{error}</Alert>}
            </div>
          </Container>
        </div>
      )}

      {/* Результаты анализа */}
      {profile && (
        <div className="results">
          <Container>
            <Button 
              variant="link" 
              className="back-btn" 
              onClick={() => setProfile(null)}
            >
              ← Back to search
            </Button>

            <div className="profile-card">
              <div className="profile-header">
                <div className="avatar-placeholder">
                  {profile.name?.charAt(0) || username.charAt(0)}
                </div>
                <div className="profile-info">
                  <h2>{profile.name}</h2>
                  <p className="profile-username">@{profile.username}</p>
                </div>
              </div>

              <div className="stats-grid">
                <div className="stat-box">
                  <div className="stat-label">Followers</div>
                  <div className="stat-value">{profile.metrics?.followers_count?.toLocaleString() || 0}</div>
                </div>
                <div className="stat-box">
                  <div className="stat-label">Following</div>
                  <div className="stat-value">{profile.metrics?.following_count?.toLocaleString() || 0}</div>
                </div>
                <div className="stat-box">
                  <div className="stat-label">Tweets</div>
                  <div className="stat-value">{profile.metrics?.tweet_count?.toLocaleString() || 0}</div>
                </div>
                <div className="stat-box">
                  <div className="stat-label">Joined</div>
                  <div className="stat-value">{profile.created_at ? new Date(profile.created_at).getFullYear() : 'N/A'}</div>
                </div>
              </div>
            </div>
          </Container>
        </div>
      )}

      {/* Footer */}
      <footer className="footer">
        <p>Built with ❤️ for Crypto Twitter Community</p>
      </footer>
    </div>
  );
}

export default App;
