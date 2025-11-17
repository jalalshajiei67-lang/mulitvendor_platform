type LabelSchemaParams = {
  label: Record<string, any>
  products: Record<string, any>[]
  canonical: string
  siteUrl: string
}

const safeUrl = (siteUrl: string, path: string) => {
  const base = siteUrl.replace(/\/$/, '')
  if (!path) {
    return base
  }
  const normalized = path.startsWith('/') ? path : `/${path}`
  return `${base}${normalized}`
}

export const createLabelPageSchema = ({
  label,
  products,
  canonical,
  siteUrl
}: LabelSchemaParams) => {
  const canonicalUrl = safeUrl(siteUrl, canonical)
  const productList = (products ?? []).slice(0, 10).map((product, index) => {
    const productSlug = product.slug ?? product.id
    return {
      '@type': 'ListItem',
      position: index + 1,
      url: safeUrl(siteUrl, `/products/${productSlug}`)
    }
  })

  const breadcrumbs = [
    {
      '@type': 'ListItem',
      position: 1,
      name: 'خانه',
      item: safeUrl(siteUrl, '/')
    },
    {
      '@type': 'ListItem',
      position: 2,
      name: 'محصولات',
      item: safeUrl(siteUrl, '/products')
    },
    {
      '@type': 'ListItem',
      position: 3,
      name: label.name ?? 'صفحه برچسب',
      item: canonicalUrl
    }
  ]

  return [
    {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name: label.name ?? 'مجموعه محصولات',
      description: label.seo_description ?? label.description ?? '',
      url: canonicalUrl,
      mainEntity: {
        '@type': 'ItemList',
        numberOfItems: productList.length,
        itemListElement: productList
      }
    },
    {
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      itemListElement: breadcrumbs
    }
  ]
}

