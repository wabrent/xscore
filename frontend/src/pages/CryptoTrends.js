import React, { useState, useEffect } from 'react';
import { Card, Form, Button, Table, Badge, Spinner, Alert, Row, Col } from 'react-bootstrap';
import { cryptoAPI, twitterAPI } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';

const CryptoTrends = () => {
  const [topCoins, setTopCoins] = useState([]);
  const [trending, setTrending] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('BTC');
  const [tweets, setTweets] = useState([]);
  const [tracking, setTracking] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [coinsRes, trendingRes] = await Promise.all([
          cryptoAPI.getTopCoins(20),
          cryptoAPI.getTrending()
        ]);
        
        setTopCoins(coinsRes.data.coins);
        setTrending(trendingRes.data.trending);
      } catch (err) {
        console.error('Error fetching crypto data:', err);
        setError('Ошибка загрузки данных о криптовалютах');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleSearch = async () => {
    try {
      setLoading(true);
      const response = await twitterAPI.searchTweets(`$${searchQuery} OR #${searchQuery}`, 50);
      setTweets(response.data.tweets);
    } catch (err) {
      console.error('Error searching tweets:', err);
      setError('Ошибка поиска твитов');
    } finally {
      setLoading(false);
    }
  };

  const handleTrack = async () => {
    try {
      setLoading(true);
      const keywords = searchQuery.split(',').map(k => k.trim());
      const response = await cryptoAPI.trackKeyword(keywords);
      setTracking(response.data.trends);
      setError(null);
    } catch (err) {
      console.error('Error tracking keywords:', err);
      setError('Ошибка отслеживания ключевых слов');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" variant="primary" />
      </div>
    );
  }

  return (
    <div>
      <h2 className="mb-4">💹 Крипто-тренды</h2>

      {error && <Alert variant="danger" onClose={() => setError(null)} dismissible>{error}</Alert>}

      {/* Поиск и отслеживание */}
      <Card className="mb-4">
        <Card.Header>🔍 Поиск и отслеживание</Card.Header>
        <Card.Body>
          <Row>
            <Col md={6}>
              <Form.Group>
                <Form.Label>Поиск твитов по крипто-ключевым словам</Form.Label>
                <div className="d-flex gap-2">
                  <Form.Control
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="BTC, ETH, SOL..."
                  />
                  <Button variant="primary" onClick={handleSearch}>
                    Поиск
                  </Button>
                </div>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group>
                <Form.Label>Отслеживание упоминаний</Form.Label>
                <div className="d-flex gap-2">
                  <Form.Control
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Введите ключевые слова через запятую"
                  />
                  <Button variant="success" onClick={handleTrack}>
                    Отслеживать
                  </Button>
                </div>
              </Form.Group>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      <Row>
        {/* Топ монеты */}
        <Col md={8}>
          <Card className="mb-4">
            <Card.Header>💰 Топ криптовалют по рыночной капитализации</Card.Header>
            <Card.Body>
              <Table responsive hover striped>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Монета</th>
                    <th>Цена (USD)</th>
                    <th>24ч %</th>
                    <th>Объем 24ч</th>
                    <th>Рын. капитализация</th>
                  </tr>
                </thead>
                <tbody>
                  {topCoins.map((coin, index) => (
                    <tr key={coin.id}>
                      <td>{index + 1}</td>
                      <td>
                        <img src={coin.image} alt={coin.name} width="24" className="me-2" />
                        <strong>{coin.name}</strong>
                        <Badge bg="secondary" className="ms-2">{coin.symbol.toUpperCase()}</Badge>
                      </td>
                      <td>${coin.current_price?.toLocaleString()}</td>
                      <td className={coin.price_change_percentage_24h >= 0 ? 'trend-up' : 'trend-down'}>
                        {coin.price_change_percentage_24h?.toFixed(2)}%
                      </td>
                      <td>${coin.total_volume?.toLocaleString()}</td>
                      <td>${coin.market_cap?.toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>

        {/* Трендовые */}
        <Col md={4}>
          <Card className="mb-4">
            <Card.Header>🔥 Трендовые сейчас</Card.Header>
            <Card.Body>
              {trending.map((coin, index) => (
                <div key={index} className="mb-3 p-2 border-bottom">
                  <div className="d-flex align-items-center">
                    <img 
                      src={coin.item?.large} 
                      alt={coin.item?.name} 
                      width="32" 
                      className="me-2" 
                    />
                    <div>
                      <strong>#{index + 1} {coin.item?.name}</strong>
                      <br />
                      <Badge bg="warning" text="dark">{coin.item?.symbol}</Badge>
                      {coin.item?.market_cap_rank && (
                        <Badge bg="info" className="ms-2">Rank: {coin.item.market_cap_rank}</Badge>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Результаты поиска твитов */}
      {tweets.length > 0 && (
        <Card className="mb-4">
          <Card.Header>🐦 Последние твиты по запросу "{searchQuery}"</Card.Header>
          <Card.Body>
            {tweets.slice(0, 10).map((tweet, index) => (
              <Card key={index} className="mb-3">
                <Card.Body>
                  <Card.Text>{tweet.text}</Card.Text>
                  <div className="d-flex justify-content-between text-muted">
                    <small>
                      ❤️ {tweet.public_metrics?.like_count || 0} | 
                      🔄 {tweet.public_metrics?.retweet_count || 0} | 
                      💬 {tweet.public_metrics?.reply_count || 0}
                    </small>
                    <small>
                      {new Date(tweet.created_at).toLocaleString('ru-RU')}
                    </small>
                  </div>
                </Card.Body>
              </Card>
            ))}
          </Card.Body>
        </Card>
      )}

      {/* Результаты отслеживания */}
      {tracking.length > 0 && (
        <Card>
          <Card.Header>📊 Результаты отслеживания</Card.Header>
          <Card.Body>
            <Table responsive>
              <thead>
                <tr>
                  <th>Токен</th>
                  <th>Упоминания</th>
                  <th>Цена (USD)</th>
                </tr>
              </thead>
              <tbody>
                {tracking.map((trend, index) => (
                  <tr key={index}>
                    <td><Badge bg="primary">{trend.token_symbol}</Badge></td>
                    <td>{trend.mentions_count}</td>
                    <td>${trend.price_usd?.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Card.Body>
        </Card>
      )}
    </div>
  );
};

export default CryptoTrends;
