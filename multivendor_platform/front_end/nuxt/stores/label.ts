import { defineStore } from 'pinia'
import { ref } from 'vue'

import { useApiFetch } from '~/composables/useApiFetch'

type LabelGroup = {
  id: number
  name: string
  slug: string
  description?: string
  labels: Record<string, any>[]
}

export const useLabelStore = defineStore('labels', () => {
  const labelGroups = ref<LabelGroup[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentSubcategoryId = ref<number | null>(null)

  const buildLabelGroupsUrl = (subcategoryId: number | null) => {
    return subcategoryId ? `label-groups/?subcategory=${subcategoryId}` : 'label-groups/'
  }

  const fetchLabelGroups = async (subcategoryId: number | null = null, force = false) => {
    const matchesCurrent = currentSubcategoryId.value === subcategoryId
    if (!force && matchesCurrent && labelGroups.value.length) {
      return labelGroups.value
    }
    if (loading.value) {
      return labelGroups.value
    }

    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<LabelGroup[] | { results?: LabelGroup[] }>(
        buildLabelGroupsUrl(subcategoryId)
      )
      const groups = Array.isArray(response) ? response : response?.results ?? []
      labelGroups.value = groups
      currentSubcategoryId.value = subcategoryId
      return labelGroups.value
    } catch (err: any) {
      error.value = err?.data?.detail ?? err?.message ?? 'خطا در دریافت فیلتر‌ها'
      labelGroups.value = []
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchLabelGroupsForSubcategory = (subcategoryId: number | null, force = false) => {
    return fetchLabelGroups(subcategoryId, force)
  }

  const reset = () => {
    labelGroups.value = []
    error.value = null
    currentSubcategoryId.value = null
  }

  return {
    labelGroups,
    loading,
    error,
    currentSubcategoryId,
    fetchLabelGroups,
    fetchLabelGroupsForSubcategory,
    reset
  }
})

