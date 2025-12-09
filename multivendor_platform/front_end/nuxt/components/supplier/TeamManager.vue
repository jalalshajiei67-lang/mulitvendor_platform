<template>
  <div class="team-manager" dir="rtl">
    <v-card elevation="2">
      <v-card-title class="text-h5 font-weight-bold d-flex align-center justify-space-between">
        <div>
          <v-icon color="primary" class="me-2">mdi-account-group</v-icon>
          مدیریت اعضای تیم
        </div>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="openForm()"
          data-tour="add-team-button"
        >
          افزودن عضو تیم
        </v-btn>
      </v-card-title>

      <v-card-text>
        <!-- Loading State -->
        <v-row v-if="loading" justify="center" class="my-8">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-row>

        <!-- Team List -->
        <v-row v-else-if="members.length > 0">
          <v-col
            v-for="member in members"
            :key="member.id"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card class="team-member-card" elevation="3">
              <v-avatar
                :size="120"
                class="mx-auto mt-4"
              >
                <v-img
                  v-if="member.photo"
                  :src="formatImageUrl(member.photo)"
                  cover
                >
                  <template v-slot:placeholder>
                    <v-skeleton-loader type="avatar" />
                  </template>
                </v-img>
                <v-icon v-else size="60" color="grey-lighten-1">
                  mdi-account-circle
                </v-icon>
              </v-avatar>

              <v-card-text class="text-center">
                <h3 class="text-h6 font-weight-bold mb-1">
                  {{ member.name }}
                </h3>
                <p class="text-subtitle-2 text-primary mb-2">
                  {{ member.position }}
                </p>
                <p v-if="member.bio" class="text-caption text-medium-emphasis line-clamp-2">
                  {{ member.bio }}
                </p>
                <v-chip size="x-small" variant="outlined" class="mt-2">
                  ترتیب: {{ member.sort_order || 0 }}
                </v-chip>
              </v-card-text>

              <v-card-actions>
                <v-btn
                  icon="mdi-pencil"
                  size="small"
                  variant="text"
                  color="primary"
                  @click="openForm(member)"
                ></v-btn>
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="error"
                  @click="confirmDelete(member)"
                ></v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <!-- Empty State -->
        <v-row v-else justify="center" class="my-8">
          <v-col cols="12" class="text-center">
            <v-icon size="80" color="grey-lighten-2">mdi-account-group</v-icon>
            <h3 class="text-h6 mt-3">هنوز عضوی به تیم اضافه نشده</h3>
            <p class="text-body-2 text-medium-emphasis mb-4">
              اعضای تیم خود را معرفی کنید
            </p>
            <v-btn color="primary" prepend-icon="mdi-plus" @click="openForm()">
              افزودن اولین عضو
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Form Dialog -->
    <v-dialog v-model="formDialog" max-width="600" persistent>
      <v-card>
        <v-card-title class="text-h6 font-weight-bold">
          {{ editingMember ? 'ویرایش عضو تیم' : 'افزودن عضو تیم' }}
        </v-card-title>

        <v-card-text>
          <v-form ref="formRef" v-model="formValid">
            <v-row>
              <v-col cols="12">
                <div class="text-center mb-4">
                  <v-avatar :size="120">
                    <v-img
                      v-if="photoPreview"
                      :src="photoPreview"
                      cover
                    ></v-img>
                    <v-icon v-else size="60" color="grey-lighten-1">
                      mdi-account-circle
                    </v-icon>
                  </v-avatar>
                </div>
                <v-file-input
                  v-model="photoFile"
                  label="عکس عضو تیم"
                  prepend-icon="mdi-camera"
                  accept="image/*"
                  variant="outlined"
                  @change="onPhotoChange"
                  hint="عکس پروفایل عضو تیم"
                ></v-file-input>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model="formData.name"
                  label="نام و نام خانوادگی *"
                  prepend-icon="mdi-account"
                  variant="outlined"
                  :rules="[v => !!v || 'نام الزامی است']"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model="formData.position"
                  label="سمت *"
                  prepend-icon="mdi-briefcase"
                  variant="outlined"
                  :rules="[v => !!v || 'سمت الزامی است']"
                  required
                  placeholder="مثال: مدیر فنی، مدیرعامل، ..."
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="formData.bio"
                  label="بیوگرافی"
                  prepend-icon="mdi-text"
                  variant="outlined"
                  rows="4"
                  hint="معرفی کوتاه عضو تیم"
                ></v-textarea>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model.number="formData.sort_order"
                  label="ترتیب نمایش"
                  prepend-icon="mdi-sort"
                  type="number"
                  variant="outlined"
                  hint="عدد کمتر = نمایش زودتر"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-btn color="primary" :loading="saving" :disabled="!formValid" @click="saveMember">
            {{ editingMember ? 'به‌روزرسانی' : 'ذخیره' }}
          </v-btn>
          <v-btn variant="text" @click="closeForm">انصراف</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">حذف عضو تیم</v-card-title>
        <v-card-text>
          آیا مطمئن هستید که می‌خواهید این عضو را از تیم حذف کنید؟
        </v-card-text>
        <v-card-actions>
          <v-btn color="error" :loading="deleting" @click="deleteMember">حذف</v-btn>
          <v-btn variant="text" @click="deleteDialog = false">انصراف</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000" location="top">
      {{ snackbarMessage }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSupplierTeamApi, type SupplierTeamMember } from '~/composables/useSupplierTeamApi'
import { formatImageUrl } from '~/utils/imageUtils'

const teamApi = useSupplierTeamApi()

const members = ref<SupplierTeamMember[]>([])
const loading = ref(false)
const formDialog = ref(false)
const deleteDialog = ref(false)
const formRef = ref()
const formValid = ref(false)
const saving = ref(false)
const deleting = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const editingMember = ref<SupplierTeamMember | null>(null)
const memberToDelete = ref<SupplierTeamMember | null>(null)
const photoFile = ref<File[]>([])
const photoPreview = ref<string>('')

const formData = ref({
  name: '',
  position: '',
  bio: '',
  sort_order: 0
})

const loadMembers = async () => {
  loading.value = true
  try {
    members.value = await teamApi.getTeamMembers()
  } catch (error) {
    console.error('Error loading team members:', error)
  } finally {
    loading.value = false
  }
}

const openForm = (member?: SupplierTeamMember) => {
  if (member) {
    editingMember.value = member
    formData.value = {
      name: member.name,
      position: member.position,
      bio: member.bio || '',
      sort_order: member.sort_order || 0
    }
    if (member.photo) {
      photoPreview.value = formatImageUrl(member.photo)
    }
  } else {
    editingMember.value = null
    formData.value = {
      name: '',
      position: '',
      bio: '',
      sort_order: 0
    }
    photoPreview.value = ''
    photoFile.value = []
  }
  formDialog.value = true
}

const closeForm = () => {
  formDialog.value = false
  editingMember.value = null
  photoPreview.value = ''
  photoFile.value = []
  formRef.value?.reset()
}

const onPhotoChange = (event: Event) => {
  const files = (event.target as HTMLInputElement).files
  if (files && files[0]) {
    const reader = new FileReader()
    reader.onload = (e) => {
      photoPreview.value = e.target?.result as string
    }
    reader.readAsDataURL(files[0])
  }
}

const saveMember = async () => {
  if (!formValid.value) return

  saving.value = true

  try {
    const data: any = {
      ...formData.value
    }

    if (photoFile.value.length > 0) {
      data.photo = photoFile.value[0]
    }

    if (editingMember.value) {
      await teamApi.updateTeamMember(editingMember.value.id!, data)
      snackbarMessage.value = 'عضو تیم با موفقیت به‌روزرسانی شد'
    } else {
      await teamApi.createTeamMember(data)
      snackbarMessage.value = 'عضو تیم با موفقیت اضافه شد'
    }

    snackbarColor.value = 'success'
    snackbar.value = true
    closeForm()
    await loadMembers()
  } catch (error: any) {
    console.error('Error saving team member:', error)
    console.error('Error data:', error?.data)
    // Extract error message from response
    let errorMessage = 'خطا در ذخیره عضو تیم'
    
    if (error?.data) {
      // Check for field-specific errors (Django REST Framework format)
      const fieldErrors: string[] = []
      Object.keys(error.data).forEach(key => {
        if (key !== 'error' && key !== 'detail' && key !== 'non_field_errors') {
          const fieldMessages = Array.isArray(error.data[key]) 
            ? error.data[key] 
            : [error.data[key]]
          fieldErrors.push(`${key}: ${fieldMessages.join(', ')}`)
        }
      })
      
      if (fieldErrors.length > 0) {
        errorMessage = fieldErrors.join(' | ')
      } else if (error.data.error) {
        errorMessage = error.data.error
      } else if (error.data.detail) {
        errorMessage = error.data.detail
      } else if (error.data.non_field_errors) {
        errorMessage = Array.isArray(error.data.non_field_errors) 
          ? error.data.non_field_errors.join(', ')
          : error.data.non_field_errors
      } else {
        // Fallback: show the entire error object as string
        errorMessage = JSON.stringify(error.data)
      }
    } else if (error?.message) {
      errorMessage = error.message
    }
    
    snackbarMessage.value = errorMessage
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    saving.value = false
  }
}

const confirmDelete = (member: SupplierTeamMember) => {
  memberToDelete.value = member
  deleteDialog.value = true
}

const deleteMember = async () => {
  if (!memberToDelete.value) return

  deleting.value = true

  try {
    await teamApi.deleteTeamMember(memberToDelete.value.id!)
    snackbarMessage.value = 'عضو تیم با موفقیت حذف شد'
    snackbarColor.value = 'success'
    snackbar.value = true
    deleteDialog.value = false
    await loadMembers()
  } catch (error) {
    console.error('Error deleting team member:', error)
    snackbarMessage.value = 'خطا در حذف عضو تیم'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadMembers()
})
</script>

<style scoped>
.team-member-card {
  transition: transform 0.3s ease;
}

.team-member-card:hover {
  transform: translateY(-4px);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

