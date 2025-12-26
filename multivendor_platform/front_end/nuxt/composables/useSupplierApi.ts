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

  const getSupplierProducts = async (id: number | string, page: number = 1): Promise<{ results: any[], count: number, next: string | null, previous: string | null } | any[]> => {
    const response = await useApiFetch<{ results?: any[], count?: number, next?: string | null, previous?: string | null } | any[]>(
      `users/suppliers/${id}/products/?page=${page}`
    )
    // Handle paginated response
    if (response && typeof response === 'object' && 'results' in response) {
      return response as { results: any[], count: number, next: string | null, previous: string | null }
    }
    // Fallback for non-paginated response (backward compatibility)
    return Array.isArray(response) ? response : []
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

  const updateSupplierProfile = async (data: Partial<Supplier & { banner_image?: File | string }>): Promise<any> => {
    // Check if there's a file upload (banner_image)
    const bannerImage = data.banner_image
    // Check if banner_image is a File object
    const hasFile = bannerImage && typeof bannerImage === 'object' && 'size' in bannerImage && 'type' in bannerImage
    
    console.log('updateSupplierProfile called with:', { data, hasFile })
    
    if (hasFile) {
      // Use FormData for file uploads
      const formData = new FormData()
      
      Object.entries(data).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          if (key === 'banner_image' && value instanceof File) {
            formData.append(key, value as File)
          } else if (typeof value === 'object' && !(value instanceof File)) {
            // Stringify objects (certifications, awards, social_media)
            formData.append(key, JSON.stringify(value))
          } else {
            formData.append(key, value.toString())
          }
        }
      })
      
      // Log FormData contents for debugging
      console.log('Sending FormData with fields:')
      for (const [key, value] of formData.entries()) {
        if (value instanceof File) {
          console.log(`  ${key}: [File] ${value.name} (${value.size} bytes)`)
        } else {
          console.log(`  ${key}:`, value)
        }
      }
      
      const response = await useApiFetch<any>('users/profile/update/', {
        method: 'PATCH',
        body: formData
      })
      console.log('FormData response:', response)
      return response
    } else {
      // Use JSON for regular updates
      console.log('Sending JSON data:', data)
      const response = await useApiFetch<any>('users/profile/update/', {
        method: 'PATCH',
        body: data
      })
      console.log('JSON response:', response)
      return response
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

