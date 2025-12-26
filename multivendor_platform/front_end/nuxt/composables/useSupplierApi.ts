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
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:52',message:'getSuppliers entry',data:{},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
    // #endregion
    try {
      const response = await useApiFetch<{ results?: Supplier[] } | Supplier[]>(
        'users/suppliers/'
      )
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:56',message:'getSuppliers response received',data:{isArray:Array.isArray(response),hasResults:'results' in (response as any),responseType:typeof response},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
      // #endregion
      const result = Array.isArray(response) ? response : response.results || []
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:60',message:'getSuppliers exit',data:{resultLength:result.length},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
      // #endregion
      return result
    } catch (err: any) {
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:64',message:'getSuppliers error',data:{error:err?.message,statusCode:err?.statusCode||err?.status},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      throw err
    }
  }

  const getSupplier = async (id: number | string): Promise<Supplier> => {
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:70',message:'getSupplier entry',data:{id},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'E'})}).catch(()=>{});
    // #endregion
    try {
      const result = await useApiFetch<Supplier>(`users/suppliers/${id}/`)
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:74',message:'getSupplier success',data:{supplierId:result?.id,storeName:result?.store_name},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'E'})}).catch(()=>{});
      // #endregion
      return result
    } catch (err: any) {
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:78',message:'getSupplier error',data:{id,error:err?.message,statusCode:err?.statusCode||err?.status},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      throw err
    }
  }

  const getSupplierProducts = async (id: number | string, page: number = 1): Promise<{ results: any[], count: number, next: string | null, previous: string | null } | any[]> => {
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:84',message:'getSupplierProducts entry',data:{id,page},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'B'})}).catch(()=>{});
    // #endregion
    const endpoint = `users/suppliers/${id}/products/`
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:87',message:'getSupplierProducts endpoint constructed',data:{endpoint,page},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'B'})}).catch(()=>{});
    // #endregion
    try {
      const response = await useApiFetch<{ results?: any[], count?: number, next?: string | null, previous?: string | null } | any[]>(endpoint, {
        query: { page }
      })
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:90',message:'getSupplierProducts response received',data:{isArray:Array.isArray(response),hasResults:'results' in (response as any),responseKeys:response?Object.keys(response as any):[],responseType:typeof response},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
      // #endregion
      // Handle paginated response
      if (response && typeof response === 'object' && 'results' in response) {
        const paginatedResult = response as { results: any[], count: number, next: string | null, previous: string | null }
        // #region agent log
        fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:95',message:'getSupplierProducts returning paginated',data:{resultsCount:paginatedResult.results?.length,count:paginatedResult.count,hasNext:!!paginatedResult.next},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
        // #endregion
        return paginatedResult
      }
      // Fallback for non-paginated response (backward compatibility)
      const arrayResult = Array.isArray(response) ? response : []
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:101',message:'getSupplierProducts returning array',data:{arrayLength:arrayResult.length},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
      // #endregion
      return arrayResult
    } catch (err: any) {
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:104',message:'getSupplierProducts error',data:{id,page,error:err?.message,statusCode:err?.statusCode||err?.status},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      throw err
    }
  }

  const getSupplierComments = async (id: number | string): Promise<SupplierComment[]> => {
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:110',message:'getSupplierComments entry',data:{id},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
    // #endregion
    try {
      const response = await useApiFetch<{ results?: SupplierComment[] } | SupplierComment[]>(
        `users/suppliers/${id}/comments/`
      )
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:115',message:'getSupplierComments response received',data:{isArray:Array.isArray(response),hasResults:'results' in (response as any)},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
      // #endregion
      const result = Array.isArray(response) ? response : response.results || []
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:119',message:'getSupplierComments exit',data:{resultLength:result.length},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
      // #endregion
      return result
    } catch (err: any) {
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useSupplierApi.ts:122',message:'getSupplierComments error',data:{id,error:err?.message,statusCode:err?.statusCode||err?.status},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      throw err
    }
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

