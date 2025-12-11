import { useApiFetch } from './useApiFetch'

export interface RFQData {
  product_id: number
  category_id?: number
  is_free?: boolean
  first_name: string
  last_name: string
  company_name: string
  phone_number: string
  unique_needs: string
  images?: File[]
}

export const useRfqApi = () => {
  const createRFQ = async (formData: FormData): Promise<any> => {
    return await useApiFetch('orders/rfq/create/', {
      method: 'POST',
      body: formData
    })
  }

  const getVendorPool = async (): Promise<any> =>
    await useApiFetch('orders/vendor/rfq/', { method: 'GET' })

  const getVendorMy = async (): Promise<any> =>
    await useApiFetch('orders/vendor/rfq/my/', { method: 'GET' })

  const revealRFQContact = async (rfqId: number): Promise<any> => {
    return await useApiFetch(`orders/vendor/rfq/${rfqId}/reveal/`, {
      method: 'POST'
    })
  }

  return {
    createRFQ,
    getVendorPool,
    getVendorMy,
    revealRFQContact
  }
}

