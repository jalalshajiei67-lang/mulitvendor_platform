// src/stores/modules/categoryStore.js
import { defineStore } from 'pinia';
import api from '@/services/api';

const translations = {
  loading: 'در حال بارگذاری...',
  error: 'خطا',
  failedToFetch: 'خطا در دریافت اطلاعات',
  failedToCreate: 'خطا در ایجاد',
  failedToUpdate: 'خطا در بروزرسانی',
  failedToDelete: 'خطا در حذف',
  categories: 'دسته‌بندی‌ها',
  category: 'دسته‌بندی'
};

export const useCategoryStore = defineStore('categories', {
  state: () => ({
    categories: [],
    currentCategory: null,
    loading: false,
    error: null,
    pagination: {
      count: 0,
      next: null,
      previous: null,
    }
  }),

  getters: {
    t: () => (key) => translations[key] || key,
    isLoading: (state) => state.loading,
    hasError: (state) => !!state.error,
    getCategoryById: (state) => (id) => state.categories.find(cat => cat.id === id),
    getCategoryBySlug: (state) => (slug) => state.categories.find(cat => cat.slug === slug),
    getCategoriesByDepartment: (state) => (departmentId) => 
      state.categories.filter(cat => cat.department === departmentId),
    activeCategories: (state) => state.categories.filter(cat => cat.is_active)
  },

  actions: {
    async fetchCategories(params = {}) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getCategories(params);
        this.categories = response.data.results || response.data;
        this.pagination = {
          count: response.data.count || 0,
          next: response.data.next,
          previous: response.data.previous,
        };
      } catch (error) {
        this.error = this.t('failedToFetch') + ': ' + error.message;
        console.error('Error fetching categories:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchAdminCategories(params = {}) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getAdminCategories(params);
        this.categories = response.data.results || response.data;
        this.pagination = {
          count: response.data.count || 0,
          next: response.data.next,
          previous: response.data.previous,
        };
        return response.data;
      } catch (error) {
        this.error = this.t('failedToFetch') + ': ' + error.message;
        console.error('Error fetching admin categories:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchCategory(id) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getCategory(id);
        this.currentCategory = response.data;
        return response.data;
      } catch (error) {
        this.error = this.t('failedToFetch');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchAdminCategoryDetail(id) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getAdminCategoryDetail(id);
        this.currentCategory = response.data;
        return response.data;
      } catch (error) {
        this.error = this.t('failedToFetch');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchCategoryBySlug(slug) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getCategoryBySlug(slug);
        const categories = response.data.results || response.data;
        if (categories.length > 0) {
          this.currentCategory = categories[0];
          return categories[0];
        }
        throw new Error('Category not found');
      } catch (error) {
        this.error = this.t('failedToFetch');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createCategory(formData) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.adminCreateCategory(formData);
        this.categories.push(response.data);
        return response.data;
      } catch (error) {
        this.error = this.t('failedToCreate');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateCategory(id, formData) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.adminUpdateCategory(id, formData);
        const index = this.categories.findIndex(cat => cat.id === id);
        if (index !== -1) {
          this.categories[index] = response.data;
        }
        return response.data;
      } catch (error) {
        this.error = this.t('failedToUpdate');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteCategory(id) {
      this.loading = true;
      this.error = null;

      try {
        await api.adminDeleteCategory(id);
        this.categories = this.categories.filter(cat => cat.id !== id);
        return true;
      } catch (error) {
        this.error = this.t('failedToDelete');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    clearCategories() {
      this.categories = [];
      this.currentCategory = null;
    }
  }
});
