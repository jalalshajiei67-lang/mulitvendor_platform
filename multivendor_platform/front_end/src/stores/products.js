// src/stores/products.js
import { defineStore } from 'pinia';
import api from '@/services/api';

export const useProductStore = defineStore('products', {
  state: () => ({
    products: [],
    categories: [],
    currentProduct: null,
    loading: false,
    error: null,
    pagination: {
      count: 0,
      next: null,
      previous: null,
    },

    // Persian Translations
    translations: {
      // Common
      loading: 'در حال بارگذاری...',
      error: 'خطا',
      save: 'ذخیره',
      cancel: 'لغو',
      delete: 'حذف',
      edit: 'ویرایش',
      view: 'مشاهده',
      create: 'ایجاد',
      update: 'بروزرسانی',
      search: 'جستجو',
      filter: 'فیلتر',
      all: 'همه',
      active: 'فعال',
      inactive: 'غیرفعال',
      actions: 'عملیات',

      // Product specific
      products: 'محصولات',
      product: 'محصول',
      myProducts: 'محصولات من',
      categories: 'دسته‌بندی‌ها',
      category: 'دسته‌بندی',
      vendor: 'فروشنده',
      price: 'قیمت',
      stock: 'موجودی',
      description: 'توضیحات',
      image: 'تصویر',
      name: 'نام',
      addNewProduct: 'افزودن محصول جدید',
      editProduct: 'ویرایش محصول',
      deleteProduct: 'حذف محصول',
      productName: 'نام محصول',
      productDescription: 'توضیحات محصول',
      productPrice: 'قیمت محصول',
      productStock: 'موجودی محصول',
      productImage: 'تصویر محصول',
      productImages: 'تصاویر محصول',
      max20Images: 'حداکثر 20 تصویر',
      dragDropImages: 'تصاویر را اینجا بکشید',
      orClickToSelect: 'یا کلیک کنید تا انتخاب کنید',
      addMore: 'افزودن بیشتر',
      removeImage: 'حذف تصویر',
      primary: 'اصلی',
      onlyImagesAllowed: 'فقط فایل‌های تصویری مجاز است',
      max20ImagesExceeded: 'حداکثر 20 تصویر مجاز است',
      previousImage: 'تصویر قبلی',
      nextImage: 'تصویر بعدی',
      clickToViewFullSize: 'کلیک کنید تا تصویر را در اندازه کامل ببینید',
      productCategory: 'دسته‌بندی محصول',
      selectCategory: 'دسته‌بندی را انتخاب کنید',
      productIsActive: 'محصول فعال است',
      saveProduct: 'ذخیره محصول',
      saving: 'در حال ذخیره...',
      noProductsFound: 'هیچ محصولی یافت نشد',
      noCategoriesFound: 'هیچ دسته‌بندی یافت نشد',
      allCategories: 'همه دسته‌بندی‌ها',
      searchProducts: 'جستجوی محصولات...',
      newestFirst: 'جدیدترین اول',
      oldestFirst: 'قدیمی‌ترین اول',
      priceLowToHigh: 'قیمت: کم به زیاد',
      priceHighToLow: 'قیمت: زیاد به کم',
      nameAToZ: 'نام: الف تا ی',
      nameZToA: 'نام: ی تا الف',
      previous: 'قبلی',
      next: 'بعدی',
      page: 'صفحه',
      of: 'از',
      inStock: 'موجود',
      outOfStock: 'ناموجود',
      soldBy: 'فروشنده',
      addToCart: 'افزودن به سبد خرید',
      confirmDelete: 'آیا مطمئن هستید که می‌خواهید حذف کنید؟',
      failedToFetch: 'خطا در دریافت اطلاعات',
      failedToCreate: 'خطا در ایجاد',
      failedToUpdate: 'خطا در بروزرسانی',
      failedToDelete: 'خطا در حذف',
      productNotFound: 'محصول یافت نشد',
      loadingProduct: 'در حال بارگذاری محصول...',
      loadingProducts: 'در حال بارگذاری محصولات...',
      home: 'خانه',
      back: 'بازگشت',
      testApiCall: 'تست فراخوانی API',
      testDirectFetch: 'تست دریافت مستقیم',
      testManualData: 'تست داده دستی',
      debugInfo: 'اطلاعات دیباگ',
      loadingState: 'وضعیت بارگذاری',
      errorState: 'وضعیت خطا',
      productsCount: 'تعداد محصولات',
      productsData: 'داده محصولات',
      noImage: 'بدون تصویر',
      noProductsAvailable: 'هنوز محصولی موجود نیست',
      tryAgain: 'دوباره تلاش کنید',

      // Comments
      comments: 'نظرات',
      comment: 'نظر',
      addComment: 'افزودن نظر',
      writeComment: 'نظر خود را بنویسید...',
      rating: 'امتیاز',
      submitComment: 'ارسال نظر',
      replyTo: 'پاسخ به',
      noCommentsYet: 'هنوز نظری ثبت نشده',
      beTheFirst: 'اولین نفر باشید که نظر می‌دهد',
      replies: 'پاسخ‌ها',
      reply: 'پاسخ',
      commentSubmitted: 'نظر شما ثبت شد و پس از تایید نمایش داده می‌شود',
      failedToSubmitComment: 'خطا در ثبت نظر',
      averageRating: 'میانگین امتیاز',
      stars: 'ستاره'
    }
  }),

  getters: {
    // Get translation by key
    t: (state) => (key) => {
      return state.translations[key] || key;
    }
  },

  actions: {
    async fetchProducts(params = {}) {
      this.loading = true;
      this.error = null;

      try {
        console.log('Product Store: Fetching products with params:', params);
        const response = await api.getProducts(params);
        console.log('Product Store: Received response:', response);

        this.products = response.data.results || response.data;
        this.pagination = {
          count: response.data.count || 0,
          next: response.data.next,
          previous: response.data.previous,
        };
        console.log('Product Store: Products set to:', this.products);
      } catch (error) {
        this.error = this.t('failedToFetch') + ': ' + error.message;
        console.error('Error fetching products:', error);
        console.error('Error details:', error.response?.data);
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
      } catch (error) {
        this.error = this.t('failedToFetch');
        console.error('Error fetching product:', error);
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

    async fetchCategories() {
      this.loading = true;
      this.error = null;

      try {
        console.log('Product Store: Fetching categories');
        const response = await api.getCategories();
        console.log('Product Store: Received categories response:', response);
        this.categories = response.data.results || response.data;
        console.log('Product Store: Categories set to:', this.categories);
      } catch (error) {
        this.error = this.t('failedToFetch');
        console.error('Error fetching categories:', error);
        console.error('Error details:', error.response?.data);
      } finally {
        this.loading = false;
      }
    },

    async fetchMyProducts() {
      this.loading = true;
      this.error = null;

      try {
        console.log('Product Store: Fetching my products');
        const response = await api.getMyProducts();
        console.log('Product Store: Received my products response:', response);
        this.products = response.data.results || response.data;
        console.log('Product Store: My products set to:', this.products);
      } catch (error) {
        this.error = this.t('failedToFetch');
        console.error('Error fetching my products:', error);
        console.error('Error details:', error.response?.data);
      } finally {
        this.loading = false;
      }
    },

    async deleteProductImage(productId, imageId) {
      this.loading = true;
      this.error = null;

      try {
        await api.deleteProductImage(productId, imageId);

        // Update current product if it's the one being modified
        if (this.currentProduct && this.currentProduct.id === productId) {
          this.currentProduct.images = this.currentProduct.images.filter(img => img.id !== imageId);
        }

        // Update products list
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
        console.log('Product Store: Creating comment for product:', productId, commentData);
        const response = await api.createProductComment(productId, commentData);
        console.log('Product Store: Comment created:', response);

        // Refresh the product to get updated comments
        await this.fetchProduct(productId);

        return response.data;
      } catch (error) {
        this.error = this.t('failedToSubmitComment');
        console.error('Error creating product comment:', error);
        console.error('Error details:', error.response?.data);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchProductComments(productId) {
      this.loading = true;
      this.error = null;

      try {
        console.log('Product Store: Fetching comments for product:', productId);
        const response = await api.getProductComments(productId);
        console.log('Product Store: Comments received:', response);
        return response.data;
      } catch (error) {
        this.error = this.t('failedToFetch');
        console.error('Error fetching product comments:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});