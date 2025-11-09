<!-- src/views/ProductForm.vue - Vuetify Material Design 3 -->
<template>
  <v-container fluid class="product-form-container" dir="rtl">
    <!-- Breadcrumbs -->
    <v-breadcrumbs
      :items="breadcrumbItems"
      class="px-2 px-sm-4 py-1 py-sm-2"
      divider="/"
      dir="rtl"
    >
      <template v-slot:prepend>
        <v-icon size="small" class="mr-2">mdi-home</v-icon>
      </template>
    </v-breadcrumbs>

    <!-- Page Title -->
    <v-row class="mb-4 mb-sm-6">
      <v-col cols="12">
        <h1 class="text-h4 text-sm-h3 font-weight-bold">
          {{ isEdit ? t('editProduct') : t('addNewProduct') }}
        </h1>
      </v-col>
    </v-row>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-16">
      <v-col cols="12" class="text-center">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
        <p class="text-h6 mt-4">{{ t('loading') }}</p>
      </v-col>
    </v-row>

    <!-- Error State -->
    <v-alert
      v-else-if="error"
      type="error"
      variant="tonal"
      prominent
      class="my-4"
    >
      {{ error }}
    </v-alert>

    <!-- Form -->
    <v-form v-else @submit.prevent="saveProduct" ref="formRef">
      <v-row>
        <!-- Main Form Column -->
        <v-col cols="12" lg="8">
          <!-- Basic Information Card -->
          <v-card elevation="4" rounded="lg" class="mb-4 mb-sm-6">
            <v-card-title class="text-h6 text-sm-h5 font-weight-bold bg-primary pa-4 pa-sm-5">
              <v-icon class="mr-2" :size="display.xs.value ? 'default' : 'large'">mdi-information</v-icon>
              اطلاعات پایه
            </v-card-title>

            <v-card-text class="pa-4 pa-sm-5 pa-md-6">
              <!-- Product Name -->
              <v-text-field
                v-model="product.name"
                :label="t('productName')"
                prepend-inner-icon="mdi-tag"
                variant="outlined"
                rounded="lg"
                :rules="[v => !!v || 'نام محصول الزامی است']"
                required
              ></v-text-field>

              <!-- Description -->
              <div class="description-editor-wrapper">
                <label class="text-body-2 mb-2 d-block">
                  <v-icon size="small" class="mr-1">mdi-text</v-icon>
                  {{ t('description') }} <span class="text-error">*</span>
                </label>
                <TiptapEditor 
                  v-model="product.description" 
                  class="description-editor"
                />
                <div v-if="!descriptionValid && descriptionTouched" class="text-error text-caption mt-1">
                  توضیحات الزامی است
                </div>
              </div>

              <!-- Price and Stock Row -->
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model.number="product.price"
                    :label="t('price') + ' (تومان)'"
                    prepend-inner-icon="mdi-currency-usd"
                    variant="outlined"
                    rounded="lg"
                    type="number"
                    step="1"
                    min="0"
                    :rules="[v => v >= 0 || 'قیمت باید مثبت باشد']"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model.number="product.stock"
                    :label="t('stock')"
                    prepend-inner-icon="mdi-package-variant"
                    variant="outlined"
                    rounded="lg"
                    type="number"
                    min="0"
                    :rules="[v => v >= 0 || 'موجودی باید مثبت باشد']"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Category Selection Card -->
          <v-card elevation="4" rounded="lg" class="mb-4 mb-sm-6">
            <v-card-title class="text-h6 text-sm-h5 font-weight-bold bg-secondary pa-4 pa-sm-5">
              <v-icon class="mr-2" :size="display.xs.value ? 'default' : 'large'">mdi-shape</v-icon>
              دسته‌بندی محصول
            </v-card-title>

            <v-card-text class="pa-4 pa-sm-5 pa-md-6">
              <v-alert
                type="info"
                variant="tonal"
                density="compact"
                class="mb-4"
              >
                <small>ساختار: بخش → دسته‌بندی → زیردسته (زیردسته‌ها از طریق دسته‌بندی به بخش متصل می‌شوند)</small>
              </v-alert>

              <!-- Department Filter -->
              <v-select
                v-model="selectedDepartment"
                :items="departments"
                item-title="name"
                item-value="id"
                label="بخش (برای فیلتر)"
                prepend-inner-icon="mdi-filter"
                variant="outlined"
                rounded="lg"
                clearable
                hint="انتخاب بخش، دسته‌بندی‌ها را فیلتر می‌کند"
                persistent-hint
                class="mb-4"
                @update:model-value="onDepartmentChange"
              ></v-select>

              <!-- Category Filter -->
              <v-select
                v-model="selectedCategory"
                :items="filteredCategories"
                item-title="name"
                item-value="id"
                label="دسته‌بندی (برای فیلتر)"
                prepend-inner-icon="mdi-filter"
                variant="outlined"
                rounded="lg"
                clearable
                hint="انتخاب دسته‌بندی، زیردسته‌ها را فیلتر می‌کند"
                persistent-hint
                class="mb-4"
                :disabled="!selectedDepartment && categories.length === 0"
                @update:model-value="onCategoryChange"
              ></v-select>

              <!-- Subcategory Selection (Required) -->
              <v-select
                v-model="product.subcategory"
                :items="filteredSubcategories"
                item-title="name"
                item-value="id"
                label="زیردسته *"
                prepend-inner-icon="mdi-check-circle"
                variant="outlined"
                rounded="lg"
                hint="محصول شما در این زیردسته قرار می‌گیرد (الزامی)"
                persistent-hint
                :rules="[v => !!v || 'انتخاب زیردسته الزامی است']"
                required
                color="success"
              >
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props">
                    <template v-slot:subtitle v-if="!selectedDepartment && item.raw.departments && item.raw.departments.length > 0">
                      {{ item.raw.departments[0].name }}
                    </template>
                  </v-list-item>
                </template>
              </v-select>

              <!-- Selected Path Display -->
              <v-alert
                v-if="product.subcategory && selectedSubcategoryObject"
                type="success"
                variant="tonal"
                class="mt-4"
              >
                <v-icon class="mr-2">mdi-route</v-icon>
                <strong>مسیر انتخاب شده:</strong>
                <div class="mt-2 font-weight-bold">
                  {{ getSelectedFullPath() }}
                </div>
              </v-alert>
            </v-card-text>
          </v-card>

          <!-- SEO Settings Card -->
          <v-card elevation="4" rounded="lg" class="mb-4 mb-sm-6">
            <v-expansion-panels v-model="seoPanel" variant="accordion" multiple>
              <v-expansion-panel>
                <v-expansion-panel-title class="text-h6 text-sm-h5 font-weight-bold">
                  <v-icon class="mr-2" :size="display.xs.value ? 'default' : 'large'">mdi-search-web</v-icon>
                  تنظیمات SEO (بهینه‌سازی موتور جستجو)
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <v-card-text class="pa-4 pa-sm-5 pa-md-6">
                    <!-- Meta Title -->
                    <v-text-field
                      v-model="product.meta_title"
                      label="عنوان متا (Meta Title)"
                      prepend-inner-icon="mdi-format-title"
                      variant="outlined"
                      rounded="lg"
                      hint="حداکثر 60 کاراکتر - عنوانی که در نتایج جستجو نمایش داده می‌شود"
                      :counter="60"
                      maxlength="60"
                      persistent-hint
                      class="mb-4"
                    ></v-text-field>

                    <!-- Meta Description -->
                    <v-textarea
                      v-model="product.meta_description"
                      label="توضیحات متا (Meta Description)"
                      prepend-inner-icon="mdi-text"
                      variant="outlined"
                      rounded="lg"
                      rows="3"
                      hint="حداکثر 160 کاراکتر - توضیحاتی که در نتایج جستجو نمایش داده می‌شود"
                      :counter="160"
                      maxlength="160"
                      persistent-hint
                      class="mb-4"
                    ></v-textarea>

                    <!-- Image Alt Text -->
                    <v-text-field
                      v-model="product.image_alt_text"
                      label="متن جایگزین تصویر (Image Alt Text)"
                      prepend-inner-icon="mdi-image-text"
                      variant="outlined"
                      rounded="lg"
                      hint="متن جایگزین برای تصویر اصلی محصول (برای SEO و دسترسی‌پذیری)"
                      :counter="125"
                      maxlength="125"
                      persistent-hint
                      class="mb-4"
                    ></v-text-field>

                    <!-- Canonical URL -->
                    <v-text-field
                      v-model="product.canonical_url"
                      label="آدرس کانونیکال (Canonical URL)"
                      prepend-inner-icon="mdi-link-variant"
                      variant="outlined"
                      rounded="lg"
                      type="url"
                      hint="آدرس کانونیکال برای جلوگیری از محتوای تکراری در SEO"
                      persistent-hint
                      class="mb-4"
                    ></v-text-field>

                    <!-- Open Graph Image -->
                    <v-file-input
                      v-model="product.og_image"
                      label="تصویر Open Graph (برای شبکه‌های اجتماعی)"
                      prepend-inner-icon="mdi-image"
                      variant="outlined"
                      rounded="lg"
                      accept="image/*"
                      hint="تصویری که در هنگام اشتراک‌گذاری محصول در شبکه‌های اجتماعی نمایش داده می‌شود"
                      persistent-hint
                      class="mb-4"
                      show-size
                    >
                      <template v-slot:prepend-inner>
                        <v-icon>mdi-image</v-icon>
                      </template>
                    </v-file-input>

                    <!-- Schema Markup (JSON-LD) -->
                    <v-textarea
                      v-model="product.schema_markup"
                      label="Schema Markup (JSON-LD)"
                      prepend-inner-icon="mdi-code-json"
                      variant="outlined"
                      rounded="lg"
                      rows="6"
                      hint="کد JSON-LD برای ساختاردهی داده‌ها و بهبود نمایش در نتایج جستجو"
                      persistent-hint
                      class="mb-2"
                    ></v-textarea>

                    <v-alert
                      type="info"
                      variant="tonal"
                      density="compact"
                      class="mt-4"
                    >
                      <small>
                        <strong>راهنما:</strong><br>
                        • عنوان متا: عنوان کوتاه و جذاب (حداکثر 60 کاراکتر)<br>
                        • توضیحات متا: خلاصه‌ای از محصول (حداکثر 160 کاراکتر)<br>
                        • متن جایگزین تصویر: برای دسترسی‌پذیری و SEO<br>
                        • آدرس کانونیکال: جلوگیری از محتوای تکراری<br>
                        • تصویر Open Graph: برای نمایش بهتر در شبکه‌های اجتماعی<br>
                        • Schema Markup: کد JSON-LD برای Rich Snippets
                      </small>
                    </v-alert>
                  </v-card-text>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card>

          <!-- Product Images Card -->
          <v-card elevation="4" rounded="lg" class="mb-4 mb-sm-6">
            <v-card-title class="text-h6 text-sm-h5 font-weight-bold bg-accent pa-4 pa-sm-5">
              <v-icon class="mr-2" :size="display.xs.value ? 'default' : 'large'">mdi-image-multiple</v-icon>
              {{ t('productImages') }} (حداکثر 20 تصویر)
            </v-card-title>

            <v-card-text class="pa-3 pa-sm-4 pa-md-6">
              <!-- Upload Zone -->
              <div
                class="image-upload-zone"
                :class="{ 'drag-over': isDragOver, 'has-images': uploadedImages.length > 0 }"
                @drop="handleDrop"
                @dragover.prevent="isDragOver = true"
                @dragleave="isDragOver = false"
                @click="triggerFileInput"
              >
                <!-- Empty State -->
                <div v-if="uploadedImages.length === 0" class="text-center pa-6 pa-sm-8">
                  <v-icon :size="display.xs.value ? 48 : 64" color="primary">mdi-cloud-upload</v-icon>
                  <p class="text-subtitle-1 text-sm-h6 mt-3 mt-sm-4">{{ t('dragDropImages') }}</p>
                  <p class="text-caption text-sm-body-2 text-medium-emphasis">{{ t('orClickToSelect') }}</p>
                </div>

                <!-- Images Grid -->
                <v-row v-else dense class="pa-1 pa-sm-2">
                  <v-col
                    v-for="(image, index) in uploadedImages"
                    :key="index"
                    cols="6"
                    sm="6"
                    lg="3"
                  >
                    <v-card
                      elevation="2"
                      rounded="lg"
                      class="image-item"
                      :class="{ 'primary-image': index === 0 }"
                    >
                      <v-img
                        :src="image.preview"
                        aspect-ratio="1"
                        cover
                      >
                        <template v-slot:placeholder>
                          <v-row
                            class="fill-height ma-0"
                            align="center"
                            justify="center"
                          >
                            <v-progress-circular
                              indeterminate
                              color="primary"
                            ></v-progress-circular>
                          </v-row>
                        </template>

                        <!-- Overlay -->
                        <div class="image-overlay">
                          <v-btn
                            icon="mdi-delete"
                            color="error"
                            size="small"
                            @click.stop="removeImage(index)"
                          ></v-btn>
                        </div>

                        <!-- Primary Badge -->
                        <v-chip
                          v-if="index === 0"
                          color="success"
                          size="small"
                          class="primary-badge"
                          prepend-icon="mdi-star"
                        >
                          {{ t('primary') }}
                        </v-chip>
                      </v-img>
                    </v-card>
                  </v-col>

                  <!-- Add More Button -->
                  <v-col
                    v-if="uploadedImages.length < 20"
                    cols="6"
                    sm="6"
                    lg="3"
                  >
                    <v-card
                      elevation="2"
                      rounded="lg"
                      class="add-more-card"
                      @click.stop="triggerFileInput"
                    >
                      <div class="d-flex flex-column align-center justify-center fill-height">
                        <v-icon size="48" color="primary">mdi-plus</v-icon>
                        <span class="text-body-2 mt-2">{{ t('addMore') }}</span>
                      </div>
                    </v-card>
                  </v-col>
                </v-row>
              </div>

              <input
                ref="fileInput"
                type="file"
                multiple
                @change="handleFileSelect"
                accept="image/*"
                style="display: none"
              >

              <v-alert
                v-if="imageError"
                type="error"
                variant="tonal"
                density="compact"
                class="mt-4"
              >
                {{ imageError }}
              </v-alert>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Sidebar Column -->
        <v-col cols="12" lg="4">
          <!-- Status Card -->
          <v-card elevation="4" rounded="lg" class="mb-4 mb-sm-6 sticky-card">
            <v-card-title class="text-subtitle-1 text-sm-h6 font-weight-bold pa-4 pa-sm-5">
              <v-icon class="mr-2" :size="display.xs.value ? 'default' : 'large'">mdi-cog</v-icon>
              تنظیمات
            </v-card-title>

            <v-card-text class="pa-3 pa-sm-4">
              <!-- Active Status -->
              <v-switch
                v-model="product.is_active"
                :label="t('productIsActive')"
                color="success"
                inset
                hide-details
              ></v-switch>
            </v-card-text>

            <v-divider></v-divider>

            <!-- Action Buttons -->
            <v-card-actions class="pa-3 pa-sm-4 flex-column ga-2 ga-sm-3">
              <v-btn
                type="submit"
                color="primary"
                :size="display.xs.value ? 'large' : 'x-large'"
                prepend-icon="mdi-content-save"
                block
                variant="elevated"
                rounded="lg"
                :loading="submitting"
                :disabled="submitting"
              >
                {{ submitting ? t('saving') : t('saveProduct') }}
              </v-btn>

              <v-btn
                color="secondary"
                :size="display.xs.value ? 'default' : 'large'"
                prepend-icon="mdi-close"
                block
                variant="outlined"
                rounded="lg"
                to="/products"
              >
                {{ t('cancel') }}
              </v-btn>
            </v-card-actions>
          </v-card>

          <!-- Help Card -->
          <v-card elevation="2" rounded="lg" color="info" variant="tonal">
            <v-card-text class="pa-3 pa-sm-4">
              <div class="d-flex align-start">
                <v-icon class="mr-2" :size="display.xs.value ? 'small' : 'default'">mdi-information</v-icon>
                <div>
                  <strong class="text-body-2 text-sm-body-1">راهنما:</strong>
                  <ul class="text-caption text-sm-body-2 mt-2">
                    <li>تصویر اول به عنوان تصویر اصلی نمایش داده می‌شود</li>
                    <li>می‌توانید تا 20 تصویر آپلود کنید</li>
                    <li>فرمت‌های قابل قبول: JPG, PNG, GIF</li>
                  </ul>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import { useProductStore } from '@/stores/modules/productStore';
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useDisplay } from 'vuetify';
import TiptapEditor from '@/components/TiptapEditor.vue';

export default {
  name: 'ProductForm',
  components: {
    TiptapEditor
  },
  setup() {
    const productStore = useProductStore();
    const route = useRoute();
    const router = useRouter();
    const display = useDisplay();

    const isEdit = computed(() => route.name === 'EditProduct');
    const productId = computed(() => route.params.id);

    const formRef = ref(null);
    const submitting = ref(false);
    const uploadedImages = ref([]);
    const isDragOver = ref(false);
    const imageError = ref('');
    const fileInput = ref(null);
    const descriptionTouched = ref(false);

    // Cascading selector state
    const departments = ref([]);
    const categories = ref([]);
    const subcategories = ref([]);
    const selectedDepartment = ref('');
    const selectedCategory = ref('');
    const filteredCategories = ref([]);
    const filteredSubcategories = ref([]);

    const product = ref({
      name: '',
      subcategory: '',
      description: '',
      price: 0,
      stock: 0,
      image: null,
      is_active: true,
      // SEO fields
      meta_title: '',
      meta_description: '',
      image_alt_text: '',
      canonical_url: '',
      og_image: null,
      schema_markup: ''
    });

    // SEO expansion panel state
    const seoPanel = ref([]);

    const loading = computed(() => productStore.loading);
    const error = computed(() => productStore.error);

    // Description validation
    const descriptionValid = computed(() => {
      if (!product.value.description) return false;
      
      // Handle both string and empty cases
      const description = product.value.description.trim();
      if (!description || description === '<p></p>' || description === '<p><br></p>') {
        return false;
      }
      
      // Strip HTML tags and check if there's actual text content
      try {
        if (typeof document !== 'undefined') {
          const tempDiv = document.createElement('div');
          tempDiv.innerHTML = description;
          const textContent = tempDiv.textContent || tempDiv.innerText || '';
          return textContent.trim().length > 0;
        }
        // Fallback for SSR: check if description has meaningful content
        // Remove HTML tags using regex (basic approach)
        const textOnly = description.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim();
        return textOnly.length > 0;
      } catch (e) {
        // Fallback: just check if it's not empty
        return description.length > 0;
      }
    });

    // Watch description changes to mark as touched
    watch(() => product.value.description, () => {
      descriptionTouched.value = true;
    });

    // Get selected subcategory object
    const selectedSubcategoryObject = computed(() => {
      if (!product.value.subcategory) return null;
      return subcategories.value.find(sub => sub.id === parseInt(product.value.subcategory));
    });

    const breadcrumbItems = computed(() => {
      if (isEdit.value) {
        return [
          { title: t.value('home'), to: '/', disabled: false },
          { title: t.value('products'), to: '/products', disabled: false },
          { title: product.value?.name || t.value('loading'), to: product.value ? `/products/${product.value.id}` : undefined, disabled: false },
          { title: t.value('edit'), disabled: true }
        ];
      }
      return [
        { title: t.value('home'), to: '/', disabled: false },
        { title: t.value('products'), to: '/products', disabled: false },
        { title: t.value('addNewProduct'), disabled: true }
      ];
    });

    const triggerFileInput = () => {
      fileInput.value.click();
    };

    const handleFileSelect = (event) => {
      const files = Array.from(event.target.files);
      addImages(files);
    };

    const handleDrop = (event) => {
      event.preventDefault();
      isDragOver.value = false;
      const files = Array.from(event.dataTransfer.files);
      addImages(files);
    };

    const addImages = (files) => {
      imageError.value = '';

      const imageFiles = files.filter(file => file.type.startsWith('image/'));

      if (imageFiles.length === 0) {
        imageError.value = t.value('onlyImagesAllowed') || 'فقط فایل‌های تصویری مجاز هستند';
        return;
      }

      if (uploadedImages.value.length + imageFiles.length > 20) {
        imageError.value = t.value('max20ImagesExceeded') || 'حداکثر 20 تصویر مجاز است';
        return;
      }

      imageFiles.forEach(file => {
        const reader = new FileReader();
        reader.onload = (e) => {
          uploadedImages.value.push({
            file: file,
            preview: e.target.result
          });
        };
        reader.readAsDataURL(file);
      });
    };

    const removeImage = (index) => {
      uploadedImages.value.splice(index, 1);
    };

    // Filtering logic for cascading dropdowns
    const onDepartmentChange = () => {
      if (selectedDepartment.value) {
        filteredCategories.value = categories.value.filter(cat =>
          cat.departments && cat.departments.some(d => d.id === parseInt(selectedDepartment.value))
        );
      } else {
        filteredCategories.value = categories.value;
      }

      if (selectedCategory.value && !filteredCategories.value.find(c => c.id === parseInt(selectedCategory.value))) {
        selectedCategory.value = '';
      }

      filterSubcategories();
    };

    const onCategoryChange = () => {
      filterSubcategories();
    };

    const filterSubcategories = () => {
      let filtered = subcategories.value;

      if (selectedDepartment.value) {
        filtered = filtered.filter(sub =>
          sub.departments && sub.departments.some(d => d.id === parseInt(selectedDepartment.value))
        );
      }

      if (selectedCategory.value) {
        filtered = filtered.filter(sub =>
          sub.categories && sub.categories.some(c => c.id === parseInt(selectedCategory.value))
        );
      }

      filteredSubcategories.value = filtered;

      if (product.value.subcategory && !filtered.find(s => s.id === parseInt(product.value.subcategory))) {
        product.value.subcategory = '';
      }
    };

    const getFullPath = (subcategory) => {
      if (!subcategory) return '';

      const parts = [];
      if (subcategory.departments && subcategory.departments.length > 0) {
        parts.push(subcategory.departments[0].name);
      }
      if (subcategory.categories && subcategory.categories.length > 0) {
        parts.push(subcategory.categories[0].name);
      }
      parts.push(subcategory.name);

      return parts.join(' ← ');
    };

    const getSelectedFullPath = () => {
      if (!selectedSubcategoryObject.value) return '';
      return getFullPath(selectedSubcategoryObject.value);
    };

    const fetchFormData = async () => {
      try {
        const api = (await import('@/services/api')).default;

        const [deptResponse, catResponse, subResponse] = await Promise.all([
          api.getDepartments(),
          api.getCategories(),
          api.getSubcategories()
        ]);

        departments.value = deptResponse.data.results || deptResponse.data;
        categories.value = catResponse.data.results || catResponse.data;
        subcategories.value = subResponse.data.results || subResponse.data;

        filteredCategories.value = categories.value;
        filteredSubcategories.value = subcategories.value;

        console.log('Loaded data:', {
          departments: departments.value.length,
          categories: categories.value.length,
          subcategories: subcategories.value.length
        });
      } catch (error) {
        console.error('Error fetching form data:', error);
      }
    };

    const saveProduct = async () => {
      // Mark description as touched
      descriptionTouched.value = true;
      
      // Validate form fields
      const { valid } = await formRef.value.validate();
      if (!valid) return;

      // Validate description
      if (!descriptionValid.value) {
        return;
      }

      submitting.value = true;

      try {
        const formData = new FormData();

        Object.keys(product.value).forEach(key => {
          // Skip image and og_image fields (handled separately)
          if (key !== 'image' && key !== 'og_image') {
            const value = product.value[key];
            // Only append if value is not null/undefined/empty string
            if (value !== null && value !== undefined && value !== '') {
              formData.append(key, value);
            }
          }
        });

        // Handle og_image file upload
        if (product.value.og_image && product.value.og_image instanceof File) {
          formData.append('og_image', product.value.og_image);
        }

        uploadedImages.value.forEach(image => {
          if (image.file) {
            formData.append('images', image.file);
          }
        });

        let response;
        if (isEdit.value) {
          response = await productStore.updateProduct(productId.value, formData);
        } else {
          response = await productStore.createProduct(formData);
        }

        router.push(`/products/${response.id}`);
      } catch (error) {
        console.error('Error saving product:', error);
      } finally {
        submitting.value = false;
      }
    };

    onMounted(async () => {
      await fetchFormData();

      if (isEdit.value) {
        await productStore.fetchProduct(productId.value);

        if (productStore.currentProduct) {
          product.value = { ...productStore.currentProduct };

          // Handle subcategories - can be array (ManyToMany) or single value
          let subcategoryId = null;
          if (product.value.subcategories && Array.isArray(product.value.subcategories) && product.value.subcategories.length > 0) {
            // If it's an array, take the first one
            subcategoryId = product.value.subcategories[0];
          } else if (product.value.subcategory) {
            // If it's a single value
            subcategoryId = product.value.subcategory;
          }

          if (subcategoryId) {
            product.value.subcategory = subcategoryId;
            const sub = subcategories.value.find(s => s.id === parseInt(subcategoryId));
            if (sub) {
              if (sub.departments && sub.departments.length > 0) {
                selectedDepartment.value = sub.departments[0].id;
                onDepartmentChange();
              }
              if (sub.categories && sub.categories.length > 0) {
                selectedCategory.value = sub.categories[0].id;
                onCategoryChange();
              }
            }
          }

          // Initialize SEO fields if they don't exist
          if (!product.value.meta_title) product.value.meta_title = '';
          if (!product.value.meta_description) product.value.meta_description = '';
          if (!product.value.image_alt_text) product.value.image_alt_text = '';
          if (!product.value.canonical_url) product.value.canonical_url = '';
          if (!product.value.schema_markup) product.value.schema_markup = '';
          // og_image will be null for existing products (file input, user needs to upload new one to change)
          if (!product.value.og_image) product.value.og_image = null;

          if (productStore.currentProduct.images && productStore.currentProduct.images.length > 0) {
            uploadedImages.value = productStore.currentProduct.images.map(img => ({
              file: null,
              preview: img.image_url || img.image,
              id: img.id,
              is_primary: img.is_primary
            }));
          }
        }
      }
    });

    const t = computed(() => productStore.t);

    return {
      isEdit,
      product,
      departments,
      categories,
      subcategories,
      selectedDepartment,
      selectedCategory,
      filteredCategories,
      filteredSubcategories,
      selectedSubcategoryObject,
      loading,
      error,
      submitting,
      uploadedImages,
      isDragOver,
      imageError,
      fileInput,
      formRef,
      breadcrumbItems,
      display,
      descriptionTouched,
      descriptionValid,
      triggerFileInput,
      handleFileSelect,
      handleDrop,
      removeImage,
      onDepartmentChange,
      onCategoryChange,
      getFullPath,
      getSelectedFullPath,
      saveProduct,
      seoPanel,
      t
    };
  }
};
</script>

<style scoped>
/* Image Upload Zone */
.image-upload-zone {
  border: 2px dashed rgb(var(--v-theme-primary));
  border-radius: 16px;
  min-height: 200px;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: rgba(var(--v-theme-surface), 1);
}

.image-upload-zone:hover {
  border-color: rgb(var(--v-theme-secondary));
  background-color: rgba(var(--v-theme-primary), 0.05);
}

.image-upload-zone.drag-over {
  border-color: rgb(var(--v-theme-success));
  background-color: rgba(var(--v-theme-success), 0.1);
  transform: scale(1.02);
}

.image-upload-zone.has-images {
  min-height: auto;
  border-style: solid;
}

/* Image Item */
.image-item {
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.image-item:hover {
  transform: scale(1.05);
}

.image-item.primary-image {
  border: 3px solid rgb(var(--v-theme-success));
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-item:hover .image-overlay {
  opacity: 1;
}

.primary-badge {
  position: absolute;
  top: 8px;
  left: 8px;
}

/* Add More Card */
.add-more-card {
  aspect-ratio: 1;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px dashed rgb(var(--v-theme-primary));
}

.add-more-card:hover {
  border-color: rgb(var(--v-theme-secondary));
  background-color: rgba(var(--v-theme-primary), 0.05);
  transform: scale(1.05);
}

/* Sticky Card */
.sticky-card {
  position: sticky;
  top: 80px;
}

/* Responsive */
@media (max-width: 1280px) {
  .sticky-card {
    position: relative;
    top: 0;
  }
}

/* Mobile responsive adjustments */
@media (max-width: 600px) {
  .image-upload-zone {
    min-height: 150px;
  }
  
  .image-item {
    border-width: 2px;
  }
  
  .image-item.primary-image {
    border-width: 2px;
  }
}

/* Container width improvements for better desktop experience */
.product-form-container {
  max-width: 100%;
  padding-left: 16px;
  padding-right: 16px;
  direction: rtl;
  text-align: right;
}

.product-form-container :deep(.v-card-title) {
  text-align: right;
  justify-content: flex-start;
}

.product-form-container :deep(.v-text-field),
.product-form-container :deep(.v-textarea),
.product-form-container :deep(.v-select) {
  text-align: right;
}

.product-form-container :deep(.v-text-field input),
.product-form-container :deep(.v-textarea textarea) {
  text-align: right;
  direction: rtl;
}

.product-form-container :deep(.v-list-item-title),
.product-form-container :deep(.v-list-item-subtitle) {
  text-align: right;
}

.product-form-container h1 {
  text-align: right;
  direction: rtl;
}

.product-form-container :deep(.v-switch .v-label) {
  text-align: right;
  margin-right: 8px;
  margin-left: 0;
}

.product-form-container :deep(.v-breadcrumbs) {
  direction: rtl;
  text-align: right;
}

.product-form-container :deep(.v-alert) {
  text-align: right;
  direction: rtl;
}

.product-form-container ul {
  text-align: right;
  direction: rtl;
  padding-right: 20px;
  padding-left: 0;
}

.product-form-container ul li {
  text-align: right;
  direction: rtl;
}

.description-editor-wrapper {
  margin-bottom: 16px;
}

.description-editor-wrapper label {
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.description-editor {
  margin-top: 8px;
}

.description-editor :deep(.tiptap-editor) {
  border-radius: 8px;
  overflow: hidden;
}

@media (min-width: 960px) {
  .product-form-container {
    max-width: 100%;
    padding-left: 24px;
    padding-right: 24px;
  }
}

@media (min-width: 1280px) {
  .product-form-container {
    max-width: 1600px;
    margin: 0 auto;
    padding-left: 32px;
    padding-right: 32px;
  }
}

@media (min-width: 1920px) {
  .product-form-container {
    max-width: 1800px;
    margin: 0 auto;
    padding-left: 40px;
    padding-right: 40px;
  }
}
</style>
