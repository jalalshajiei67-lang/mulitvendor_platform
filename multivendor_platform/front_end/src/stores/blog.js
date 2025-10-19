// src/stores/blog.js
import { defineStore } from 'pinia';
import api from '@/services/api';

export const useBlogStore = defineStore('blog', {
    state: () => ({
        // Blog Posts
        posts: [],
        currentPost: null,
        featuredPosts: [],
        recentPosts: [],
        popularPosts: [],

        // Blog Categories
        categories: [],
        currentCategory: null,

        // Comments
        comments: [],

        // UI State
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
            published: 'منتشر شده',
            draft: 'پیش‌نویس',
            archived: 'آرشیو شده',
            featured: 'ویژه',
            active: 'فعال',
            actions: 'عملیات',

            // Blog specific
            blog: 'وبلاگ',
            dashboard: 'داشبورد',
            posts: 'پست‌ها',
            post: 'پست',
            categories: 'دسته‌بندی‌ها',
            category: 'دسته‌بندی',
            comments: 'نظرات',
            comment: 'نظر',
            author: 'نویسنده',
            date: 'تاریخ',
            views: 'بازدید',
            readingTime: 'دقیقه مطالعه',
            totalPosts: 'کل پست‌ها',
            totalViews: 'کل بازدیدها',
            totalComments: 'کل نظرات',
            myPosts: 'پست‌های من',
            newPost: 'پست جدید',
            newCategory: 'دسته‌بندی جدید',
            createNewPost: 'ایجاد پست جدید',
            createNewCategory: 'ایجاد دسته‌بندی جدید',
            editPost: 'ویرایش پست',
            editCategory: 'ویرایش دسته‌بندی',
            deletePost: 'حذف پست',
            deleteCategory: 'حذف دسته‌بندی',
            postTitle: 'عنوان پست',
            postContent: 'محتوای پست',
            postExcerpt: 'خلاصه پست',
            featuredImage: 'تصویر شاخص',
            metaTitle: 'عنوان متا',
            metaDescription: 'توضیحات متا',
            status: 'وضعیت',
            isFeatured: 'پست ویژه',
            categoryName: 'نام دسته‌بندی',
            categoryDescription: 'توضیحات دسته‌بندی',
            categoryColor: 'رنگ دسته‌بندی',
            noPostsFound: 'هیچ پستی یافت نشد',
            noCategoriesFound: 'هیچ دسته‌بندی یافت نشد',
            noCommentsFound: 'هیچ نظری یافت نشد',
            leaveComment: 'نظر بگذارید',
            postComment: 'ارسال نظر',
            reply: 'پاسخ',
            share: 'اشتراک‌گذاری',
            relatedPosts: 'پست‌های مرتبط',
            popularPosts: 'پست‌های محبوب',
            recentPosts: 'پست‌های اخیر',
            backToBlog: 'بازگشت به وبلاگ',
            back: 'بازگشت',
            next: 'بعدی',
            previous: 'قبلی',
            page: 'صفحه',
            of: 'از',
            minRead: 'دقیقه مطالعه',
            clickToUpload: 'برای آپلود کلیک کنید',
            recommendedSize: 'اندازه پیشنهادی',
            enterTitle: 'عنوان جذاب برای پست خود وارد کنید',
            writeExcerpt: 'توضیح کوتاهی از پست خود بنویسید',
            writeContent: 'محتوای پست خود را اینجا بنویسید...',
            enterCategoryName: 'نام دسته‌بندی را وارد کنید',
            categoryDescriptionPlaceholder: 'توضیحات دسته‌بندی',
            writeComment: 'نظر خود را اینجا بنویسید...',
            loginToComment: 'لطفاً برای نظر دادن وارد شوید',
            beFirstToComment: 'هنوز نظری وجود ندارد. اولین نفری باشید که نظر می‌دهد!',
            postNotFound: 'پست یافت نشد',
            failedToFetch: 'خطا در دریافت اطلاعات',
            failedToCreate: 'خطا در ایجاد',
            failedToUpdate: 'خطا در بروزرسانی',
            failedToDelete: 'خطا در حذف',
            confirmDelete: 'آیا مطمئن هستید که می‌خواهید حذف کنید؟',
            linkCopied: 'لینک کپی شد!',
            loadingPosts: 'در حال بارگذاری پست‌ها...',
            loadingPost: 'در حال بارگذاری پست...',
            postingComment: 'در حال ارسال نظر...',
            creatingCategory: 'در حال ایجاد دسته‌بندی...',
            updatingCategory: 'در حال بروزرسانی دسته‌بندی...',
            savingDraft: 'ذخیره پیش‌نویس',
            publishPost: 'انتشار پست',
            updatePost: 'بروزرسانی پست',
            createCategory: 'ایجاد دسته‌بندی',
            updateCategory: 'بروزرسانی دسته‌بندی',
            selectCategory: 'دسته‌بندی را انتخاب کنید',
            none: 'هیچکدام',
            linkedToProductCategory: 'مرتبط با دسته‌بندی محصول',
            postCount: 'پست',
            posts: 'پست‌ها',
            thisWillBeShown: 'این در لیست وبلاگ و پیش‌نمایش شبکه‌های اجتماعی نمایش داده می‌شود',
            useLineBreaks: 'از خطوط جدید برای جدا کردن پاراگراف‌ها استفاده کنید',
            leaveEmptyToUse: 'خالی بگذارید تا از عنوان پست استفاده شود',
            leaveEmptyToUseExcerpt: 'خالی بگذارید تا از خلاصه پست استفاده شود',
            featuredPostsAppear: 'پست‌های ویژه به طور برجسته در صفحه اصلی وبلاگ نمایش داده می‌شوند',
            noDescription: 'بدون توضیحات',
            noPostsInCategory: 'هنوز پستی در این دسته‌بندی وجود ندارد',
            noBlogPostsAvailable: 'هنوز پست وبلاگی موجود نیست',
            discoverInsights: 'بینش‌ها، نکات و داستان‌ها را از جامعه ما کشف کنید',
            allPosts: 'همه پست‌ها',
            gridView: 'نمایش شبکه‌ای',
            listView: 'نمایش لیستی',
            tryAgain: 'دوباره تلاش کنید',
            basicInformation: 'اطلاعات پایه',
            publishSettings: 'تنظیمات انتشار',
            seoSettings: 'تنظیمات SEO',
            preview: 'پیش‌نمایش',
            seoTitleOptional: 'عنوان SEO (اختیاری)',
            seoDescriptionOptional: 'توضیحات SEO (اختیاری)',
            yourPostTitleWillAppearHere: 'عنوان پست شما اینجا نمایش داده می‌شود',
            yourExcerptWillAppearHere: 'خلاصه شما اینجا نمایش داده می‌شود',
            tags: 'برچسب‌ها'
        }
    }),

    getters: {
        // Get posts by category
        postsByCategory: (state) => (categoryId) => {
            return state.posts.filter(post => post.category === categoryId);
        },

        // Get published posts only
        publishedPosts: (state) => {
            return state.posts.filter(post => post.status === 'published');
        },

        // Get draft posts for current user
        draftPosts: (state) => {
            return state.posts.filter(post => post.status === 'draft');
        },

        // Get approved comments
        approvedComments: (state) => {
            return state.comments.filter(comment => comment.is_approved);
        },

        // Get translation by key
        t: (state) => (key) => {
            return state.translations[key] || key;
        }
    },

    actions: {
        // Blog Posts Actions
        async fetchPosts(params = {}) {
            this.loading = true;
            this.error = null;

            try {
                console.log('Blog Store: Fetching posts with params:', params);
                const response = await api.getBlogPosts(params);
                console.log('Blog Store: Received response:', response);
                this.posts = response.data.results || response.data;
                this.pagination = {
                    count: response.data.count || 0,
                    next: response.data.next,
                    previous: response.data.previous,
                };
                console.log('Blog Store: Posts set to:', this.posts);
            } catch (error) {
                this.error = this.t('failedToFetch') + ': ' + error.message;
                console.error('Error fetching blog posts:', error);
                console.error('Error details:', error.response?.data);
            } finally {
                this.loading = false;
            }
        },

        async fetchPost(slug) {
            this.loading = true;
            this.error = null;

            try {
                const response = await api.getBlogPost(slug);
                this.currentPost = response.data;

                // Update the post in the posts array if it exists
                const index = this.posts.findIndex(p => p.slug === slug);
                if (index !== -1) {
                    this.posts[index] = response.data;
                }
            } catch (error) {
                this.error = this.t('failedToFetch');
                console.error('Error fetching blog post:', error);
            } finally {
                this.loading = false;
            }
        },

        async createPost(postData) {
            this.loading = true;
            this.error = null;

            try {
                const response = await api.createBlogPost(postData);
                this.posts.unshift(response.data);
                return response.data;
            } catch (error) {
                this.error = this.t('failedToCreate');
                console.error('Error creating blog post:', error);
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async updatePost(slug, postData) {
            this.loading = true;
            this.error = null;

            try {
                const response = await api.updateBlogPost(slug, postData);
                const index = this.posts.findIndex(p => p.slug === slug);
                if (index !== -1) {
                    this.posts[index] = response.data;
                }
                if (this.currentPost && this.currentPost.slug === slug) {
                    this.currentPost = response.data;
                }
                return response.data;
            } catch (error) {
                this.error = this.t('failedToUpdate');
                console.error('Error updating blog post:', error);
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async deletePost(slug) {
            this.loading = true;
            this.error = null;

            try {
                await api.deleteBlogPost(slug);
                this.posts = this.posts.filter(p => p.slug !== slug);
                if (this.currentPost && this.currentPost.slug === slug) {
                    this.currentPost = null;
                }
            } catch (error) {
                this.error = this.t('failedToDelete');
                console.error('Error deleting blog post:', error);
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async fetchFeaturedPosts() {
            try {
                const response = await api.getFeaturedBlogPosts();
                this.featuredPosts = response.data;
            } catch (error) {
                console.error('Error fetching featured posts:', error);
            }
        },

        async fetchRecentPosts() {
            try {
                const response = await api.getRecentBlogPosts();
                this.recentPosts = response.data;
            } catch (error) {
                console.error('Error fetching recent posts:', error);
            }
        },

        async fetchPopularPosts() {
            try {
                const response = await api.getPopularBlogPosts();
                this.popularPosts = response.data;
            } catch (error) {
                console.error('Error fetching popular posts:', error);
            }
        },

        async fetchMyPosts() {
            this.loading = true;
            this.error = null;

            try {
                const response = await api.getMyBlogPosts();
                this.posts = response.data.results || response.data;
            } catch (error) {
                this.error = this.t('failedToFetch');
                console.error('Error fetching my blog posts:', error);
            } finally {
                this.loading = false;
            }
        },

        // Blog Categories Actions
        async fetchCategories() {
            this.loading = true;
            this.error = null;

            try {
                console.log('Blog Store: Fetching categories');
                const response = await api.getBlogCategories();
                console.log('Blog Store: Received categories response:', response);
                this.categories = response.data.results || response.data;
                console.log('Blog Store: Categories set to:', this.categories);
            } catch (error) {
                this.error = this.t('failedToFetch');
                console.error('Error fetching blog categories:', error);
                console.error('Error details:', error.response?.data);
            } finally {
                this.loading = false;
            }
        },

        async fetchCategory(slug) {
            this.loading = true;
            this.error = null;

            try {
                const response = await api.getBlogCategory(slug);
                this.currentCategory = response.data;
            } catch (error) {
                this.error = this.t('failedToFetch');
                console.error('Error fetching blog category:', error);
            } finally {
                this.loading = false;
            }
        },

        async createCategory(categoryData) {
            this.loading = true;
            this.error = null;

            try {
                const response = await api.createBlogCategory(categoryData);
                this.categories.push(response.data);
                return response.data;
            } catch (error) {
                this.error = this.t('failedToCreate');
                console.error('Error creating blog category:', error);
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async updateCategory(slug, categoryData) {
            this.loading = true;
            this.error = null;

            try {
                const response = await api.updateBlogCategory(slug, categoryData);
                const index = this.categories.findIndex(c => c.slug === slug);
                if (index !== -1) {
                    this.categories[index] = response.data;
                }
                if (this.currentCategory && this.currentCategory.slug === slug) {
                    this.currentCategory = response.data;
                }
                return response.data;
            } catch (error) {
                this.error = this.t('failedToUpdate');
                console.error('Error updating blog category:', error);
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async deleteCategory(slug) {
            this.loading = true;
            this.error = null;

            try {
                await api.deleteBlogCategory(slug);
                this.categories = this.categories.filter(c => c.slug !== slug);
                if (this.currentCategory && this.currentCategory.slug === slug) {
                    this.currentCategory = null;
                }
            } catch (error) {
                this.error = this.t('failedToDelete');
                console.error('Error deleting blog category:', error);
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async fetchCategoryPosts(slug) {
            this.loading = true;
            this.error = null;

            try {
                const response = await api.getBlogCategoryPosts(slug);
                this.posts = response.data.results || response.data;
                this.pagination = {
                    count: response.data.count || 0,
                    next: response.data.next,
                    previous: response.data.previous,
                };
            } catch (error) {
                this.error = this.t('failedToFetch');
                console.error('Error fetching category posts:', error);
            } finally {
                this.loading = false;
            }
        },

        // Comments Actions
        async fetchComments(postSlug) {
            try {
                const response = await api.getBlogPostComments(postSlug);
                this.comments = response.data;
            } catch (error) {
                console.error('Error fetching comments:', error);
            }
        },

        async createComment(postSlug, commentData) {
            try {
                const response = await api.createBlogComment(postSlug, commentData);
                this.comments.push(response.data);
                return response.data;
            } catch (error) {
                this.error = this.t('failedToCreate');
                console.error('Error creating comment:', error);
                throw error;
            }
        },

        // Utility Actions
        clearCurrentPost() {
            this.currentPost = null;
        },

        clearCurrentCategory() {
            this.currentCategory = null;
        },

        clearError() {
            this.error = null;
        }
    }
});
