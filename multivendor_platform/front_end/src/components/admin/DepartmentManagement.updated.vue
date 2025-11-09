<template>
  <div dir="rtl">
    <!-- Summary Cards -->
    <v-row class="mb-4">
      <v-col cols="12" sm="6" md="3">
        <v-card class="summary-card" elevation="0" variant="outlined">
          <v-card-text class="text-center pa-4">
            <div class="text-h5 font-weight-bold mb-1">{{ departmentStore.departments.length }}</div>
            <div class="text-caption text-grey">کل دپارتمان‌ها</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="summary-card" elevation="0" variant="outlined">
          <v-card-text class="text-center pa-4">
            <div class="text-h5 font-weight-bold text-success mb-1">
              {{ departmentStore.activeDepartments.length }}
            </div>
            <div class="text-caption text-grey">فعال</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="summary-card" elevation="0" variant="outlined">
          <v-card-text class="text-center pa-4">
            <div class="text-h5 font-weight-bold text-warning mb-1">
              {{ inactiveDepartmentsCount }}
            </div>
            <div class="text-caption text-grey">غیرفعال</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Loading State -->
    <v-row v-if="departmentStore.isLoading">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <div class="mt-2">{{ $t('loading') }}</div>
      </v-col>
    </v-row>

    <!-- Error State -->
    <v-row v-else-if="departmentStore.hasError">
      <v-col cols="12">
        <v-alert type="error" variant="tonal">
          {{ departmentStore.error }}
        </v-alert>
      </v-col>
    </v-row>

    <!-- Departments List -->
    <v-row v-else>
      <v-col cols="12">
        <v-card elevation="0" variant="outlined">
          <v-card-title class="d-flex justify-space-between align-center">
            <span>مدیریت دپارتمان‌ها</span>
            <v-btn color="primary" @click="openCreateDialog">
              <v-icon start>mdi-plus</v-icon>
              افزودن دپارتمان
            </v-btn>
          </v-card-title>
          
          <v-card-text>
            <v-data-table
              :items="departmentStore.departments"
              :headers="headers"
              :loading="departmentStore.isLoading"
              :search="filters.search"
            >
              <template #item.is_active="{ item }">
                <v-chip :color="item.is_active ? 'success' : 'warning'" size="small">
                  {{ item.is_active ? 'فعال' : 'غیرفعال' }}
                </v-chip>
              </template>
              
              <template #item.actions="{ item }">
                <v-btn icon size="small" @click="editDepartment(item)" color="primary">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon size="small" @click="deleteDepartment(item)" color="error">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useDepartmentStore } from '@/stores';

const departmentStore = useDepartmentStore();

const headers = [
  { title: 'نام', key: 'name' },
  { title: 'اسلاگ', key: 'slug' },
  { title: 'وضعیت', key: 'is_active' },
  { title: 'عملیات', key: 'actions', sortable: false }
];

const filters = {
  search: ''
};

const inactiveDepartmentsCount = computed(() => 
  departmentStore.departments.filter(d => !d.is_active).length
);

const loadDepartments = async () => {
  await departmentStore.fetchDepartments();
};

const openCreateDialog = () => {
  // Implementation for create dialog
  console.log('Open create dialog');
};

const editDepartment = (department) => {
  // Implementation for edit dialog
  console.log('Edit department:', department);
};

const deleteDepartment = async (department) => {
  if (confirm(`آیا مطمئن هستید که می‌خواهید دپارتمان "${department.name}" را حذف کنید؟`)) {
    try {
      await departmentStore.deleteDepartment(department.id);
      await loadDepartments();
    } catch (error) {
      console.error('Error deleting department:', error);
    }
  }
};

onMounted(() => {
  loadDepartments();
});
</script>

<style scoped>
.summary-card {
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}
.summary-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
</style>
