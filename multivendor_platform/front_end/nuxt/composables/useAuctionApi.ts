import { useApiFetch } from './useApiFetch'

export interface AuctionRequest {
  id: number
  buyer: number
  buyer_name: string
  product: number | null
  product_name: string | null
  subcategory: number | null
  subcategory_name: string | null
  status: string
  request_type: 'free' | 'verified'
  deposit_amount: number
  deposit_status: string
  auction_style: 'sealed' | 'live_reverse'
  start_time: string | null
  end_time: string | null
  description: string
  technical_specs: Record<string, any>
  photos: AuctionPhoto[]
  documents: AuctionDocument[]
  bids: Bid[]
  bid_count: number
  can_close_early: boolean
  time_remaining: number | null
  created_at: string
  updated_at: string
}

export interface AuctionPhoto {
  id: number
  image: string
  image_url: string
  uploaded_at: string
}

export interface AuctionDocument {
  id: number
  file: string
  file_url: string
  file_name: string
  uploaded_at: string
}

export interface Bid {
  id: number
  auction: number
  seller: number
  seller_name: string | null
  seller_id: number | null
  bidder_number: string | null
  price: number
  technical_compliance: Record<string, any>
  additional_notes: string | null
  is_winner: boolean
  rank: number | null
  created_at: string
  updated_at: string
}

export interface AuctionDepositPayment {
  id: number
  auction: number
  user: number
  amount: number
  status: string
  track_id: string
  payment_url?: string
}

export const useAuctionApi = () => {
  // Auction Requests
  const getAuctionRequests = async (): Promise<AuctionRequest[]> => {
    const response = await useApiFetch<{ results: AuctionRequest[] } | AuctionRequest[]>('auctions/auctions/')
    // Handle both paginated and non-paginated responses
    if (Array.isArray(response)) {
      return response
    }
    return response.results || []
  }

  const getAuctionRequest = async (id: number): Promise<AuctionRequest> => {
    return await useApiFetch<AuctionRequest>(`auctions/auctions/${id}/`)
  }

  const createAuctionRequest = async (data: any): Promise<AuctionRequest> => {
    return await useApiFetch<AuctionRequest>('auctions/auctions/', {
      method: 'POST',
      body: data
    })
  }

  const updateAuctionRequest = async (id: number, data: any): Promise<AuctionRequest> => {
    return await useApiFetch<AuctionRequest>(`auctions/auctions/${id}/`, {
      method: 'PATCH',
      body: data
    })
  }

  // Active Auctions (for sellers)
  const getActiveAuctions = async (subcategoryId?: number): Promise<AuctionRequest[]> => {
    const url = subcategoryId 
      ? `auctions/auction-list/?subcategory=${subcategoryId}`
      : 'auctions/auction-list/'
    const response = await useApiFetch<{ results: AuctionRequest[] } | AuctionRequest[]>(url)
    // Handle both paginated and non-paginated responses
    if (Array.isArray(response)) {
      return response
    }
    return response.results || []
  }

  // Bids
  const getBids = async (auctionId: number): Promise<Bid[]> => {
    const response = await useApiFetch<{ results: Bid[] } | Bid[]>(`auctions/bids/?auction=${auctionId}`)
    // Handle both paginated and non-paginated responses
    if (Array.isArray(response)) {
      return response
    }
    return response.results || []
  }

  const createBid = async (data: any): Promise<Bid> => {
    return await useApiFetch<Bid>('auctions/bids/', {
      method: 'POST',
      body: data
    })
  }

  // Deposit Payment
  const requestDepositPayment = async (auctionId: number): Promise<AuctionDepositPayment> => {
    return await useApiFetch<AuctionDepositPayment>('auctions/deposit/request/', {
      method: 'POST',
      body: { auction_id: auctionId }
    })
  }

  // Accept Bid / Close Early
  const acceptBid = async (auctionId: number, bidId: number): Promise<AuctionRequest> => {
    return await useApiFetch<AuctionRequest>(`auctions/auctions/${auctionId}/accept_bid/`, {
      method: 'POST',
      body: { bid_id: bidId }
    })
  }

  const closeEarly = async (auctionId: number): Promise<AuctionRequest> => {
    return await useApiFetch<AuctionRequest>(`auctions/auctions/${auctionId}/close_early/`, {
      method: 'POST'
    })
  }

  // File Uploads
  const uploadPhoto = async (file: File): Promise<AuctionPhoto> => {
    const formData = new FormData()
    formData.append('image', file)
    
    return await useApiFetch<AuctionPhoto>('auctions/photos/upload/', {
      method: 'POST',
      body: formData,
      headers: {} // Let browser set Content-Type for FormData
    })
  }

  const uploadDocument = async (file: File, fileName?: string): Promise<AuctionDocument> => {
    const formData = new FormData()
    formData.append('file', file)
    if (fileName) {
      formData.append('file_name', fileName)
    }
    
    return await useApiFetch<AuctionDocument>('auctions/documents/upload/', {
      method: 'POST',
      body: formData,
      headers: {} // Let browser set Content-Type for FormData
    })
  }

  // Notifications
  const getNotifications = async (): Promise<any[]> => {
    const response = await useApiFetch<{ results: any[] } | any[]>('auctions/notifications/')
    // Handle both paginated and non-paginated responses
    if (Array.isArray(response)) {
      return response
    }
    return response.results || []
  }

  const markNotificationRead = async (notificationId: number): Promise<void> => {
    await useApiFetch(`auctions/notifications/${notificationId}/mark_read/`, {
      method: 'POST'
    })
  }

  // Reports
  const getReport = async (auctionId: number): Promise<any> => {
    try {
      const response = await useApiFetch<{ results: any[] } | any[]>(`auctions/reports/?auction=${auctionId}`)
      // Handle both paginated and non-paginated responses
      let reports: any[] = []
      if (Array.isArray(response)) {
        reports = response
      } else if (response.results) {
        reports = response.results
      }
      // Return first report or null
      return reports.length > 0 ? reports[0] : null
    } catch (error) {
      // Report might not exist yet
      return null
    }
  }

  const createReport = async (auctionId: number, reportText: string): Promise<any> => {
    return await useApiFetch<any>('auctions/reports/', {
      method: 'POST',
      body: {
        auction: auctionId,
        report_text: reportText
      }
    })
  }

  const updateReport = async (reportId: number, reportText: string): Promise<any> => {
    return await useApiFetch<any>(`auctions/reports/${reportId}/`, {
      method: 'PATCH',
      body: {
        report_text: reportText
      }
    })
  }

  return {
    getAuctionRequests,
    getAuctionRequest,
    createAuctionRequest,
    updateAuctionRequest,
    getActiveAuctions,
    getBids,
    createBid,
    requestDepositPayment,
    acceptBid,
    closeEarly,
    uploadPhoto,
    uploadDocument,
    getNotifications,
    markNotificationRead,
    getReport,
    createReport,
    updateReport
  }
}

