import { useRuntimeConfig } from '#imports'
import { defineEventHandler } from 'h3'

const buildUrlEntry = (params: {
  loc: string
  changefreq?: string
  priority?: number
  lastmod?: string
}) => {
  const parts = [
    `<loc>${params.loc}</loc>`,
    params.lastmod ? `<lastmod>${params.lastmod}</lastmod>` : '',
    params.changefreq ? `<changefreq>${params.changefreq}</changefreq>` : '',
    params.priority !== undefined ? `<priority>${params.priority.toFixed(1)}</priority>` : ''
  ]

  return `<url>${parts.filter(Boolean).join('')}</url>`
}

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase.replace(/\/$/, '')
  const siteUrl = config.public.siteUrl.replace(/\/$/, '')

  const fetchSafe = async (url: string) => {
    try {
      return await $fetch(url)
    } catch (error) {
      console.error('Error fetching sitemap data:', error)
      return null
    }
  }

  const [labelResponse, comboResponse] = await Promise.all([
    fetchSafe(`${apiBase}/labels/?page_size=1000&is_seo_page=true`),
    fetchSafe(`${apiBase}/label-combos/?page_size=1000&is_indexable=true`)
  ])

  const labelEntries = Array.isArray(labelResponse)
    ? labelResponse
    : labelResponse?.results ?? []

  const comboEntries = Array.isArray(comboResponse)
    ? comboResponse
    : comboResponse?.results ?? []

  const baseEntries = [
    buildUrlEntry({
      loc: `${siteUrl}/`,
      changefreq: 'daily',
      priority: 1
    }),
    buildUrlEntry({
      loc: `${siteUrl}/products/`,
      changefreq: 'daily',
      priority: 0.9
    }),
    buildUrlEntry({
      loc: `${siteUrl}/machinery/`,
      changefreq: 'weekly',
      priority: 0.7
    })
  ]

  const labelEntriesXml = labelEntries
    .filter((label: Record<string, any>) => label.slug)
    .map((label: Record<string, any>) =>
      buildUrlEntry({
        loc: `${siteUrl}/machinery/${label.slug}/`,
        changefreq: 'weekly',
        priority: 0.7,
        lastmod: label.updated_at
      })
    )

  const comboEntriesXml = comboEntries
    .filter((combo: Record<string, any>) => combo.slug)
    .map((combo: Record<string, any>) =>
      buildUrlEntry({
        loc: `${siteUrl}/machinery/${combo.slug}/`,
        changefreq: 'weekly',
        priority: 0.6,
        lastmod: combo.updated_at
      })
    )

  const urlset = [...baseEntries, ...labelEntriesXml, ...comboEntriesXml].join('')
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urlset}</urlset>`

  event.node.res.setHeader('Content-Type', 'application/xml')
  return xml
})

