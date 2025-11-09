<template>
  <div class="blog-form" dir="rtl">
    <div class="container">
      <div class="form-header">
        <h1>{{ isEditing ? t('editPost') : t('createNewPost') }}</h1>
        <button @click="$router.go(-1)" class="back-btn">
          <i class="fas fa-arrow-right"></i>
          {{ t('back') }}
        </button>
      </div>

      <form @submit.prevent="submitForm" class="blog-form-content">
        <div class="form-grid">
          <!-- Main Content -->
          <div class="main-form">
            <div class="form-section">
              <h2>{{ t('basicInformation') }}</h2>
              
              <div class="form-group">
                <label for="title">{{ t('postTitle') }} *</label>
                <input 
                  id="title"
                  v-model="form.title" 
                  type="text" 
                  required 
                  :placeholder="t('enterTitle')"
                  class="form-input"
                  :class="{ 'error': !form.title.trim() && submitting }"
                />
                <small v-if="!form.title.trim() && submitting" class="error-text">عنوان پست الزامی است</small>
              </div>

              <div class="form-group">
                <label for="excerpt">{{ t('postExcerpt') }}</label>
                <textarea 
                  id="excerpt"
                  v-model="form.excerpt" 
                  :placeholder="t('writeExcerpt')"
                  rows="3"
                  class="form-textarea"
                ></textarea>
                <small class="form-help">{{ t('thisWillBeShown') }}</small>
              </div>

              <div class="form-group">
                <label for="content">{{ t('postContent') }} *</label>
                <textarea 
                  id="content"
                  v-model="form.content" 
                  required 
                  :placeholder="t('writeContent')"
                  rows="15"
                  class="form-textarea content-editor"
                ></textarea>
                <small class="form-help">{{ t('useLineBreaks') }}</small>
              </div>
            </div>

            <!-- Featured Image Section -->
            <div class="form-section">
              <h2>{{ t('featuredImage') }}</h2>
              
              <div class="image-upload">
                <div v-if="imagePreview" class="image-preview">
                  <img :src="imagePreview" :alt="form.title" />
                  <button @click="removeImage" class="remove-image-btn">
                    <i class="fas fa-times"></i>
                  </button>
                </div>
                
                <div v-else class="image-upload-area" @click="triggerFileInput">
                  <i class="fas fa-cloud-upload-alt"></i>
                  <p>{{ t('clickToUpload') }}</p>
                  <small>{{ t('recommendedSize') }}: 1200x630px</small>
                </div>
                
                <input 
                  ref="fileInput"
                  @change="handleImageUpload"
                  type="file" 
                  accept="image/*"
                  style="display: none"
                />
              </div>
            </div>
          </div>

          <!-- Sidebar -->
          <div class="form-sidebar">
            <!-- Publish Settings -->
            <div class="form-section">
              <h3>{{ t('publishSettings') }}</h3>
              
              <div class="form-group">
                <label for="status">{{ t('status') }}</label>
                <select id="status" v-model="form.status" class="form-select">
                  <option value="draft">{{ t('draft') }}</option>
                  <option value="published">{{ t('published') }}</option>
                  <option value="archived">{{ t('archived') }}</option>
                </select>
              </div>

              <div class="form-group">
                <label for="category">{{ t('category') }} *</label>
                <div class="category-select-wrapper">
                  <select 
                    id="category" 
                    v-model="form.category" 
                    class="form-select"
                    :class="{ 'error': !form.category && submitting }"
                    required
                  >
                    <option value="">{{ t('selectCategory') }}</option>
                    <option v-for="category in categories" :key="category.id" :value="category.id">
                      {{ category.name }}
                    </option>
                  </select>
                  <button type="button" @click="showCreateCategory = true" class="add-category-btn">
                    <i class="fas fa-plus"></i>
                  </button>
                </div>
                <small v-if="!form.category && submitting" class="error-text">انتخاب دسته‌بندی الزامی است</small>
              </div>

              <div class="form-group">
                <label class="checkbox-label">
                  <input v-model="form.is_featured" type="checkbox" />
                  <span class="checkmark"></span>
                  {{ t('isFeatured') }}
                </label>
                <small class="form-help">{{ t('featuredPostsAppear') }}</small>
              </div>
            </div>

            <!-- SEO Settings -->
            <div class="form-section">
              <h3>{{ t('seoSettings') }}</h3>
              
              <div class="form-group">
                <label for="meta_title">{{ t('metaTitle') }}</label>
                <input 
                  id="meta_title"
                  v-model="form.meta_title" 
                  type="text" 
                  :placeholder="t('seoTitleOptional')"
                  class="form-input"
                />
                <small class="form-help">{{ t('leaveEmptyToUse') }}</small>
              </div>

              <div class="form-group">
                <label for="meta_description">{{ t('metaDescription') }}</label>
                <textarea 
                  id="meta_description"
                  v-model="form.meta_description" 
                  :placeholder="t('seoDescriptionOptional')"
                  rows="3"
                  class="form-textarea"
                ></textarea>
                <small class="form-help">{{ t('leaveEmptyToUseExcerpt') }}</small>
              </div>
            </div>

            <!-- Post Preview -->
            <div class="form-section">
              <h3>{{ t('preview') }}</h3>
              <div class="post-preview">
                <div class="preview-meta">
                  <span class="preview-category">{{ selectedCategory?.name || t('category') }}</span>
                  <span class="preview-date">{{ formatDate(new Date()) }}</span>
                </div>
                <h4 class="preview-title">{{ form.title || t('yourPostTitleWillAppearHere') }}</h4>
                <p class="preview-excerpt">{{ form.excerpt || t('yourExcerptWillAppearHere') }}</p>
                <div class="preview-stats">
                  <span class="preview-reading-time">{{ estimatedReadingTime }} {{ t('minRead') }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Form Actions -->
          <div class="form-actions">
            <button type="button" @click="saveDraft" class="btn btn-secondary" :disabled="submitting">
              <i class="fas fa-save"></i>
              {{ t('savingDraft') }}
            </button>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              <i v-if="submitting" class="fas fa-spinner fa-spin"></i>
              <i v-else class="fas fa-paper-plane"></i>
              {{ isEditing ? t('updatePost') : t('publishPost') }}
            </button>
          </div>
        </div>
      </form>
    </div>

    <!-- Create Category Modal -->
    <div v-if="showCreateCategory" class="modal-overlay" @click="showCreateCategory = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ t('createNewCategory') }}</h3>
          <button @click="showCreateCategory = false" class="close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <form @submit.prevent="createCategory" class="modal-body">
          <div class="form-group">
            <label>{{ t('categoryName') }} *</label>
            <input 
              v-model="categoryForm.name" 
              type="text" 
              required 
              :placeholder="t('enterCategoryName')"
            />
          </div>
          
          <div class="form-group">
            <label>{{ t('categoryDescription') }}</label>
            <textarea 
              v-model="categoryForm.description" 
              :placeholder="t('categoryDescriptionPlaceholder')"
              rows="3"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label>{{ t('categoryColor') }}</label>
            <input 
              v-model="categoryForm.color" 
              type="color" 
              class="color-input"
            />
          </div>
          
          <div class="modal-footer">
            <button type="button" @click="showCreateCategory = false" class="btn btn-secondary">
              {{ t('cancel') }}
            </button>
            <button type="submit" class="btn btn-primary" :disabled="creatingCategory">
              <i v-if="creatingCategory" class="fas fa-spinner fa-spin"></i>
              {{ t('createCategory') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBlogStore } from '@/stores/blog'
import { useCategoryStore } from '@/stores/modules/categoryStore'

export default {
  name: 'BlogForm',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const blogStore = useBlogStore()
    const categoryStore = useCategoryStore()
    
    const isEditing = ref(false)
    const submitting = ref(false)
    const creatingCategory = ref(false)
    const showCreateCategory = ref(false)
    const fileInput = ref(null)
    const imagePreview = ref(null)
    
    const form = ref({
      title: '',
      excerpt: '',
      content: '',
      category: '',
      status: 'draft',
      is_featured: false,
      meta_title: '',
      meta_description: '',
      featured_image: null
    })
    
    const categoryForm = ref({
      name: '',
      description: '',
      color: '#007bff'
    })
    
    const categories = computed(() => blogStore.categories)
    const productCategories = computed(() => categoryStore.categories)
    const t = computed(() => blogStore.t)
    
    const selectedCategory = computed(() => {
      return categories.value.find(c => c.id === parseInt(form.value.category))
    })
    
    const estimatedReadingTime = computed(() => {
      const wordsPerMinute = 200
      const wordCount = form.value.content.split(' ').length
      return Math.max(1, Math.round(wordCount / wordsPerMinute))
    })
    
    const fetchData = async () => {
      await Promise.all([
        blogStore.fetchCategories(),
        categoryStore.fetchCategories()
      ])
    }
    
    const loadPost = async () => {
      if (route.params.slug) {
        isEditing.value = true
        try {
          await blogStore.fetchPost(route.params.slug)
          const post = blogStore.currentPost
          if (post) {
            form.value = {
              title: post.title,
              excerpt: post.excerpt,
              content: post.content,
              category: post.category,
              status: post.status,
              is_featured: post.is_featured,
              meta_title: post.meta_title || '',
              meta_description: post.meta_description || '',
              featured_image: null
            }
            
            if (post.featured_image) {
              imagePreview.value = post.featured_image
            }
          }
        } catch (error) {
          console.error('Error loading post:', error)
          router.push('/blog')
        }
      }
    }
    
    const triggerFileInput = () => {
      fileInput.value?.click()
    }
    
    const handleImageUpload = (event) => {
      const file = event.target.files[0]
      if (file) {
        form.value.featured_image = file
        
        // Create preview
        const reader = new FileReader()
        reader.onload = (e) => {
          imagePreview.value = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }
    
    const removeImage = () => {
      form.value.featured_image = null
      imagePreview.value = null
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }
    
    const saveDraft = async () => {
      form.value.status = 'draft'
      await submitForm()
    }
    
    const submitForm = async () => {
      submitting.value = true
      try {
        const formData = new FormData()
        
        // Validate required fields
        if (!form.value.title.trim()) {
          throw new Error('عنوان پست الزامی است')
        }
        if (!form.value.content.trim()) {
          throw new Error('محتوای پست الزامی است')
        }
        if (!form.value.category || form.value.category === '') {
          throw new Error('انتخاب دسته‌بندی الزامی است')
        }
        
        // Append only non-empty fields
        Object.keys(form.value).forEach(key => {
          if (form.value[key] !== null && form.value[key] !== '' && form.value[key] !== undefined) {
            if (key === 'category') {
              // Ensure category is sent as integer
              formData.append(key, parseInt(form.value[key]))
            } else if (key === 'is_featured') {
              // Ensure boolean is sent as string for FormData
              formData.append(key, form.value[key] ? 'true' : 'false')
            } else {
              formData.append(key, form.value[key])
            }
          }
        })
        
        if (isEditing.value) {
          await blogStore.updatePost(route.params.slug, formData)
        } else {
          await blogStore.createPost(formData)
        }
        
        router.push('/blog/dashboard')
      } catch (error) {
        console.error('Error submitting form:', error)
        // Show user-friendly error message
        if (error.message) {
          alert(error.message)
        } else if (error.response?.data) {
          // Handle backend validation errors
          const errorData = error.response.data
          let errorMessage = 'خطا در ارسال فرم: '
          
          if (typeof errorData === 'object') {
            Object.keys(errorData).forEach(key => {
              if (Array.isArray(errorData[key])) {
                errorMessage += `${key}: ${errorData[key].join(', ')}`
              } else {
                errorMessage += `${key}: ${errorData[key]}`
              }
            })
          } else {
            errorMessage += errorData
          }
          
          alert(errorMessage)
        } else {
          alert('خطا در ارسال فرم. لطفاً دوباره تلاش کنید.')
        }
      } finally {
        submitting.value = false
      }
    }
    
    const createCategory = async () => {
      creatingCategory.value = true
      try {
        const newCategory = await blogStore.createCategory(categoryForm.value)
        form.value.category = newCategory.id
        showCreateCategory.value = false
        
        // Reset category form
        categoryForm.value = {
          name: '',
          description: '',
          color: '#007bff'
        }
      } catch (error) {
        console.error('Error creating category:', error)
      } finally {
        creatingCategory.value = false
      }
    }
    
    const formatDate = (date) => {
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    onMounted(async () => {
      await fetchData()
      await loadPost()
    })
    
    return {
      isEditing,
      submitting,
      creatingCategory,
      showCreateCategory,
      fileInput,
      imagePreview,
      form,
      categoryForm,
      categories,
      productCategories,
      selectedCategory,
      estimatedReadingTime,
      t,
      triggerFileInput,
      handleImageUpload,
      removeImage,
      saveDraft,
      submitForm,
      createCategory,
      formatDate
    }
  }
}
</script>

<style scoped>
.blog-form {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding: 2rem 0;
  direction: rtl;
  text-align: right;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-direction: row-reverse;
}

.form-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
}

.back-btn {
  background: none;
  border: 1px solid #dee2e6;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6c757d;
  transition: all 0.3s ease;
  flex-direction: row-reverse;
}

.back-btn:hover {
  background-color: #f8f9fa;
}

.blog-form-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.main-form {
  padding: 2rem;
  width: 100%;
  border-bottom: 1px solid #e9ecef;
}

.form-sidebar {
  padding: 2rem;
  background-color: #f8f9fa;
  width: 100%;
}

.form-section {
  margin-bottom: 2rem;
}

.form-section h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #007bff;
}

.form-section h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-family: inherit;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-input.error,
.form-textarea.error,
.form-select.error {
  border-color: #dc3545;
  box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1);
}

.form-input.error:focus,
.form-textarea.error:focus,
.form-select.error:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.2);
}

.error-text {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #dc3545;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.content-editor {
  min-height: 300px;
  font-family: 'Georgia', serif;
  line-height: 1.6;
}

.form-help {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #6c757d;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  flex-direction: row-reverse;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin: 0;
}

.create-category-btn {
  background: none;
  border: 1px solid #007bff;
  color: #007bff;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.3s ease;
  flex-direction: row-reverse;
}

.create-category-btn:hover {
  background-color: #007bff;
  color: white;
}

.add-category-btn {
  background: none;
  border: 1px solid #007bff;
  color: #007bff;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.3s ease;
  flex-direction: row-reverse;
}

.add-category-btn:hover {
  background-color: #007bff;
  color: white;
}

.image-upload {
  border: 2px dashed #dee2e6;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  transition: border-color 0.3s ease;
}

.image-upload:hover {
  border-color: #007bff;
}

.image-upload-area {
  cursor: pointer;
  color: #6c757d;
}

.image-upload-area i {
  font-size: 2rem;
  margin-bottom: 1rem;
  display: block;
}

.image-preview {
  position: relative;
  display: inline-block;
}

.image-preview img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
}

.remove-image-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.post-preview {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1rem;
}

.preview-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: #6c757d;
  flex-direction: row-reverse;
}

.preview-category {
  background-color: #007bff;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
}

.preview-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  line-height: 1.4;
}

.preview-excerpt {
  color: #6c757d;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  line-height: 1.5;
}

.preview-stats {
  font-size: 0.875rem;
  color: #6c757d;
}

.form-actions {
  padding: 2rem;
  border-top: 1px solid #e9ecef;
  display: flex;
  justify-content: flex-start;
  gap: 1rem;
  flex-direction: row-reverse;
  width: 100%;
  background-color: white;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  flex-direction: row-reverse;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #545b62;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #dee2e6;
  flex-direction: row-reverse;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #dee2e6;
  flex-direction: row-reverse;
}

.color-input {
  height: 40px;
  padding: 0;
  border: none;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .form-actions {
    flex-direction: column;
  }
  
  .form-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .main-form,
  .form-sidebar {
    padding: 1.5rem;
  }
}
</style>
