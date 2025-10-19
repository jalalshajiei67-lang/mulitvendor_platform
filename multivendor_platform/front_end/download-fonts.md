# IRANSans Font Download Instructions

## Quick Setup

1. **Download IRANSans Font Files:**
   - Go to: https://github.com/rastikerdar/iransans-font
   - Click on "Releases" or download the latest version
   - Extract the downloaded files

2. **Copy Font Files:**
   - Copy the following font files to `src/assets/fonts/` directory:
     - IRANSans-Regular.woff2
     - IRANSans-Regular.woff
     - IRANSans-Regular.ttf
     - IRANSans-Medium.woff2
     - IRANSans-Medium.woff
     - IRANSans-Medium.ttf
     - IRANSans-Bold.woff2
     - IRANSans-Bold.woff
     - IRANSans-Bold.ttf
     - IRANSans-Light.woff2
     - IRANSans-Light.woff
     - IRANSans-Light.ttf
     - IRANSans-UltraLight.woff2
     - IRANSans-UltraLight.woff
     - IRANSans-UltraLight.ttf

3. **Alternative - Use Vazirmatn (Recommended):**
   If you can't find IRANSans, you can use Vazirmatn which is also excellent for Persian:
   - Go to: https://github.com/rastikerdar/vazirmatn
   - Download and extract the font files
   - Rename them to match the IRANSans naming convention

## What's Already Done:
✅ Font directory created: `src/assets/fonts/`
✅ CSS font definitions created: `src/assets/fonts.css`
✅ Font CSS imported in: `src/main.js`
✅ Base CSS updated to use IRANSans
✅ App.vue updated to use IRANSans

## After Adding Font Files:
1. Run your development server: `npm run dev`
2. The IRANSans font should now be applied to your Persian text
3. You can also use the utility classes:
   - `.font-iransans`
   - `.font-iransans-light`
   - `.font-iransans-regular`
   - `.font-iransans-medium`
   - `.font-iransans-bold`

## Testing:
Open your browser's developer tools and check the "Computed" styles to verify that IRANSans is being used for Persian text elements.
