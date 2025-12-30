import { useApiFetch } from './useApiFetch'

export interface AuctionCreateData {
  title: string
  description: string
  category: number
  starting_price: string | number
  reserve_price?: string | number
  deadline: string  // ISO datetime string
  minimum_decrement: string | number
}

export interface BidData {
  amount: string | number
}

export interface AuctionAwardData {
  bid_id: number
}

export const useAuctionApi = () => {
  const apiFetch = useApiFetch

  const createAuction = async (data: AuctionCreateData): Promise<any> => {
    return await apiFetch('auctions/auctions/', {
      method: 'POST',
      body: data
    })
  }

  const getAuctions = async (params?: any): Promise<any> => {
    return await apiFetch('auctions/auctions/', {
      method: 'GET',
      params
    })
  }

  const getAuctionDetail = async (id: number): Promise<any> => {
    return await apiFetch(`auctions/auctions/${id}/`, {
      method: 'GET'
    })
  }

  const placeBid = async (id: number, amount: string | number): Promise<any> => {
    return await apiFetch(`auctions/auctions/${id}/place-bid/`, {
      method: 'POST',
      body: { amount }
    })
  }

  const getMyStatus = async (id: number): Promise<any> => {
    return await apiFetch(`auctions/auctions/${id}/my-status/`, {
      method: 'GET'
    })
  }

  const getBids = async (id: number): Promise<any> => {
    return await apiFetch(`auctions/auctions/${id}/bids/`, {
      method: 'GET'
    })
  }

  const awardAuction = async (id: number, bidId: number): Promise<any> => {
    return await apiFetch(`auctions/auctions/${id}/award/`, {
      method: 'POST',
      body: { bid_id: bidId }
    })
  }

  const cancelAuction = async (id: number): Promise<any> => {
    return await apiFetch(`auctions/auctions/${id}/cancel/`, {
      method: 'POST'
    })
  }

  return {
    createAuction,
    getAuctions,
    getAuctionDetail,
    placeBid,
    getMyStatus,
    getBids,
    awardAuction,
    cancelAuction
  }
}

