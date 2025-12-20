import { useApiFetch } from './useApiFetch'

export interface SupplierTeamMember {
  id?: number
  vendor_profile?: number
  vendor_name?: string
  name: string
  position: string
  photo?: string | File
  bio?: string
  sort_order?: number
  created_at?: string
  updated_at?: string
}

export const useSupplierTeamApi = () => {
  const getTeamMembers = async (): Promise<SupplierTeamMember[]> => {
    const response = await useApiFetch<{ results?: SupplierTeamMember[] } | SupplierTeamMember[]>(
      'users/supplier-team/'
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const getTeamMember = async (id: number | string): Promise<SupplierTeamMember> => {
    return await useApiFetch<SupplierTeamMember>(`users/supplier-team/${id}/`)
  }

  const createTeamMember = async (data: Partial<SupplierTeamMember>): Promise<SupplierTeamMember> => {
    const formData = new FormData()
    
    // Required fields that must always be included
    const requiredFields = ['name', 'position']
    
    Object.entries(data).forEach(([key, value]) => {
      // Skip undefined and null values (except for required fields)
      if (value === undefined || value === null) {
        if (requiredFields.includes(key)) {
          // Include required fields even if null/undefined (will cause validation error, but that's expected)
          formData.append(key, '')
        }
        return
      }
      
      // Handle File objects (for photo)
      if (key === 'photo' && value instanceof File) {
        formData.append(key, value)
      } 
      // Handle empty strings for optional fields - skip them
      else if (key === 'bio' && value === '') {
        // Skip empty bio - let backend use default (null)
        return
      }
      // Handle numbers (sort_order) - always include, even if 0
      else if (key === 'sort_order' && typeof value === 'number') {
        formData.append(key, value.toString())
      }
      // Handle strings - include all strings (required fields must not be empty, but include them anyway)
      else if (typeof value === 'string') {
        formData.append(key, value)
      }
      // Handle other objects (shouldn't happen, but just in case)
      else if (typeof value === 'object') {
        formData.append(key, JSON.stringify(value))
      }
      // Handle other primitives
      else {
        formData.append(key, value.toString())
      }
    })

    return await useApiFetch<SupplierTeamMember>('users/supplier-team/', {
      method: 'POST',
      body: formData
    })
  }

  const updateTeamMember = async (
    id: number | string,
    data: Partial<SupplierTeamMember>
  ): Promise<SupplierTeamMember> => {
    const formData = new FormData()
    
    // Required fields that must always be included
    const requiredFields = ['name', 'position']
    
    Object.entries(data).forEach(([key, value]) => {
      // Skip undefined and null values (except for required fields)
      if (value === undefined || value === null) {
        if (requiredFields.includes(key)) {
          // Include required fields even if null/undefined (will cause validation error, but that's expected)
          formData.append(key, '')
        }
        return
      }
      
      // Handle File objects (for photo)
      if (key === 'photo' && value instanceof File) {
        formData.append(key, value)
      } 
      // Handle empty strings for optional fields - skip them
      else if (key === 'bio' && value === '') {
        // Skip empty bio - let backend use default (null)
        return
      }
      // Handle numbers (sort_order) - always include, even if 0
      else if (key === 'sort_order' && typeof value === 'number') {
        formData.append(key, value.toString())
      }
      // Handle strings - include all strings (required fields must not be empty, but include them anyway)
      else if (typeof value === 'string') {
        formData.append(key, value)
      }
      // Handle other objects (shouldn't happen, but just in case)
      else if (typeof value === 'object') {
        formData.append(key, JSON.stringify(value))
      }
      // Handle other primitives
      else {
        formData.append(key, value.toString())
      }
    })

    return await useApiFetch<SupplierTeamMember>(`users/supplier-team/${id}/`, {
      method: 'PATCH',
      body: formData
    })
  }

  const deleteTeamMember = async (id: number | string): Promise<void> => {
    await useApiFetch(`users/supplier-team/${id}/`, {
      method: 'DELETE'
    })
  }

  return {
    getTeamMembers,
    getTeamMember,
    createTeamMember,
    updateTeamMember,
    deleteTeamMember
  }
}

