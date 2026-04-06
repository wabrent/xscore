import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Spinner, Form, Button, Table, Badge } from 'react-bootstrap';
import { analyticsAPI } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';

const Analytics = () => {
  const [loading, setLoading] = useState(true);
  const [postsAnalytics, setPostsAnalytics] = useState(null);
  const [engagementData, setEngagementData] = useState([]);
  const [cryptoTrends, setCryptoTrends] = useState(null);
  const [timelineData, setTimelineData] = useState([]);
  const [daysFilter, setDaysFilter] = useState(30);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [postsRes, engagementRes, trendsRes, timelineRes] = await Promise.all([
          analyticsAPI.getPostsAnalytics(),
          analyticsAPI.getEngagementMetrics(),
          analyticsAPI.getCryptoTrends(),
          analyticsAPI.getTimeline(daysFilter)
        ]);

        setPostsAnalytics(postsRes.data);
        setEngagementData(engagementRes.data.engagement_data || []);
        setCryptoTrends(trendsRes.data);
        
        // Преобразование данных временной шкалы для графика
        const timelineEntries = timelineRes.data.posts_by_day;
        const formattedTimeline = Object.entries(timelineEntries).map(([date, data]) => ({
          date,
          ...data
        })).sort((a, b) => new Date(a.date) - new Date(b.date));
        
        setTimelineData(formattedTimeline);
      } catch (err) {
        console.error('Error fetching analytics:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [daysFilter]);

  if (loading) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" variant="primary" />
      </div>
    );
  }

  const COLORS = ['#28a745', '#ffc107', '#6c757d', '#dc3545'];

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>📈 Аналитика</h2>
        <Form.Group style={{ width: '200px' }}>
          <Form.Label>Период (дни)</Form.Label>
          <Form.Control
            type="number"
            value={daysFilter}
            onChange={(e) => setDaysFilter(Number(e.target.value))}
            min={1}
            max={90}
          />
        </Form.Group>
      </div>

      {/* Общая статистика */}
      <Row className="mb-4">
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>Всего постов</Card.Title>
              <h2 className="text-primary">{postsAnalytics?.total_posts || 0}</h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>Опубликовано</Card.Title>
              <h2 className="text-success">{postsAnalytics?.published_posts || 0}</h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>Запланировано</Card.Title>
              <h2 className="text-warning">{postsAnalytics?.scheduled_posts || 0}</h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>Ошибки</Card.Title>
              <h2 className="text-danger">{postsAnalytics?.failed_posts || 0}</h2>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row>
        {/* График активности постов */}
        <Col md={8}>
          <Card className="mb-4">
            <Card.Header>📊 Активность постов по дням</Card.Header>
            <Card.Body>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={timelineData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="total" stroke="#8884d8" name="Всего" />
                  <Line type="monotone" dataKey="published" stroke="#28a745" name="Опубликовано" />
                  <Line type="monotone" dataKey="failed" stroke="#dc3545" name="Ошибки" />
                </LineChart>
              </ResponsiveContainer>
            </Card.Body>
          </Card>
        </Col>

        {/* Распределение статусов */}
        <Col md={4}>
          <Card className="mb-4">
            <Card.Header>📈 Распределение статусов</Card.Header>
            <Card.Body>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={[
                      { name: 'Опубликовано', value: postsAnalytics?.published_posts || 0 },
                      { name: 'Запланировано', value: postsAnalytics?.scheduled_posts || 0 },
                      { name: 'Черновики', value: (postsAnalytics?.total_posts || 0) - (postsAnalytics?.published_posts || 0) - (postsAnalytics?.scheduled_posts || 0) - (postsAnalytics?.failed_posts || 0) },
                      { name: 'Ошибки', value: postsAnalytics?.failed_posts || 0 }
                    ]}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {COLORS.map((color, index) => (
                      <Cell key={`cell-${index}`} fill={color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Метрики вовлеченности */}
      <Card className="mb-4">
        <Card.Header>❤️ Метрики вовлеченности</Card.Header>
        <Card.Body>
          {engagementData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={engagementData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="tweet_id" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="metrics.like_count" fill="#e1306c" name="Лайки" />
                <Bar dataKey="metrics.retweet_count" fill="#1da1f2" name="Ретвиты" />
                <Bar dataKey="metrics.reply_count" fill="#ffd700" name="Ответы" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-muted text-center">Нет данных о вовлеченности</p>
          )}
        </Card.Body>
      </Card>

      {/* Таблица вовлеченности */}
      {engagementData.length > 0 && (
        <Card className="mb-4">
          <Card.Header>📋 Детальная статистика по постам</Card.Header>
          <Card.Body>
            <Table responsive striped hover>
              <thead>
                <tr>
                  <th>Пост</th>
                  <th>Содержание</th>
                  <th>Лайки</th>
                  <th>Ретвиты</th>
                  <th>Ответы</th>
                  <th>Просмотры</th>
                </tr>
              </thead>
              <tbody>
                {engagementData.map((item, index) => (
                  <tr key={index}>
                    <td><Badge bg="primary">{item.post_id}</Badge></td>
                    <td style={{ maxWidth: '300px' }}>{item.content}</td>
                    <td>❤️ {item.metrics?.like_count || 0}</td>
                    <td>🔄 {item.metrics?.retweet_count || 0}</td>
                    <td>💬 {item.metrics?.reply_count || 0}</td>
                    <td>👁️ {item.metrics?.impression_count || 0}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Card.Body>
        </Card>
      )}

      {/* Крипто-тренды аналитика */}
      {cryptoTrends && (
        <Row>
          <Col md={6}>
            <Card className="mb-4">
              <Card.Header>🔥 Топ по упоминаниям в Twitter</Card.Header>
              <Card.Body>
                <Table responsive>
                  <thead>
                    <tr>
                      <th>Токен</th>
                      <th>Упоминания</th>
                      <th>Цена</th>
                    </tr>
                  </thead>
                  <tbody>
                    {cryptoTrends.top_mentions?.slice(0, 10).map((trend, index) => (
                      <tr key={index}>
                        <td><Badge bg="info">{trend.token_symbol}</Badge></td>
                        <td>{trend.mentions_count}</td>
                        <td>${trend.price_usd?.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </Card.Body>
            </Card>
          </Col>

          <Col md={6}>
            <Card className="mb-4">
              <Card.Header>📈 Топ по изменению цены (24ч)</Card.Header>
              <Card.Body>
                <Table responsive>
                  <thead>
                    <tr>
                      <th>Токен</th>
                      <th>Изменение 24ч</th>
                      <th>Цена</th>
                    </tr>
                  </thead>
                  <tbody>
                    {cryptoTrends.top_price_change?.slice(0, 10).map((trend, index) => (
                      <tr key={index}>
                        <td><Badge bg="warning" text="dark">{trend.token_symbol}</Badge></td>
                        <td className={trend.price_change_24h >= 0 ? 'trend-up' : 'trend-down'}>
                          {trend.price_change_24h?.toFixed(2)}%
                        </td>
                        <td>${trend.price_usd?.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}
    </div>
  );
};

export default Analytics;
