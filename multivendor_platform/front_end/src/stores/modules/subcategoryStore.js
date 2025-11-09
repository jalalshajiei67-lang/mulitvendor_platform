// src/stores/modules/subcategoryStore.js
import { defineStore } from 'pinia';
import api from '@/services/api';

const translations = {
  loading: 'در حال بارگذاری...',
  error: 'خطا',
  failedToFetch: 'خطا در دریافت اطلاعات',
  failedToCreate: 'خطا در ایجاد',
  failedToUpdate: 'خطا در بروزرسانی',
  failedToDelete: 'خطا در حذف',
  subcategories: 'زیردسته‌ها',
  subcategory: 'زیردسته'
};

export const useSubcategoryStore = defineStore('subcategories', {
  state: () => ({
    subcategories: [],
    currentSubcategory: null,
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
    getSubcategoryById: (state) => (id) => state.subcategories.find(sub => sub.id === id),
    getSubcategoryBySlug: (state) => (slug) => state.subcategories.find(sub => sub.slug === slug),
    getSubcategoriesByCategory: (state) => (categoryId) => 
      state.subcategories.filter(sub => sub.category === categoryId),
    getSubcategoriesByDepartment: (state) => (departmentId) => 
      state.subcategories.filter(sub => sub.department === departmentId),
    activeSubcategories: (state) => state.subcategories.filter(sub => sub.is_active),
    // For most viewed subcategory page
    getNewProductsBySubcategory: (state) => (subcategoryId) => {
      const subcategory = state.subcategories.find(sub => sub.id === subcategoryId);
      return subcategory?.new_products || [];
    }
  },

  actions: {
    async fetchSubcategories(params = {}) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getSubcategories(params);
        this.subcategories = response.data.results || response.data;
        this.pagination = {
          count: response.data.count || 0,
          next: response.data.next,
          previous: response.data.previous,
        };
      } catch (error) {
        this.error = this.t('failedToFetch') + ': ' + error.message;
        console.error('Error fetching subcategories:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchAdminSubcategories(params = {}) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getAdminSubcategories(params);
        this.subcategories = response.data.results || response.data;
        this.pagination = {
          count: response.data.count || 0,
          next: response.data.next,
          previous: response.data.previous,
        };
        return response.data;
      } catch (error) {
        this.error = this.t('failedToFetch') + ': ' + error.message;
        console.error('Error fetching admin subcategories:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchSubcategory(id) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getSubcategory(id);
        this.currentSubcategory = response.data;
        return response.data;
      } catch (error) {
        this.error = this.t('failedToFetch');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchAdminSubcategoryDetail(id) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getAdminSubcategoryDetail(id);
        this.currentSubcategory = response.data;
        return response.data;
      } catch (error) {
        this.error = this.t('failedToFetch');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchSubcategoryBySlug(slug) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getSubcategoryBySlug(slug);
        const subcategories = response.data.results || response.data;
        if (subcategories.length > 0) {
          this.currentSubcategory = subcategories[0];
          return subcategories[0];
        }
        throw new Error('Subcategory not found');
      } catch (error) {
        this.error = this.t('failedToFetch');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createSubcategory(formData) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.adminCreateSubcategory(formData);
        this.subcategories.push(response.data);
        return response.data;
      } catch (error) {
        this.error = this.t('failedToCreate');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateSubcategory(id, formData) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.adminUpdateSubcategory(id, formData);
        const index = this.subcategories.findIndex(sub => sub.id === id);
        if (index !== -1) {
          this.subcategories[index] = response.data;
        }
        return response.data;
      } catch (error) {
        this.error = this.t('failedToUpdate');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteSubcategory(id) {
      this.loading = true;
      this.error = null;

      try {
        await api.adminDeleteSubcategory(id);
        this.subcategories = this.subcategories.filter(sub => sub.id !== id);
        return true;
      } catch (error) {
        this.error = this.t('failedToDelete');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    clearSubcategories() {
      this.subcategories = [];
      this.currentSubcategory = null;
    }
  }
});
