import { useApiFetch } from './useApiFetch'

export interface RFQData {
  product_id: number
  category_id?: number
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

  return {
    createRFQ
  }
}

