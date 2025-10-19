// src/stores/auth.js
import { defineStore } from 'pinia';
import api from '@/services/api';
import { useI18n } from 'vue-i18n';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('authToken') || null,
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
    userRole: (state) => state.user?.role || null,
    isBuyer: (state) => state.user?.role === 'buyer' || state.user?.role === 'both',
    isSeller: (state) => state.user?.role === 'seller' || state.user?.role === 'both',
    isAdmin: (state) => state.user?.is_staff || false,
    isVerified: (state) => state.user?.is_verified || false,
    vendorProfile: (state) => state.user?.vendor_profile || null
  },

  actions: {
    async login(credentials) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.login(credentials);
        this.token = response.data.token;
        this.user = response.data.user;
        localStorage.setItem('authToken', this.token);
        localStorage.setItem('user', JSON.stringify(response.data.user));

        return response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'خطا در ورود. لطفاً اطلاعات خود را بررسی کنید.';
        console.error('Login error:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async logout() {
      this.loading = true;

      try {
        await api.logout();
      } catch (error) {
        console.error('Logout error:', error);
      } finally {
        this.token = null;
        this.user = null;
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        this.loading = false;
      }
    },

    async register(userData) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.register(userData);
        this.token = response.data.token;
        this.user = response.data.user;
        localStorage.setItem('authToken', this.token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.';
        console.error('Registration error:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchCurrentUser() {
      if (!this.token) return;

      try {
        const response = await api.getCurrentUser();
        this.user = response.data;
        localStorage.setItem('user', JSON.stringify(response.data));
      } catch (error) {
        console.error('Fetch current user error:', error);
        // If token is invalid, logout
        if (error.response?.status === 401) {
          this.logout();
        }
      }
    },

    async updateProfile(data) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.updateProfile(data);
        this.user = response.data;
        localStorage.setItem('user', JSON.stringify(response.data));
        return response.data;
      } catch (error) {
        this.error = 'خطا در بروزرسانی پروفایل. لطفاً دوباره تلاش کنید.';
        console.error('Profile update error:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    initializeAuth() {
      if (this.token) {
        // Token is automatically added via interceptor in api.js
        // Optionally fetch current user data
        this.fetchCurrentUser();
      }
    }
  }
});