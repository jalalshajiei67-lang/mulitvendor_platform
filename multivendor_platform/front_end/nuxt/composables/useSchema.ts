/**
 * Schema validation and generation utilities for JSON-LD
 */

interface SchemaValidationResult {
  valid: boolean
  errors: string[]
}

interface SchemaObject {
  '@context'?: string
  '@type'?: string
  [key: string]: any
}

/**
 * Validates JSON-LD schema structure
 */
function validateSchema(schema: SchemaObject): SchemaValidationResult {
  const errors: string[] = []

  if (!schema || typeof schema !== 'object') {
    return { valid: false, errors: ['Schema must be an object'] }
  }

  // Check for @context (required for JSON-LD)
  if (!schema['@context']) {
    errors.push('Missing @context property')
  } else if (typeof schema['@context'] !== 'string') {
    errors.push('@context must be a string')
  }

  // Check for @type (required for most schemas)
  if (!schema['@type']) {
    errors.push('Missing @type property')
  } else if (typeof schema['@type'] !== 'string') {
    errors.push('@type must be a string')
  }

  return {
    valid: errors.length === 0,
    errors
  }
}

/**
 * Prepares JSON-LD schema markup for rendering
 * Returns script tags array that can be used with useHead()
 */
export function prepareSchemaScripts(
  schema: string | SchemaObject | SchemaObject[] | null | undefined
): Array<{ type: string; key: string; innerHTML: string }> {
  if (!schema) return []

  let schemas: SchemaObject[] = []

  // Handle string schema (from database)
  if (typeof schema === 'string') {
    try {
      const parsed = JSON.parse(schema)
      schemas = Array.isArray(parsed) ? parsed : [parsed]
    } catch (error: any) {
      console.warn('Invalid JSON-LD schema (parse error):', error.message)
      return []
    }
  } else if (Array.isArray(schema)) {
    schemas = schema
  } else if (typeof schema === 'object') {
    schemas = [schema]
  } else {
    console.warn('Invalid schema type:', typeof schema)
    return []
  }

  // Validate and filter schemas
  const validSchemas: SchemaObject[] = []
  schemas.forEach((schemaObj, index) => {
    const validation = validateSchema(schemaObj)
    if (validation.valid) {
      validSchemas.push(schemaObj)
    } else {
      console.warn(`Schema ${index} validation failed:`, validation.errors)
    }
  })

  if (validSchemas.length === 0) {
    console.warn('No valid schemas to render')
    return []
  }

  // Create script tags for each valid schema
  return validSchemas.map((schemaObj, index) => ({
    type: 'application/ld+json',
    key: `schema-${index}`,
    innerHTML: JSON.stringify(schemaObj, null, 2)
  }))
}

/**
 * Generate automatic Product schema from product data
 */
export function generateProductSchema(product: any, baseUrl: string): SchemaObject | null {
  if (!product) return null

  const productUrl = `${baseUrl}/products/${product.slug}`
  const imageUrl = product.primary_image || product.og_image_url || product.image_url

  // Build image array
  const images: string[] = []
  if (imageUrl) {
    images.push(imageUrl)
  }
  if (product.images && Array.isArray(product.images)) {
    product.images.forEach((img: any) => {
      const imgUrl = img.image_url || img.image
      if (imgUrl && !images.includes(imgUrl)) {
        images.push(imgUrl)
      }
    })
  }

  const schema: SchemaObject = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.meta_description || (product.description ? product.description.substring(0, 500) : ''),
    image: images.length > 0 ? images : undefined,
    sku: product.id?.toString() || '',
    brand: {
      '@type': 'Brand',
      name: product.vendor_name || product.supplier?.name || 'Unknown'
    },
    offers: {
      '@type': 'Offer',
      url: productUrl,
      priceCurrency: 'IRR',
      price: product.price ? (product.price / 100).toFixed(2) : '0.00',
      availability: product.stock > 0
        ? 'https://schema.org/InStock'
        : 'https://schema.org/OutOfStock',
      seller: {
        '@type': 'Organization',
        name: product.vendor_name || product.supplier?.name || 'Unknown'
      }
    }
  }

  // Add aggregate rating if available
  if (product.average_rating > 0 && product.comment_count > 0) {
    schema.aggregateRating = {
      '@type': 'AggregateRating',
      ratingValue: product.average_rating,
      reviewCount: product.comment_count
    }
  }

  return schema
}

/**
 * Generate automatic BreadcrumbList schema
 */
export function generateBreadcrumbSchema(
  breadcrumbs: Array<{ name?: string; title?: string; text?: string; url?: string; to?: string; href?: string }>,
  baseUrl = ''
): SchemaObject | null {
  if (!breadcrumbs || breadcrumbs.length === 0) return null

  const itemListElement = breadcrumbs
    .map((item, index) => {
      const name = item.name || item.title || item.text
      let url = item.url || item.to || item.href

      // If URL is relative, make it absolute
      if (url && baseUrl && !url.startsWith('http')) {
        url = `${baseUrl}${url.startsWith('/') ? url : '/' + url}`
      }

      if (!name || !url) return null

      return {
        '@type': 'ListItem',
        position: index + 1,
        name: name,
        item: url
      }
    })
    .filter(Boolean) as Array<{ '@type': string; position: number; name: string; item: string }>

  if (itemListElement.length === 0) return null

  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: itemListElement
  }
}

/**
 * Generate automatic Article schema for blog posts
 */
export function generateArticleSchema(post: any, baseUrl: string): SchemaObject | null {
  if (!post) return null

  const articleUrl = `${baseUrl}/blog/${post.slug}`
  const images = post.featured_image ? [post.featured_image] : []

  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.meta_description || post.excerpt || '',
    image: images.length > 0 ? images : undefined,
    datePublished: post.published_at || post.created_at,
    dateModified: post.updated_at,
    author: {
      '@type': 'Person',
      name: post.author_name || 'Unknown'
    },
    publisher: {
      '@type': 'Organization',
      name: 'ایندکسو',
      logo: {
        '@type': 'ImageObject',
        url: `${baseUrl}/icon.jpg`
      }
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': articleUrl
    }
  }
}

/**
 * Generate automatic CollectionPage schema for categories and subcategories
 * Includes product list (first 10 products)
 */
export function generateCollectionPageSchema(
  collection: { name: string; description?: string; slug: string; meta_description?: string },
  products: Array<{ name: string; slug: string; id?: number | string }>,
  baseUrl: string,
  type: 'Category' | 'Subcategory'
): SchemaObject | null {
  if (!collection) return null

  const collectionUrl = `${baseUrl}/${type.toLowerCase()}s/${collection.slug}`
  const productList = (products || []).slice(0, 10).map((product, index) => {
    const productSlug = product.slug || product.id
    return {
      '@type': 'ListItem',
      position: index + 1,
      name: product.name,
      url: `${baseUrl}/products/${productSlug}`
    }
  })

  return {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: collection.name,
    description: collection.meta_description || collection.description || '',
    url: collectionUrl,
    mainEntity: {
      '@type': 'ItemList',
      numberOfItems: productList.length,
      itemListElement: productList
    }
  }
}

/**
 * Generate automatic Organization schema for suppliers/stores
 */
export function generateOrganizationSchema(supplier: any, baseUrl: string): SchemaObject | null {
  if (!supplier) return null

  const supplierUrl = `${baseUrl}/suppliers/${supplier.id}`
  const logoUrl = supplier.logo || supplier.banner_image

  const schema: SchemaObject = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: supplier.store_name,
    description: supplier.meta_description || supplier.description || '',
    url: supplier.website || supplierUrl,
    image: logoUrl ? [logoUrl] : undefined,
    logo: logoUrl ? {
      '@type': 'ImageObject',
      url: logoUrl
    } : undefined
  }

  // Add address if available
  if (supplier.address) {
    schema.address = {
      '@type': 'PostalAddress',
      streetAddress: supplier.address
    }
  }

  // Add contact point
  if (supplier.contact_phone || supplier.contact_email) {
    schema.contactPoint = {
      '@type': 'ContactPoint',
      ...(supplier.contact_phone && { telephone: supplier.contact_phone }),
      ...(supplier.contact_email && { email: supplier.contact_email }),
      contactType: 'Customer Service'
    }
  }

  // Add founding date
  if (supplier.year_established) {
    schema.foundingDate = `${supplier.year_established}-01-01`
  }

  // Add number of employees
  if (supplier.employee_count) {
    schema.numberOfEmployees = {
      '@type': 'QuantitativeValue',
      value: supplier.employee_count
    }
  }

  return schema
}

