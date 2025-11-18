import { useApiFetch } from './useApiFetch'

export interface SupplierContactMessage {
  id?: number
  vendor_profile: number
  vendor_name?: string
  sender_name: string
  sender_email: string
  sender_phone?: string
  subject: string
  message: string
  is_read?: boolean
  created_at?: string
  updated_at?: string
}

export const useSupplierContactApi = () => {
  const getContactMessages = async (): Promise<SupplierContactMessage[]> => {
    const response = await useApiFetch<{ results?: SupplierContactMessage[] } | SupplierContactMessage[]>(
      'users/supplier-contact/'
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const getContactMessage = async (id: number | string): Promise<SupplierContactMessage> => {
    return await useApiFetch<SupplierContactMessage>(`users/supplier-contact/${id}/`)
  }

  const createContactMessage = async (data: Omit<SupplierContactMessage, 'id' | 'vendor_name' | 'is_read' | 'created_at' | 'updated_at'>): Promise<SupplierContactMessage> => {
    return await useApiFetch<SupplierContactMessage>('users/supplier-contact/', {
      method: 'POST',
      body: data
    })
  }

  const markMessageRead = async (id: number | string): Promise<{ status: string }> => {
    return await useApiFetch<{ status: string }>(`users/supplier-contact/${id}/mark_read/`, {
      method: 'PATCH'
    })
  }

  const markMessageUnread = async (id: number | string): Promise<{ status: string }> => {
    return await useApiFetch<{ status: string }>(`users/supplier-contact/${id}/mark_unread/`, {
      method: 'PATCH'
    })
  }

  const deleteContactMessage = async (id: number | string): Promise<void> => {
    await useApiFetch(`users/supplier-contact/${id}/`, {
      method: 'DELETE'
    })
  }

  return {
    getContactMessages,
    getContactMessage,
    createContactMessage,
    markMessageRead,
    markMessageUnread,
    deleteContactMessage
  }
}

