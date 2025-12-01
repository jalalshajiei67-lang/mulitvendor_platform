/**
 * Decodes HTML entities in a string
 * Handles double/triple encoding by decoding until no more changes occur
 */
export const decodeHtmlEntities = (input) => {
  if (!input) return input
  
  // Handle double-encoding by decoding multiple times if needed
  let decoded = input
  let previousDecoded = ''
  
  // Decode until no more changes occur (handles double/triple encoding)
  while (decoded !== previousDecoded) {
    previousDecoded = decoded
    decoded = decoded
      .replace(/&lt;/gi, '<')
      .replace(/&gt;/gi, '>')
      .replace(/&quot;/gi, '"')
      .replace(/&#39;/gi, "'")
      .replace(/&#x27;/gi, "'")
      .replace(/&zwnj;/gi, '\u200C')
      .replace(/&nbsp;/gi, ' ')
      .replace(/&amp;/gi, '&')
      .replace(/&#160;/gi, ' ')
      .replace(/&apos;/gi, "'")
      .replace(/&mdash;/gi, '—')
      .replace(/&ndash;/gi, '–')
      .replace(/&#8211;/gi, '–')
      .replace(/&#8212;/gi, '—')
  }
  
  return decoded
}

/**
 * Decodes HTML entities and returns the decoded string for use with v-html
 */
export const decodeHtmlForDisplay = (input) => {
  if (!input) return ''
  return decodeHtmlEntities(input)
}





