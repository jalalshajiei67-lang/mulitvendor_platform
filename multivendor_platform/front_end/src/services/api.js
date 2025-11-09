// src/services/api.js
import axios from 'axios';

const DEFAULT_DEV_API_URL = 'http://127.0.0.1:8000/api/';
const DEFAULT_PROD_API_URL = '/api/';
const DOCKER_HOSTNAME_REGEX = /backend:8000/gi;
const REQUIRED_ENV_VARS = ['VITE_API_BASE_URL'];
const isBrowser = typeof window !== 'undefined';

const validateEnvironment = () => {
  if (import.meta.env.MODE !== 'production') {
    return;
  }

  const missing = REQUIRED_ENV_VARS.filter(
    (envKey) => !import.meta.env[envKey]
  );

  if (missing.length > 0) {
    console.warn(
      `⚠️ Missing required environment variable(s): ${missing.join(', ')}`
    );
  }
};

const ensureTrailingSlash = (value) =>
  value.endsWith('/') ? value : `${value}/`;

const ensureApiSuffix = (value) => {
  if (value.endsWith('/api/')) {
    return value;
  }
  if (value.endsWith('/api')) {
    return `${value}/`;
  }
  return `${ensureTrailingSlash(value)}api/`;
};

const sanitizeDockerHostname = (value) =>
  value.replace(DOCKER_HOSTNAME_REGEX, '127.0.0.1:8000');

const isValidAbsoluteUrl = (value) => {
  if (!value.startsWith('http')) {
    return true;
  }

  try {
     
    new URL(value);
    return true;
  } catch (error) {
    console.warn(
      `⚠️ Invalid VITE_API_BASE_URL provided (${value}). Falling back to defaults.`,
      error
    );
    return false;
  }
};

const getBaseUrl = () => {
  let baseUrl = import.meta.env.VITE_API_BASE_URL?.trim();

  if (baseUrl && DOCKER_HOSTNAME_REGEX.test(baseUrl)) {
    console.warn(
      '⚠️ Detected Docker hostname "backend:8000" in VITE_API_BASE_URL. Using localhost instead.'
    );
    baseUrl = sanitizeDockerHostname(baseUrl);
  }

  if (baseUrl && !isValidAbsoluteUrl(baseUrl)) {
    baseUrl = undefined;
  }

  if (!baseUrl) {
    baseUrl =
      import.meta.env.MODE === 'production'
        ? DEFAULT_PROD_API_URL
        : DEFAULT_DEV_API_URL;
  }

  if (!baseUrl.startsWith('http')) {
    baseUrl = ensureApiSuffix(ensureTrailingSlash(baseUrl));
  } else {
    baseUrl = ensureApiSuffix(baseUrl);
  }

  if (import.meta.env.MODE !== 'production') {
    console.debug('🔧 API Client baseURL resolved to:', baseUrl);
  }

  return baseUrl;
};

validateEnvironment();

const apiClient = axios.create({
  baseURL: getBaseUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

const requestControllers = new Map();

const safeSerialize = (payload) => {
  if (!payload) {
    return '';
  }

  if (payload instanceof FormData) {
    return '[form-data]';
  }

  if (typeof payload === 'object') {
    try {
      return JSON.stringify(payload, Object.keys(payload).sort());
    } catch (error) {
      console.warn('⚠️ Unable to serialize request payload for deduplication.', error);
      return '[unserializable-object]';
    }
  }

  return String(payload);
};

const createRequestKey = (config) => {
  const method = (config.method || 'GET').toUpperCase();
  const url = `${config.baseURL || ''}${config.url || ''}`;
  const params = safeSerialize(config.params);
  const data = safeSerialize(config.data);
  return `${method}::${url}::${params}::${data}`;
};

const getTimeoutForEndpoint = (endpoint = '') => {
  const timeoutMatrix = [
    { pattern: /\/products\/.+\/images\/|\/upload/gi, timeout: 30000 },
    { pattern: /\/products\/|\/categories\/|\/subcategories\//gi, timeout: 15000 },
    { pattern: /\/auth\/|\/login|\/logout/gi, timeout: 12000 },
  ];

  const match = timeoutMatrix.find(({ pattern }) => pattern.test(endpoint));
  return match ? match.timeout : 10000;
};

const clearPendingRequest = (key) => {
  const controller = requestControllers.get(key);
  if (controller) {
    controller.abort();
    requestControllers.delete(key);
  }
};

apiClient.interceptors.request.use(
  (config) => {
    const token = isBrowser ? localStorage.getItem('authToken') : null;
    if (token) {
      config.headers = {
        ...config.headers,
        Authorization: `Token ${token}`,
      };
    }

    config.timeout = getTimeoutForEndpoint(config.url);

    const requestKey = createRequestKey(config);
    clearPendingRequest(requestKey);

    const controller = new AbortController();
    config.signal = controller.signal;
    requestControllers.set(requestKey, controller);

    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => {
    const requestKey = createRequestKey(response.config);
    requestControllers.delete(requestKey);

    return response;
  },
  (error) => {
    if (error.config) {
      const requestKey = createRequestKey(error.config);
      requestControllers.delete(requestKey);
    }

    if (axios.isAxiosError(error) && error.response?.status === 401) {
      if (isBrowser) {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      }
    }

    return Promise.reject(error);
  }
);

const buildRequestConfig = (data, config = {}) => {
  const finalConfig = { ...config };

  if (!(data instanceof FormData)) {
    finalConfig.headers = {
      'Content-Type': 'application/json',
      ...config.headers,
    };
  }

  return finalConfig;
};

export default {
  // Products
  getProducts(params = {}) {
    return apiClient.get('/products/', { params });
  },
  getProduct(id) {
    return apiClient.get(`/products/${id}/`);
  },
  getProductBySlug(slug) {
    return apiClient.get(`/products/slug/${slug}/`);
  },
  createProduct(data) {
    return apiClient.post('/products/', data, buildRequestConfig(data));
  },
  updateProduct(id, data) {
    return apiClient.put(`/products/${id}/`, data, buildRequestConfig(data));
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
    return apiClient.get('/blog/posts/', { params });
  },
  getBlogPost(slug) {
    return apiClient.get(`/blog/posts/${slug}/`);
  },
  createBlogPost(data) {
    return apiClient.post('/blog/posts/', data, buildRequestConfig(data));
  },
  updateBlogPost(slug, data) {
    return apiClient.put(`/blog/posts/${slug}/`, data, buildRequestConfig(data));
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
    return apiClient.get('/blog/categories/');
  },
  getBlogCategory(slug) {
    return apiClient.get(`/blog/categories/${slug}/`);
  },
  createBlogCategory(data) {
    return apiClient.post('/blog/categories/', data, buildRequestConfig(data));
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
    return apiClient.put(
      '/auth/profile/update/',
      data,
      buildRequestConfig(data)
    );
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
    return apiClient.post('/auth/ads/', data, buildRequestConfig(data));
  },
  updateSellerAd(id, data) {
    return apiClient.put(`/auth/ads/${id}/`, data, buildRequestConfig(data));
  },
  deleteSellerAd(id) {
    return apiClient.delete(`/auth/ads/${id}/`);
  },
  uploadAdImage(adId, formData) {
    return apiClient.post(
      `/auth/ads/${adId}/upload_image/`,
      formData,
      buildRequestConfig(formData)
    );
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
  },
  
  // Admin Product Management
  getAdminProducts(params = {}) {
    return apiClient.get('/auth/admin/products/', { params });
  },
  getAdminProductDetail(productId) {
    return apiClient.get(`/auth/admin/products/${productId}/`);
  },
  adminProductBulkAction(action, productIds) {
    return apiClient.post('/auth/admin/products/bulk-action/', {
      action: action,
      product_ids: productIds
    });
  },
  adminDeleteProduct(productId) {
    return apiClient.delete(`/auth/admin/products/${productId}/delete/`);
  },
  
  // Admin Department Management
  getAdminDepartments(params = {}) {
    return apiClient.get('/auth/admin/departments/', { params });
  },
  getAdminDepartmentDetail(departmentId) {
    return apiClient.get(`/auth/admin/departments/${departmentId}/`);
  },
  adminCreateDepartment(data) {
    return apiClient.post(
      '/auth/admin/departments/create/',
      data,
      buildRequestConfig(data)
    );
  },
  adminUpdateDepartment(departmentId, data) {
    return apiClient.put(
      `/auth/admin/departments/${departmentId}/update/`,
      data,
      buildRequestConfig(data)
    );
  },
  adminDeleteDepartment(departmentId) {
    return apiClient.delete(`/auth/admin/departments/${departmentId}/delete/`);
  },
  
  // Admin Category Management
  getAdminCategories(params = {}) {
    return apiClient.get('/auth/admin/categories/', { params });
  },
  getAdminCategoryDetail(categoryId) {
    return apiClient.get(`/auth/admin/categories/${categoryId}/`);
  },
  adminCreateCategory(data) {
    return apiClient.post(
      '/auth/admin/categories/create/',
      data,
      buildRequestConfig(data)
    );
  },
  adminUpdateCategory(categoryId, data) {
    return apiClient.put(
      `/auth/admin/categories/${categoryId}/update/`,
      data,
      buildRequestConfig(data)
    );
  },
  adminDeleteCategory(categoryId) {
    return apiClient.delete(`/auth/admin/categories/${categoryId}/delete/`);
  },
  
  // Admin Subcategory Management
  getAdminSubcategories(params = {}) {
    return apiClient.get('/auth/admin/subcategories/', { params });
  },
  getAdminSubcategoryDetail(subcategoryId) {
    return apiClient.get(`/auth/admin/subcategories/${subcategoryId}/`);
  },
  adminCreateSubcategory(data) {
    return apiClient.post(
      '/auth/admin/subcategories/create/',
      data,
      buildRequestConfig(data)
    );
  },
  adminUpdateSubcategory(subcategoryId, data) {
    return apiClient.put(
      `/auth/admin/subcategories/${subcategoryId}/update/`,
      data,
      buildRequestConfig(data)
    );
  },
  adminDeleteSubcategory(subcategoryId) {
    return apiClient.delete(`/auth/admin/subcategories/${subcategoryId}/delete/`);
  },
  
  // Admin Blog Management
  getAdminBlogPosts(params = {}) {
    return apiClient.get('/auth/admin/blog/posts/', { params });
  },
  getAdminBlogPostDetail(slug) {
    return apiClient.get(`/auth/admin/blog/posts/${slug}/`);
  },
  adminBlogPostBulkAction(action, postSlugs) {
    return apiClient.post('/auth/admin/blog/posts/bulk-action/', {
      action: action,
      post_slugs: postSlugs
    });
  },
  adminDeleteBlogPost(slug) {
    return apiClient.delete(`/auth/admin/blog/posts/${slug}/delete/`);
  },
  getAdminBlogCategories(params = {}) {
    return apiClient.get('/auth/admin/blog/categories/', { params });
  },
  adminCreateBlogCategory(data) {
    return apiClient.post(
      '/auth/admin/blog/categories/create/',
      data,
      buildRequestConfig(data)
    );
  },
  adminUpdateBlogCategory(slug, data) {
    return apiClient.put(
      `/auth/admin/blog/categories/${slug}/update/`,
      data,
      buildRequestConfig(data)
    );
  },
  adminDeleteBlogCategory(slug) {
    return apiClient.delete(`/auth/admin/blog/categories/${slug}/delete/`);
  },
  
  // RFQ (Request for Quotation)
  createRFQ(formData) {
    return apiClient.post(
      '/orders/rfq/create/',
      formData,
      buildRequestConfig(formData)
    );
  },
  getAdminRFQs(params = {}) {
    return apiClient.get('/orders/admin/rfq/', { params });
  },
  getAdminRFQDetail(rfqId) {
    return apiClient.get(`/orders/admin/rfq/${rfqId}/`);
  },
  updateRFQStatus(rfqId, status) {
    return apiClient.patch(`/orders/admin/rfq/${rfqId}/status/`, { status });
  },
  getVendorRFQs(params = {}) {
    return apiClient.get('/orders/vendor/rfq/', { params });
  }
}