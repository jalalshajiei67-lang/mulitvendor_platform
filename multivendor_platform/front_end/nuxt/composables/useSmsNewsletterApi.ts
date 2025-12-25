/**
 * SMS Newsletter API composable
 * Handles SMS newsletter for sellers API calls
 */

export const useSmsNewsletterApi = () => {
  return {
    /**
     * Get sellers with optional filtering by working fields
     * @param workingFieldIds - Array of subcategory IDs to filter by
     */
    async getSellers(workingFieldIds?: number[]) {
      const params: Record<string, any> = {}
      
      if (workingFieldIds && workingFieldIds.length > 0) {
        // Kavenegar API expects multiple values as array
        params.working_fields = workingFieldIds
      }
      
      return useApiFetch<{
        results: Array<{
          id: number
          name: string
          company_name: string | null
          mobile_number: string
          phone: string | null
          working_fields: number[]
          working_fields_display: string
        }>
        count: number
      }>('sms-newsletter/sellers/', {
        params
      })
    },

    /**
     * Get all subcategories for filter dropdown
     */
    async getSubcategories() {
      return useApiFetch<{
        results: Array<{
          id: number
          name: string
          slug: string
        }>
      }>('subcategories/', {
        params: { is_active: true }
      })
    },

    /**
     * Send SMS to selected sellers
     * @param sellerIds - Array of seller IDs to send SMS to
     * @param workingFieldIds - Optional array of working field IDs to include in SMS
     */
    async sendSms(sellerIds: number[], workingFieldIds?: number[]) {
      return useApiFetch<{
        total: number
        success_count: number
        failure_count: number
        results: Array<{
          seller_id: number
          seller_name: string
          mobile_number: string
          success: boolean
          message: string
        }>
      }>('sms-newsletter/send/', {
        method: 'POST',
        body: {
          seller_ids: sellerIds,
          working_field_ids: workingFieldIds || []
        }
      })
    }
  }
}

