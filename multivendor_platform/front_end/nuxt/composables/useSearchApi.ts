type SearchResultProduct = Record<string, any>
type SearchResultBlog = Record<string, any>

export type SearchResults = {
  products: SearchResultProduct[]
  blogs: SearchResultBlog[]
  total: number
}

export const useSearchApi = () => {
  const globalSearch = async (query: string, limit = 10): Promise<SearchResults> => {
    return useApiFetch<SearchResults>('search/', {
      query: { q: query, limit }
    })
  }

  return {
    globalSearch
  }
}

