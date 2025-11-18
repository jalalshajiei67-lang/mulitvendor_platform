import { useApiFetch } from './useApiFetch'

export interface SupplierPortfolioItem {
  id?: number
  vendor_profile?: number
  vendor_name?: string
  title: string
  description: string
  image?: string | File
  project_date?: string
  client_name?: string
  category?: string
  sort_order?: number
  is_featured?: boolean
  created_at?: string
  updated_at?: string
}

export const useSupplierPortfolioApi = () => {
  const getPortfolioItems = async (): Promise<SupplierPortfolioItem[]> => {
    const response = await useApiFetch<{ results?: SupplierPortfolioItem[] } | SupplierPortfolioItem[]>(
      'users/supplier-portfolio/'
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const getPortfolioItem = async (id: number | string): Promise<SupplierPortfolioItem> => {
    return await useApiFetch<SupplierPortfolioItem>(`users/supplier-portfolio/${id}/`)
  }

  const createPortfolioItem = async (data: Partial<SupplierPortfolioItem>): Promise<SupplierPortfolioItem> => {
    const formData = new FormData()
    
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (key === 'image' && value instanceof File) {
          formData.append(key, value)
        } else if (typeof value === 'object') {
          formData.append(key, JSON.stringify(value))
        } else {
          formData.append(key, value.toString())
        }
      }
    })

    return await useApiFetch<SupplierPortfolioItem>('users/supplier-portfolio/', {
      method: 'POST',
      body: formData
    })
  }

  const updatePortfolioItem = async (
    id: number | string,
    data: Partial<SupplierPortfolioItem>
  ): Promise<SupplierPortfolioItem> => {
    const formData = new FormData()
    
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (key === 'image' && value instanceof File) {
          formData.append(key, value)
        } else if (typeof value === 'object') {
          formData.append(key, JSON.stringify(value))
        } else {
          formData.append(key, value.toString())
        }
      }
    })

    return await useApiFetch<SupplierPortfolioItem>(`users/supplier-portfolio/${id}/`, {
      method: 'PATCH',
      body: formData
    })
  }

  const deletePortfolioItem = async (id: number | string): Promise<void> => {
    await useApiFetch(`users/supplier-portfolio/${id}/`, {
      method: 'DELETE'
    })
  }

  return {
    getPortfolioItems,
    getPortfolioItem,
    createPortfolioItem,
    updatePortfolioItem,
    deletePortfolioItem
  }
}

