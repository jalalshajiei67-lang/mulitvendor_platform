export interface AboutPage {
  id: number
  title_fa: string
  content_fa: string
  title_en?: string
  content_en?: string
  meta_title_fa?: string
  meta_description_fa?: string
  meta_keywords_fa?: string
  meta_title_en?: string
  meta_description_en?: string
  meta_keywords_en?: string
  created_at: string
  updated_at: string
}

export interface ContactPage {
  id: number
  title_fa: string
  content_fa: string
  address_fa?: string
  phone?: string
  email?: string
  working_hours_fa?: string
  title_en?: string
  content_en?: string
  address_en?: string
  working_hours_en?: string
  meta_title_fa?: string
  meta_description_fa?: string
  meta_keywords_fa?: string
  meta_title_en?: string
  meta_description_en?: string
  meta_keywords_en?: string
  created_at: string
  updated_at: string
}

export const usePagesApi = () => {
  return {
    // Get About Us page
    async getAboutPage(): Promise<AboutPage> {
      return useApiFetch<AboutPage>('pages/about/current/')
    },

    // Get Contact Us page
    async getContactPage(): Promise<ContactPage> {
      return useApiFetch<ContactPage>('pages/contact/current/')
    }
  }
}

