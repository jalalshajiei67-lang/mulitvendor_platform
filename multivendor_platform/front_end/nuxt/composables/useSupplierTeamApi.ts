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
    
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (key === 'photo' && value instanceof File) {
          formData.append(key, value)
        } else if (typeof value === 'object') {
          formData.append(key, JSON.stringify(value))
        } else {
          formData.append(key, value.toString())
        }
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
    
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (key === 'photo' && value instanceof File) {
          formData.append(key, value)
        } else if (typeof value === 'object') {
          formData.append(key, JSON.stringify(value))
        } else {
          formData.append(key, value.toString())
        }
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

