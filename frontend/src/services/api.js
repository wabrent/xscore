import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const twitterAPI = {
  createTweet: (text) => api.post('/twitter/tweet', { text }),
  searchTweets: (query, maxResults = 100) => 
    api.get(`/twitter/search?query=${query}&max_results=${maxResults}`),
  getCryptoMentions: (keywords, maxResults = 100) =>
    api.post(`/twitter/crypto-mentions?keywords=${keywords.join(',')}&max_results=${maxResults}`),
};

export const postsAPI = {
  getPosts: (status = null, limit = 50) => 
    api.get(`/posts/${status ? `?status=${status}` : `?limit=${limit}`}`),
  createPost: (data) => api.post('/posts/', data),
  updatePost: (id, data) => api.put(`/posts/${id}`, data),
  deletePost: (id) => api.delete(`/posts/${id}`),
  publishNow: (id) => api.post(`/posts/${id}/publish`),
  schedulePost: (id, scheduledAt) => 
    api.post(`/posts/${id}/schedule?scheduled_at=${scheduledAt}`),
};

export const cryptoAPI = {
  getTopCoins: (limit = 20) => api.get(`/crypto/top-coins?limit=${limit}`),
  getTrending: () => api.get('/crypto/trending'),
  getGlobalData: () => api.get('/crypto/global'),
  getCoinData: (coinId) => api.get(`/crypto/coin/${coinId}`),
  getCoinChart: (coinId, days = 7) => 
    api.get(`/crypto/coin/${coinId}/chart?days=${days}`),
  trackKeywords: (keywords) => 
    api.post(`/crypto/track?keywords=${keywords.join(',')}`),
  getTrends: (limit = 20) => api.get(`/crypto/trends?limit=${limit}`),
};

export const analyticsAPI = {
  getOverview: () => api.get('/analytics/overview'),
  getPostsAnalytics: () => api.get('/analytics/posts'),
  getEngagementMetrics: () => api.get('/analytics/engagement'),
  getCryptoTrends: () => api.get('/analytics/crypto-trends'),
  getTimeline: (days = 30) => api.get(`/analytics/timeline?days=${days}`),
};

export default api;
