// src/stores/modules/orderStore.js
import { defineStore } from 'pinia';
import api from '@/services/api';

const translations = {
  loading: 'در حال بارگذاری...',
  error: 'خطا',
  failedToFetch: 'خطا در دریافت اطلاعات',
  failedToCreate: 'خطا در ایجاد',
  failedToUpdate: 'خطا در بروزرسانی',
  failedToDelete: 'خطا در حذف',
  orders: 'سفارش‌ها',
  order: 'سفارش'
};

export const useOrderStore = defineStore('orders', {
  state: () => ({
    orders: [],
    currentOrder: null,
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
    
    // Order filters
    getOrdersByStatus: (state) => (status) => 
      state.orders.filter(order => order.status === status),
    getOrdersByUser: (state) => (userId) => 
      state.orders.filter(order => order.user === userId),
    getOrdersByVendor: (state) => (vendorId) => 
      state.orders.filter(order => order.vendor === vendorId),
    
    // Order status helpers
    pendingOrders: (state) => state.orders.filter(order => order.status === 'pending'),
    completedOrders: (state) => state.orders.filter(order => order.status === 'completed'),
    cancelledOrders: (state) => state.orders.filter(order => order.status === 'cancelled'),
    
    // Order statistics
    totalRevenue: (state) => state.orders
      .filter(order => order.status === 'completed')
      .reduce((sum, order) => sum + parseFloat(order.total), 0),
    
    totalOrdersCount: (state) => state.orders.length
  },

  actions: {
    async fetchOrders(params = {}) {
      this.loading = true;
      this.error = null;

      try {
        // This would need to be implemented in your API
        // const response = await api.getOrders(params);
        // this.orders = response.data.results || response.data;
        // this.pagination = {
        //   count: response.data.count || 0,
        //   next: response.data.next,
        //   previous: response.data.previous,
        // };
        console.log('Order Store: Fetch orders not yet implemented');
      } catch (error) {
        this.error = this.t('failedToFetch') + ': ' + error.message;
        console.error('Error fetching orders:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchOrder(id) {
      this.loading = true;
      this.error = null;

      try {
        // const response = await api.getOrder(id);
        // this.currentOrder = response.data;
        // return response.data;
        console.log('Order Store: Fetch order not yet implemented');
      } catch (error) {
        this.error = this.t('failedToFetch');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createOrder(orderData) {
      this.loading = true;
      this.error = null;

      try {
        // const response = await api.createOrder(orderData);
        // this.orders.unshift(response.data);
        // return response.data;
        console.log('Order Store: Create order not yet implemented');
      } catch (error) {
        this.error = this.t('failedToCreate');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateOrderStatus(id, status) {
      this.loading = true;
      this.error = null;

      try {
        // const response = await api.updateOrderStatus(id, status);
        // this.updateOrderInStore(response.data);
        // return response.data;
        console.log('Order Store: Update order status not yet implemented');
      } catch (error) {
        this.error = this.t('failedToUpdate');
        throw error;
      } finally {
        this.loading = false;
      }
    },

    updateOrderInStore(order) {
      const index = this.orders.findIndex(o => o.id === order.id);
      if (index !== -1) {
        this.orders[index] = order;
      }
      if (this.currentOrder && this.currentOrder.id === order.id) {
        this.currentOrder = order;
      }
    },

    clearOrders() {
      this.orders = [];
      this.currentOrder = null;
      this.pagination = {
        count: 0,
        next: null,
        previous: null,
      };
    }
  }
});
