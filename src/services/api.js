// src/services/api.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// Add response interceptor for debugging
apiClient.interceptors.response.use(
  response => {
    console.log('API Response:', response);
    return response;
  },
  error => {
    console.error('API Error:', error);
    console.error('API Error Response:', error.response);
    return Promise.reject(error);
  }
);

// Add a request interceptor to include auth token
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default {
  // Products
  getProducts(params = {}) {
    console.log('API: getProducts called with params:', params);
    console.log('API: Making request to:', apiClient.defaults.baseURL + '/products/');
    console.log('API: Full URL will be:', apiClient.defaults.baseURL + '/products/');
    console.log('API: Request params:', params);
    return apiClient.get('/products/', { params });
  },
  getProduct(id) {
    return apiClient.get(`/products/${id}/`);
  },
  createProduct(data) {
    // Handle FormData for file uploads
    const config = {};
    if (data instanceof FormData) {
      config.headers = {
        'Content-Type': 'multipart/form-data'
      };
    }
    return apiClient.post('/products/', data, config);
  },
  updateProduct(id, data) {
    // Handle FormData for file uploads
    const config = {};
    if (data instanceof FormData) {
      config.headers = {
        'Content-Type': 'multipart/form-data'
      };
    }
    return apiClient.put(`/products/${id}/`, data, config);
  },
  deleteProduct(id) {
    return apiClient.delete(`/products/${id}/`);
  },
  deleteProductImage(productId, imageId) {
    return apiClient.delete(`/products/${productId}/images/${imageId}/`);
  },
  getMyProducts() {
    return apiClient.get('/products/my_products/');
  },

  // Departments
  getDepartments(params = {}) {
    return apiClient.get('/departments/', { params });
  },
  getDepartment(id) {
    return apiClient.get(`/departments/${id}/`);
  },
  getDepartmentBySlug(slug) {
    return apiClient.get(`/departments/?slug=${slug}`);
  },

  // Categories
  getCategories(params = {}) {
    return apiClient.get('/categories/', { params });
  },
  getCategory(id) {
    return apiClient.get(`/categories/${id}/`);
  },
  getCategoryBySlug(slug) {
    return apiClient.get(`/categories/?slug=${slug}`);
  },
  createCategory(data) {
    return apiClient.post('/categories/', data);
  },
  updateCategory(id, data) {
    return apiClient.put(`/categories/${id}/`, data);
  },
  deleteCategory(id) {
    return apiClient.delete(`/categories/${id}/`);
  },

  // Subcategories
  getSubcategories(params = {}) {
    return apiClient.get('/subcategories/', { params });
  },
  getSubcategory(id) {
    return apiClient.get(`/subcategories/${id}/`);
  },
  getSubcategoryBySlug(slug) {
    return apiClient.get(`/subcategories/?slug=${slug}`);
  },

  // Blog Posts
  getBlogPosts(params = {}) {
    console.log('API: getBlogPosts called with params:', params);
    console.log('API: Making request to:', apiClient.defaults.baseURL + '/blog/posts/');
    return apiClient.get('/blog/posts/', { params });
  },
  getBlogPost(slug) {
    return apiClient.get(`/blog/posts/${slug}/`);
  },
  createBlogPost(data) {
    const config = {};
    if (data instanceof FormData) {
      config.headers = {
        'Content-Type': 'multipart/form-data'
      };
    }
    return apiClient.post('/blog/posts/', data, config);
  },
  updateBlogPost(slug, data) {
    const config = {};
    if (data instanceof FormData) {
      config.headers = {
        'Content-Type': 'multipart/form-data'
      };
    }
    return apiClient.put(`/blog/posts/${slug}/`, data, config);
  },
  deleteBlogPost(slug) {
    return apiClient.delete(`/blog/posts/${slug}/`);
  },
  getMyBlogPosts() {
    return apiClient.get('/blog/my-posts/');
  },
  getFeaturedBlogPosts() {
    return apiClient.get('/blog/posts/featured/');
  },
  getRecentBlogPosts() {
    return apiClient.get('/blog/posts/recent/');
  },
  getPopularBlogPosts() {
    return apiClient.get('/blog/posts/popular/');
  },
  getRelatedBlogPosts(slug) {
    return apiClient.get(`/blog/posts/${slug}/related/`);
  },

  // Blog Categories
  getBlogCategories() {
    console.log('API: getBlogCategories called');
    console.log('API: Making request to:', apiClient.defaults.baseURL + '/blog/categories/');
    return apiClient.get('/blog/categories/');
  },
  getBlogCategory(slug) {
    return apiClient.get(`/blog/categories/${slug}/`);
  },
  createBlogCategory(data) {
    return apiClient.post('/blog/categories/', data);
  },
  updateBlogCategory(slug, data) {
    return apiClient.put(`/blog/categories/${slug}/`, data);
  },
  deleteBlogCategory(slug) {
    return apiClient.delete(`/blog/categories/${slug}/`);
  },
  getBlogCategoryPosts(slug) {
    return apiClient.get(`/blog/categories/${slug}/posts/`);
  },

  // Blog Comments
  getBlogPostComments(postSlug) {
    return apiClient.get(`/blog/posts/${postSlug}/comments/`);
  },
  createBlogComment(postSlug, data) {
    return apiClient.post(`/blog/posts/${postSlug}/comment/`, data);
  },

  // Product Comments
  getProductComments(productId) {
    return apiClient.get(`/products/${productId}/comments/`);
  },
  createProductComment(productId, data) {
    return apiClient.post(`/products/${productId}/comment/`, data);
  },

  // Global Search
  globalSearch(query, limit = 10) {
    return apiClient.get('/search/', {
      params: { q: query, limit }
    });
  },

  // Auth
  login(credentials) {
    return apiClient.post('/auth/login/', credentials);
  },
  logout() {
    return apiClient.post('/auth/logout/');
  },
  register(userData) {
    return apiClient.post('/auth/register/', userData);
  },
  getCurrentUser() {
    return apiClient.get('/auth/me/');
  },
  updateProfile(data) {
    const config = {};
    if (data instanceof FormData) {
      config.headers = {
        'Content-Type': 'multipart/form-data'
      };
    }
    return apiClient.put('/auth/profile/update/', data, config);
  },

  // Buyer Dashboard
  getBuyerDashboard() {
    return apiClient.get('/auth/buyer/dashboard/');
  },
  getBuyerOrders() {
    return apiClient.get('/auth/buyer/orders/');
  },
  getBuyerReviews() {
    return apiClient.get('/auth/buyer/reviews/');
  },

  // Seller Dashboard
  getSellerDashboard() {
    return apiClient.get('/auth/seller/dashboard/');
  },
  getSellerOrders() {
    return apiClient.get('/auth/seller/orders/');
  },
  getSellerReviews() {
    return apiClient.get('/auth/seller/reviews/');
  },

  // Seller Ads
  getSellerAds() {
    return apiClient.get('/auth/ads/');
  },
  getSellerAd(id) {
    return apiClient.get(`/auth/ads/${id}/`);
  },
  createSellerAd(data) {
    return apiClient.post('/auth/ads/', data);
  },
  updateSellerAd(id, data) {
    return apiClient.put(`/auth/ads/${id}/`, data);
  },
  deleteSellerAd(id) {
    return apiClient.delete(`/auth/ads/${id}/`);
  },
  uploadAdImage(adId, formData) {
    return apiClient.post(`/auth/ads/${adId}/upload_image/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // Admin Dashboard
  getAdminDashboard() {
    return apiClient.get('/auth/admin/dashboard/');
  },
  getAdminUsers(params = {}) {
    return apiClient.get('/auth/admin/users/', { params });
  },
  adminBlockUser(userId, isBlocked) {
    return apiClient.post(`/auth/admin/users/${userId}/block/`, { is_blocked: isBlocked });
  },
  adminVerifyUser(userId, isVerified) {
    return apiClient.post(`/auth/admin/users/${userId}/verify/`, { is_verified: isVerified });
  },
  adminChangePassword(userId, newPassword) {
    return apiClient.post('/auth/admin/change-password/', {
      user_id: userId,
      new_password: newPassword
    });
  },
  getAdminActivities(params = {}) {
    return apiClient.get('/auth/admin/activities/', { params });
  },
  adminUpdateOrderStatus(orderId, status) {
    return apiClient.put(`/auth/admin/orders/${orderId}/status/`, { status });
  }
}