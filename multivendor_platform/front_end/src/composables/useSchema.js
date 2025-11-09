// src/composables/useSchema.js

/**
 * Validates JSON-LD schema structure
 * @param {object} schema - Schema object to validate
 * @returns {object} { valid: boolean, errors: array }
 */
function validateSchema(schema) {
  const errors = []

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
 * @param {string|object|array} schema - JSON-LD schema as string, object, or array of schemas
 * @returns {array} Array of script tag objects for useHead()
 */
export function prepareSchemaScripts(schema) {
  if (!schema) return []

  let schemas = []

  // Handle string schema (from database)
  if (typeof schema === 'string') {
    try {
      const parsed = JSON.parse(schema)
      schemas = Array.isArray(parsed) ? parsed : [parsed]
    } catch (error) {
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
  const validSchemas = []
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
 * @param {object} product - Product object
 * @param {string} baseUrl - Base URL for the site
 * @returns {object} Product schema object
 */
export function generateProductSchema(product, baseUrl) {
  if (!product) return null

  const productUrl = `${baseUrl}/products/${product.slug}`
  const imageUrl = product.primary_image || product.og_image_url || product.image_url

  // Build image array
  const images = []
  if (imageUrl) {
    images.push(imageUrl)
  }
  if (product.images && Array.isArray(product.images)) {
    product.images.forEach(img => {
      const imgUrl = img.image_url || img.image
      if (imgUrl && !images.includes(imgUrl)) {
        images.push(imgUrl)
      }
    })
  }

  const schema = {
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
 * @param {array} breadcrumbs - Array of breadcrumb items {name, url} or {title, to} or {text, to}
 * @param {string} baseUrl - Base URL for the site
 * @returns {object} BreadcrumbList schema object
 */
export function generateBreadcrumbSchema(breadcrumbs, baseUrl = '') {
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
    .filter(Boolean)

  if (itemListElement.length === 0) return null

  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: itemListElement
  }
}

/**
 * Generate automatic Article schema for blog posts
 * @param {object} post - Blog post object
 * @param {string} baseUrl - Base URL for the site
 * @returns {object} Article schema object
 */
export function generateArticleSchema(post, baseUrl) {
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

