import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Spinner, Table, Badge } from 'react-bootstrap';
import { analyticsAPI, cryptoAPI } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [overview, setOverview] = useState(null);
  const [postsStats, setPostsStats] = useState(null);
  const [topCoins, setTopCoins] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [overviewRes, postsRes, coinsRes] = await Promise.all([
          analyticsAPI.getOverview(),
          analyticsAPI.getPostsAnalytics(),
          cryptoAPI.getTopCoins(10)
        ]);
        
        setOverview(overviewRes.data);
        setPostsStats(postsRes.data);
        setTopCoins(coinsRes.data.coins);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2">Загрузка данных...</p>
      </div>
    );
  }

  const pieData = postsStats ? [
    { name: 'Опубликовано', value: postsStats.published_posts, color: '#28a745' },
    { name: 'Запланировано', value: postsStats.scheduled_posts, color: '#ffc107' },
    { name: 'Черновики', value: postsStats.total_posts - postsStats.published_posts - postsStats.scheduled_posts - postsStats.failed_posts, color: '#6c757d' },
    { name: 'Ошибки', value: postsStats.failed_posts, color: '#dc3545' },
  ] : [];

  return (
    <div>
      <h2 className="mb-4">📊 Дашборд</h2>
      
      {/* Карточки статистики */}
      <Row className="mb-4">
        <Col md={3}>
          <Card className="stat-card">
            <Card.Body>
              <Card.Title>Всего постов</Card.Title>
              <div className="metric-value">
                {postsStats?.total_posts || 0}
              </div>
              <small>{postsStats?.recent_posts_7d || 0} за 7 дней</small>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="stat-card-green">
            <Card.Body>
              <Card.Title>Опубликовано</Card.Title>
              <div className="metric-value">
                {postsStats?.published_posts || 0}
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="stat-card-blue">
            <Card.Body>
              <Card.Title>Рынок (24ч)</Card.Title>
              <div className="metric-value" style={{ fontSize: '1.2rem' }}>
                {overview?.market_overview?.total_market_cap?.usd ? 
                  `$${(overview.market_overview.total_market_cap.usd / 1e12).toFixed(2)}T` : 
                  'N/A'}
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="stat-card-orange">
            <Card.Body>
              <Card.Title>Доминация BTC</Card.Title>
              <div className="metric-value">
                {overview?.market_overview?.market_cap_percentage?.btc ? 
                  `${overview.market_overview.market_cap_percentage.btc.toFixed(1)}%` : 
                  'N/A'}
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row>
        {/* График распределения постов */}
        <Col md={6}>
          <Card className="mb-4">
            <Card.Header>📈 Распределение постов</Card.Header>
            <Card.Body>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Card.Body>
          </Card>
        </Col>

        {/* Топ крипто-монеты */}
        <Col md={6}>
          <Card className="mb-4">
            <Card.Header>💰 Топ крипто-монеты</Card.Header>
            <Card.Body>
              <Table striped bordered hover responsive size="sm">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Монета</th>
                    <th>Цена</th>
                    <th>24ч</th>
                  </tr>
                </thead>
                <tbody>
                  {topCoins.map((coin, index) => (
                    <tr key={coin.id}>
                      <td>{index + 1}</td>
                      <td>
                        <img src={coin.image} alt={coin.name} width="20" className="me-2" />
                        {coin.name}
                        <Badge bg="secondary" className="ms-2">{coin.symbol.toUpperCase()}</Badge>
                      </td>
                      <td>${coin.current_price?.toLocaleString()}</td>
                      <td className={coin.price_change_percentage_24h >= 0 ? 'trend-up' : 'trend-down'}>
                        {coin.price_change_percentage_24h?.toFixed(2)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Трендовые монеты */}
      <Row>
        <Col md={12}>
          <Card>
            <Card.Header>🔥 Трендовые крипто</Card.Header>
            <Card.Body>
              <div className="d-flex flex-wrap gap-2">
                {overview?.trending?.map((coin, index) => (
                  <Badge 
                    bg="warning" 
                    text="dark" 
                    key={index}
                    style={{ fontSize: '1rem', padding: '10px 15px' }}
                  >
                    #{index + 1} {coin.item?.name} ({coin.item?.symbol})
                  </Badge>
                ))}
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
