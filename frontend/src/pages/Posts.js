import React, { useState, useEffect } from 'react';
import { Button, Card, Form, Modal, Badge, Spinner, Table, Alert } from 'react-bootstrap';
import { postsAPI } from '../services/api';
import moment from 'moment';

const Posts = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingPost, setEditingPost] = useState(null);
  const [postData, setPostData] = useState({
    content: '',
    scheduled_at: '',
    crypto_tags: []
  });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const cryptoTagsList = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'ADA', 'DOGE', 'MATIC', 'DOT', 'AVAX'];

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await postsAPI.getPosts(null, 100);
      setPosts(response.data.posts);
    } catch (err) {
      console.error('Error fetching posts:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleShowModal = (post = null) => {
    if (post) {
      setEditingPost(post);
      setPostData({
        content: post.content,
        scheduled_at: post.scheduled_at ? moment(post.scheduled_at).format('YYYY-MM-DDTHH:mm') : '',
        crypto_tags: post.crypto_tags ? post.crypto_tags.split(',') : []
      });
    } else {
      setEditingPost(null);
      setPostData({ content: '', scheduled_at: '', crypto_tags: [] });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingPost(null);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    try {
      const data = {
        content: postData.content,
        scheduled_at: postData.scheduled_at || null,
        crypto_tags: postData.crypto_tags
      };

      if (editingPost) {
        await postsAPI.updatePost(editingPost.id, data);
        setSuccess('Пост успешно обновлен');
      } else {
        await postsAPI.createPost(data);
        setSuccess('Пост успешно создан');
      }

      handleCloseModal();
      fetchPosts();
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка сохранения поста');
    }
  };

  const handlePublishNow = async (postId) => {
    try {
      await postsAPI.publishNow(postId);
      setSuccess('Пост опубликован');
      fetchPosts();
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка публикации');
    }
  };

  const handleDelete = async (postId) => {
    if (window.confirm('Вы уверены, что хотите удалить этот пост?')) {
      try {
        await postsAPI.deletePost(postId);
        setSuccess('Пост удален');
        fetchPosts();
      } catch (err) {
        setError(err.response?.data?.detail || 'Ошибка удаления');
      }
    }
  };

  const handleTagToggle = (tag) => {
    setPostData(prev => ({
      ...prev,
      crypto_tags: prev.crypto_tags.includes(tag)
        ? prev.crypto_tags.filter(t => t !== tag)
        : [...prev.crypto_tags, tag]
    }));
  };

  const getStatusBadge = (status) => {
    const variants = {
      draft: 'secondary',
      scheduled: 'warning',
      published: 'success',
      failed: 'danger'
    };
    const labels = {
      draft: 'Черновик',
      scheduled: 'Запланирован',
      published: 'Опубликован',
      failed: 'Ошибка'
    };
    return <Badge bg={variants[status]}>{labels[status]}</Badge>;
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
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>📝 Посты</h2>
        <Button variant="primary" onClick={() => handleShowModal()}>
          + Новый пост
        </Button>
      </div>

      {error && <Alert variant="danger" onClose={() => setError(null)} dismissible>{error}</Alert>}
      {success && <Alert variant="success" onClose={() => setSuccess(null)} dismissible>{success}</Alert>}

      <Card>
        <Card.Body>
          <Table responsive hover>
            <thead>
              <tr>
                <th>Содержание</th>
                <th>Теги</th>
                <th>Статус</th>
                <th>Запланирован</th>
                <th>Опубликован</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              {posts.map(post => (
                <tr key={post.id}>
                  <td style={{ maxWidth: '300px' }}>
                    {post.content.length > 100 ? post.content.substring(0, 100) + '...' : post.content}
                  </td>
                  <td>
                    {post.crypto_tags && post.crypto_tags.split(',').map(tag => (
                      <Badge bg="info" key={tag} className="me-1">{tag}</Badge>
                    ))}
                  </td>
                  <td>{getStatusBadge(post.status)}</td>
                  <td>{post.scheduled_at ? moment(post.scheduled_at).format('DD.MM.YYYY HH:mm') : '-'}</td>
                  <td>{post.published_at ? moment(post.published_at).format('DD.MM.YYYY HH:mm') : '-'}</td>
                  <td>
                    <Button 
                      size="sm" 
                      variant="outline-primary" 
                      className="me-1"
                      onClick={() => handleShowModal(post)}
                    >
                      ✏️
                    </Button>
                    {post.status !== 'published' && (
                      <Button 
                        size="sm" 
                        variant="outline-success" 
                        className="me-1"
                        onClick={() => handlePublishNow(post.id)}
                      >
                        🚀
                      </Button>
                    )}
                    <Button 
                      size="sm" 
                      variant="outline-danger"
                      onClick={() => handleDelete(post.id)}
                    >
                      🗑️
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      {/* Модальное окно создания/редактирования */}
      <Modal show={showModal} onHide={handleCloseModal} size="lg">
        <Form onSubmit={handleSubmit}>
          <Modal.Header closeButton>
            <Modal.Title>{editingPost ? 'Редактировать пост' : 'Новый пост'}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>Содержание твита</Form.Label>
              <Form.Control
                as="textarea"
                rows={4}
                value={postData.content}
                onChange={(e) => setPostData({...postData, content: e.target.value})}
                maxLength={280}
                required
              />
              <Form.Text className="text-muted">
                {postData.content.length}/280 символов
              </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Крипто-теги</Form.Label>
              <div className="d-flex flex-wrap gap-2 mt-2">
                {cryptoTagsList.map(tag => (
                  <Badge
                    key={tag}
                    bg={postData.crypto_tags.includes(tag) ? 'primary' : 'secondary'}
                    style={{ cursor: 'pointer', padding: '8px 12px' }}
                    onClick={() => handleTagToggle(tag)}
                  >
                    {tag}
                  </Badge>
                ))}
              </div>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Запланировать на</Form.Label>
              <Form.Control
                type="datetime-local"
                value={postData.scheduled_at}
                onChange={(e) => setPostData({...postData, scheduled_at: e.target.value})}
              />
              <Form.Text className="text-muted">
                Оставьте пустым для сохранения как черновик
              </Form.Text>
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleCloseModal}>
              Отмена
            </Button>
            <Button variant="primary" type="submit">
              {editingPost ? 'Сохранить' : 'Создать'}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </div>
  );
};

export default Posts;
