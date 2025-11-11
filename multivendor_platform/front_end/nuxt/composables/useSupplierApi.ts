import { useApiFetch } from './useApiFetch'

export interface Supplier {
  id: number
  store_name: string
  description?: string
  about?: string
  work_resume?: string
  successful_projects?: string
  history?: string
  address?: string
  logo?: string
  contact_email?: string
  contact_phone?: string
  website?: string
  rating_average?: number
  product_count?: number
  created_at?: string
  user?: {
    id: number
    username: string
    email?: string
    first_name?: string
    last_name?: string
  }
}

export interface SupplierComment {
  id: number
  user_username: string
  rating: number
  title?: string
  comment: string
  supplier_reply?: string
  created_at: string
}

export const useSupplierApi = () => {
  const getSuppliers = async (): Promise<Supplier[]> => {
    const response = await useApiFetch<{ results?: Supplier[] } | Supplier[]>(
      'users/suppliers/'
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const getSupplier = async (id: number | string): Promise<Supplier> => {
    return await useApiFetch<Supplier>(`users/suppliers/${id}/`)
  }

  const getSupplierProducts = async (id: number | string): Promise<any[]> => {
    const response = await useApiFetch<{ results?: any[] } | any[]>(
      `users/suppliers/${id}/products/`
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const getSupplierComments = async (id: number | string): Promise<SupplierComment[]> => {
    const response = await useApiFetch<{ results?: SupplierComment[] } | SupplierComment[]>(
      `users/suppliers/${id}/comments/`
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const createSupplierComment = async (
    supplierId: number | string,
    data: {
      rating: number
      title?: string
      comment: string
    }
  ): Promise<SupplierComment> => {
    return await useApiFetch<SupplierComment>('users/supplier-comments/', {
      method: 'POST',
      body: {
        supplier: supplierId,
        ...data
      }
    })
  }

  return {
    getSuppliers,
    getSupplier,
    getSupplierProducts,
    getSupplierComments,
    createSupplierComment
  }
}

