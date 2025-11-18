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
  // Mini website branding fields
  banner_image?: string
  brand_color_primary?: string
  brand_color_secondary?: string
  slogan?: string
  year_established?: number
  employee_count?: number
  certifications?: any[]
  awards?: any[]
  social_media?: any
  video_url?: string
  meta_title?: string
  meta_description?: string
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

  const getSupplierPortfolio = async (id: number | string): Promise<any[]> => {
    const response = await useApiFetch<{ results?: any[] } | any[]>(
      `users/suppliers/${id}/portfolio/`
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const getSupplierTeam = async (id: number | string): Promise<any[]> => {
    const response = await useApiFetch<{ results?: any[] } | any[]>(
      `users/suppliers/${id}/team/`
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const updateSupplierProfile = async (data: Partial<Supplier & { banner_image?: File | string }>): Promise<Supplier> => {
    // Check if there's a file upload (banner_image)
    const bannerImage = data.banner_image
    // Check if banner_image is a File object
    const hasFile = bannerImage && typeof bannerImage === 'object' && 'size' in bannerImage && 'type' in bannerImage
    
    if (hasFile) {
      // Use FormData for file uploads
      const formData = new FormData()
      
      Object.entries(data).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          if (key === 'banner_image' && value instanceof File) {
            formData.append(key, value as File)
          } else if (typeof value === 'object' && !(value instanceof File)) {
            formData.append(key, JSON.stringify(value))
          } else {
            formData.append(key, value.toString())
          }
        }
      })
      
      return await useApiFetch<Supplier>('users/profile/update/', {
        method: 'PATCH',
        body: formData
      })
    } else {
      // Use JSON for regular updates
      return await useApiFetch<Supplier>('users/profile/update/', {
        method: 'PATCH',
        body: data
      })
    }
  }

  return {
    getSuppliers,
    getSupplier,
    getSupplierProducts,
    getSupplierComments,
    createSupplierComment,
    getSupplierPortfolio,
    getSupplierTeam,
    updateSupplierProfile
  }
}

