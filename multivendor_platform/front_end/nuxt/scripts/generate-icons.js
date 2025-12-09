import sharp from 'sharp'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'
import { existsSync, mkdirSync } from 'fs'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const sourceImage = join(__dirname, '../public/indexo.jpg')
const iconsDir = join(__dirname, '../public/icons')

// Create icons directory if it doesn't exist
if (!existsSync(iconsDir)) {
  mkdirSync(iconsDir, { recursive: true })
}

// Icon sizes to generate
const iconSizes = [
  { size: 192, name: 'pwa-192x192.png' },
  { size: 512, name: 'pwa-512x512.png' },
  { size: 180, name: 'apple-touch-icon.png' },
  { size: 32, name: 'favicon-32x32.png' },
  { size: 16, name: 'favicon-16x16.png' }
]

async function generateIcons() {
  try {
    // Check if source image exists
    if (!existsSync(sourceImage)) {
      console.warn(`Source image not found: ${sourceImage}`)
      console.warn('Please ensure indexo.jpg exists in the public directory')
      return
    }

    console.log('Generating PWA icons from', sourceImage)

    // Generate each icon size
    for (const { size, name } of iconSizes) {
      const outputPath = join(iconsDir, name)
      await sharp(sourceImage)
        .resize(size, size, {
          fit: 'cover',
          position: 'center'
        })
        .png()
        .toFile(outputPath)
      console.log(`✓ Generated ${name} (${size}x${size})`)
    }

    // Generate Safari pinned tab SVG (simplified - just a reference)
    // Note: For a proper SVG, you'd need to create a proper SVG file
    // For now, we'll create a simple placeholder
    const svgContent = `<?xml version="1.0" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" fill="#4CAF50"/>
  <text x="256" y="280" font-family="Arial, sans-serif" font-size="200" font-weight="bold" fill="white" text-anchor="middle">I</text>
</svg>`
    
    const fs = await import('fs/promises')
    await fs.writeFile(join(iconsDir, 'safari-pinned-tab.svg'), svgContent)
    console.log('✓ Generated safari-pinned-tab.svg')

    console.log('\n✅ All PWA icons generated successfully!')
  } catch (error) {
    console.error('Error generating icons:', error)
    process.exit(1)
  }
}

generateIcons()

