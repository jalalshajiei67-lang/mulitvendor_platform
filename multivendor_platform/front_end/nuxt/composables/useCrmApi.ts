import { useApiFetch } from './useApiFetch'

export interface SellerContact {
  id: number
  seller: number
  first_name: string
  last_name: string
  company_name?: string | null
  phone: string
  email?: string | null
  address?: string | null
  notes?: string | null
  source_order?: number | null
  notes_count?: number
  tasks_count?: number
  created_at: string
  updated_at: string
}

export interface ContactNote {
  id: number
  contact: number
  contact_name?: string
  seller: number
  content: string
  created_at: string
  updated_at: string
}

export interface ContactTask {
  id: number
  contact?: number | null
  contact_name?: string | null
  seller: number
  title: string
  description?: string | null
  due_date: string
  priority: 'low' | 'medium' | 'high'
  priority_display?: string
  status: 'pending' | 'completed' | 'cancelled'
  status_display?: string
  is_overdue?: boolean
  created_at: string
  updated_at: string
}

export const useCrmApi = () => {
  // Contacts
  const getContacts = async (search?: string): Promise<SellerContact[]> => {
    const params = search ? { search } : {}
    const response = await useApiFetch<{ results?: SellerContact[] } | SellerContact[]>(
      'auth/crm/contacts/',
      { query: params }
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const getContact = async (id: number): Promise<SellerContact> => {
    return await useApiFetch<SellerContact>(`auth/crm/contacts/${id}/`)
  }

  const createContact = async (data: Partial<SellerContact>): Promise<SellerContact> => {
    return await useApiFetch<SellerContact>('auth/crm/contacts/', {
      method: 'POST',
      body: data
    })
  }

  const updateContact = async (id: number, data: Partial<SellerContact>): Promise<SellerContact> => {
    return await useApiFetch<SellerContact>(`auth/crm/contacts/${id}/`, {
      method: 'PUT',
      body: data
    })
  }

  const deleteContact = async (id: number): Promise<void> => {
    await useApiFetch(`auth/crm/contacts/${id}/`, {
      method: 'DELETE'
    })
  }

  const getContactNotes = async (contactId: number): Promise<ContactNote[]> => {
    const response = await useApiFetch<{ results?: ContactNote[] } | ContactNote[]>(
      'auth/crm/notes/',
      { query: { contact: contactId } }
    )
    return Array.isArray(response) ? response : response.results || []
  }

  // Notes
  const getNotes = async (contactId?: number): Promise<ContactNote[]> => {
    const params = contactId ? { contact: contactId } : {}
    const response = await useApiFetch<{ results?: ContactNote[] } | ContactNote[]>(
      'auth/crm/notes/',
      { query: params }
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const getNote = async (id: number): Promise<ContactNote> => {
    return await useApiFetch<ContactNote>(`auth/crm/notes/${id}/`)
  }

  const createNote = async (contactId: number, content: string): Promise<ContactNote> => {
    return await useApiFetch<ContactNote>('auth/crm/notes/', {
      method: 'POST',
      body: {
        contact: contactId,
        content
      }
    })
  }

  const updateNote = async (id: number, content: string): Promise<ContactNote> => {
    return await useApiFetch<ContactNote>(`auth/crm/notes/${id}/`, {
      method: 'PUT',
      body: { content }
    })
  }

  const deleteNote = async (id: number): Promise<void> => {
    await useApiFetch(`auth/crm/notes/${id}/`, {
      method: 'DELETE'
    })
  }

  // Tasks
  const getTasks = async (params?: {
    status?: 'pending' | 'completed' | 'cancelled'
    contact?: number
    priority?: 'low' | 'medium' | 'high'
  }): Promise<ContactTask[]> => {
    const response = await useApiFetch<{ results?: ContactTask[] } | ContactTask[]>(
      'auth/crm/tasks/',
      { query: params }
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const getTask = async (id: number): Promise<ContactTask> => {
    return await useApiFetch<ContactTask>(`auth/crm/tasks/${id}/`)
  }

  const createTask = async (data: Partial<ContactTask>): Promise<ContactTask> => {
    return await useApiFetch<ContactTask>('auth/crm/tasks/', {
      method: 'POST',
      body: data
    })
  }

  const updateTask = async (id: number, data: Partial<ContactTask>): Promise<ContactTask> => {
    return await useApiFetch<ContactTask>(`auth/crm/tasks/${id}/`, {
      method: 'PUT',
      body: data
    })
  }

  const deleteTask = async (id: number): Promise<void> => {
    await useApiFetch(`auth/crm/tasks/${id}/`, {
      method: 'DELETE'
    })
  }

  const completeTask = async (id: number): Promise<ContactTask> => {
    return await useApiFetch<ContactTask>(`auth/crm/tasks/${id}/complete/`, {
      method: 'PATCH'
    })
  }

  const cancelTask = async (id: number): Promise<ContactTask> => {
    return await useApiFetch<ContactTask>(`auth/crm/tasks/${id}/cancel/`, {
      method: 'PATCH'
    })
  }

  return {
    // Contacts
    getContacts,
    getContact,
    createContact,
    updateContact,
    deleteContact,
    getContactNotes,
    // Notes
    getNotes,
    getNote,
    createNote,
    updateNote,
    deleteNote,
    // Tasks
    getTasks,
    getTask,
    createTask,
    updateTask,
    deleteTask,
    completeTask,
    cancelTask
  }
}

