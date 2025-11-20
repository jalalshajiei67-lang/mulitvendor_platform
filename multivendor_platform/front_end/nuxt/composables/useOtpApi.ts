/**
 * OTP API composable
 * Handles OTP request and verification
 */

export type OtpPurpose = 'login' | 'password_reset' | 'phone_verification' | 'transaction'

export interface OtpRequestData {
  phone?: string
  username?: string
  purpose: OtpPurpose
}

export interface OtpVerifyData {
  phone?: string
  username?: string
  code: string
  purpose: OtpPurpose
}

export interface OtpRequestResponse {
  success: boolean
  message: string
  otp_code?: string  // Only in local/dev mode
}

export interface OtpVerifyResponse {
  success: boolean
  message: string
  token?: string  // For login purpose
  user?: any  // For login purpose
}

export const useOtpApi = () => {
  return {
    /**
     * Request OTP
     */
    async requestOtp(data: OtpRequestData) {
      return useApiFetch<OtpRequestResponse>('auth/otp/request/', {
        method: 'POST',
        body: data
      })
    },

    /**
     * Verify OTP
     */
    async verifyOtp(data: OtpVerifyData) {
      return useApiFetch<OtpVerifyResponse>('auth/otp/verify/', {
        method: 'POST',
        body: data
      })
    }
  }
}

