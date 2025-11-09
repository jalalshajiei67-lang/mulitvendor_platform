// src/stores/modules/productStore.js
import { defineStore } from 'pinia';
import api from '@/services/api';

const translations = {
  loading: 'در حال بارگذاری...',
  error: 'خطا',
  failedToFetch: 'خطا در دریافت اطلاعات',
  failedToCreate: 'خطا در ایجاد',
  failedToUpdate: 'خطا در بروزرسانی',
  failedToDelete: 'خطا در حذف',
  failedToSubmitComment: 'خطا در ثبت نظر',
  products: 'محصولات',
  product: 'محصول',
  myProducts: 'محصولات من'
};

export const useProductStore = defineStore('products', {
  state: () => ({
    products: [],
    currentProduct: null,
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
    
    // Product filters
    getProductsByCategory: (state) => (categoryId) => 
      state.products.filter(product => product.category === categoryId),
    getProductsBySubcategory: (state) => (subcategoryId) => 
      state.products.filter(product => product.subcategory === subcategoryId),
    getProductsByVendor: (state) => (vendorId) => 
      state.products.filter(product => product.vendor === vendorId),
    
    // Product status
    activeProducts: (state) => state.products.filter(product => product.is_active),
    inStockProducts: (state) => state.products.filter(product => product.stock > 0),
    
    // Sorting helpers
    newestProducts: (state) => [...state.products].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)),
    cheapestProducts: (state) => [...state.products].sort((a, b) => a.price - b.price),
    mostExpensiveProducts: (state) => [...state.products].sort((a, b) => b.price - a.price)
  },

  actions: {
    async fetchProducts(params = {}) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getProducts(params);
        this.products = response.data.results || response.data;
        this.pagination = {
          count: response.data.count || 0,
          next: response.data.next,
          previous: response.data.previous,
        };
      } catch (error) {
        this.error = this.t('failedToFetch') + ': ' + error.message;
        console.error('Error fetching products:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchProduct(id) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getProduct(id);
        this.currentProduct = response.data;
        return response.data;
      } catch (error) {
        this.error = this.t('failedToFetch');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchProductBySlug(slug) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getProductBySlug(slug);
        this.currentProduct = response.data;
        return response.data;
      } catch (error) {
        this.error = this.t('failedToFetch');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchMyProducts() {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getMyProducts();
        this.products = response.data.results || response.data;
        this.pagination = {
          count: response.data.count || 0,
          next: response.data.next,
          previous: response.data.previous,
        };
      } catch (error) {
        this.error = this.t('failedToFetch') + ': ' + error.message;
        console.error('Error fetching my products:', error);
      } finally {
        this.loading = false;
      }
    },

    async createProduct(productData) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.createProduct(productData);
        this.products.unshift(response.data);
        return response.data;
      } catch (error) {
        this.error = this.t('failedToCreate');
        console.error('Error creating product:', error);
        console.error('Error response:', error.response);
        console.error('Error response data:', error.response?.data);
        console.error('Error status:', error.response?.status);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateProduct(id, productData) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.updateProduct(id, productData);
        const index = this.products.findIndex(p => p.id === id);
        if (index !== -1) {
          this.products[index] = response.data;
        }
        if (this.currentProduct && this.currentProduct.id === id) {
          this.currentProduct = response.data;
        }
        return response.data;
      } catch (error) {
        this.error = this.t('failedToUpdate');
        console.error('Error updating product:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteProduct(id) {
      this.loading = true;
      this.error = null;

      try {
        await api.deleteProduct(id);
        this.products = this.products.filter(p => p.id !== id);
        if (this.currentProduct && this.currentProduct.id === id) {
          this.currentProduct = null;
        }
      } catch (error) {
        this.error = this.t('failedToDelete');
        console.error('Error deleting product:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteProductImage(productId, imageId) {
      this.loading = true;
      this.error = null;

      try {
        await api.deleteProductImage(productId, imageId);
        
        if (this.currentProduct && this.currentProduct.id === productId) {
          this.currentProduct.images = this.currentProduct.images.filter(img => img.id !== imageId);
        }
        
        const productIndex = this.products.findIndex(p => p.id === productId);
        if (productIndex !== -1) {
          this.products[productIndex].images = this.products[productIndex].images.filter(img => img.id !== imageId);
        }
      } catch (error) {
        this.error = this.t('failedToDelete');
        console.error('Error deleting product image:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createProductComment(productId, commentData) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.createProductComment(productId, commentData);
        await this.fetchProduct(productId);
        return response.data;
      } catch (error) {
        this.error = this.t('failedToSubmitComment');
        console.error('Error creating product comment:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchProductComments(productId) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.getProductComments(productId);
        return response.data;
      } catch (error) {
        this.error = this.t('failedToFetch');
        console.error('Error fetching product comments:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    clearProducts() {
      this.products = [];
      this.currentProduct = null;
      this.pagination = {
        count: 0,
        next: null,
        previous: null,
      };
    }
  }
});
