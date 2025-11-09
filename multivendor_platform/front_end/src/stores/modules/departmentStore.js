// src/stores/modules/departmentStore.js
import { defineStore } from 'pinia';
import api from '@/services/api';

const translations = {
  loading: 'در حال بارگذاری...',
  error: 'خطا',
  failedToFetch: 'خطا در دریافت اطلاعات',
  failedToCreate: 'خطا در ایجاد',
  failedToUpdate: 'خطا در بروزرسانی',
  failedToDelete: 'خطا در حذف',
  departments: 'دپارتمان‌ها',
  department: 'دپارتمان'
};

export const useDepartmentStore = defineStore('departments', {
  state: () => ({
    departments: [],
    currentDepartment: null,
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
    getDepartmentById: (state) => (id) => state.departments.find(dept => dept.id === id),
    getDepartmentBySlug: (state) => (slug) => state.departments.find(dept => dept.slug === slug),
    activeDepartments: (state) => state.departments.filter(dept => dept.is_active)
  },

  actions: {
    async fetchDepartments(params = {}) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getDepartments(params);
        this.departments = response.data.results || response.data;
        this.pagination = {
          count: response.data.count || 0,
          next: response.data.next,
          previous: response.data.previous,
        };
      } catch (error) {
        this.error = this.t('failedToFetch') + ': ' + error.message;
        console.error('Error fetching departments:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchAdminDepartments(params = {}) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getAdminDepartments(params);
        this.departments = response.data.results || response.data;
        this.pagination = {
          count: response.data.count || 0,
          next: response.data.next,
          previous: response.data.previous,
        };
        return response.data;
      } catch (error) {
        this.error = this.t('failedToFetch') + ': ' + error.message;
        console.error('Error fetching admin departments:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchDepartment(id) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getDepartment(id);
        this.currentDepartment = response.data;
        return response.data;
      } catch (error) {
        this.error = this.t('failedToFetch');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchAdminDepartmentDetail(id) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getAdminDepartmentDetail(id);
        this.currentDepartment = response.data;
        return response.data;
      } catch (error) {
        this.error = this.t('failedToFetch');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createDepartment(formData) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.adminCreateDepartment(formData);
        this.departments.push(response.data);
        return response.data;
      } catch (error) {
        this.error = this.t('failedToCreate');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateDepartment(id, formData) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.adminUpdateDepartment(id, formData);
        const index = this.departments.findIndex(dept => dept.id === id);
        if (index !== -1) {
          this.departments[index] = response.data;
        }
        return response.data;
      } catch (error) {
        this.error = this.t('failedToUpdate');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteDepartment(id) {
      this.loading = true;
      this.error = null;

      try {
        await api.adminDeleteDepartment(id);
        this.departments = this.departments.filter(dept => dept.id !== id);
        return true;
      } catch (error) {
        this.error = this.t('failedToDelete');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    clearDepartments() {
      this.departments = [];
      this.currentDepartment = null;
    }
  }
});
