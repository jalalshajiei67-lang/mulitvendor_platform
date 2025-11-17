// Deep merge utility function
function deepMerge(target: any, source: any): any {
  const output = { ...target }
  if (isObject(target) && isObject(source)) {
    Object.keys(source).forEach((key) => {
      if (isObject(source[key])) {
        if (!(key in target)) {
          Object.assign(output, { [key]: source[key] })
        } else {
          output[key] = deepMerge(target[key], source[key])
        }
      } else {
        Object.assign(output, { [key]: source[key] })
      }
    })
  }
  return output
}

function isObject(item: any): boolean {
  return item && typeof item === 'object' && !Array.isArray(item)
}

export default defineNuxtPlugin((nuxtApp) => {
  const vuetify = (nuxtApp as any).$vuetify

  // Ensure translations are properly set (fallback in case config didn't apply)
  if (!vuetify?.locale) {
    return
  }

  const messages = vuetify.locale.messages.value || {}
  const faMessages = messages.fa || {}
  const currentVuetify = faMessages.$vuetify || {}

  // Ensure critical missing keys are present
  const requiredKeys = {
    open: 'باز کردن',
    close: 'بستن',
    input: {
      clear: 'پاک کردن',
      appendAction: 'عملیات اضافی',
      prependAction: 'عملیات اولیه'
    }
  }

  // Deep merge to ensure all keys are present
  const mergedVuetify = deepMerge(currentVuetify, requiredKeys)

  // Only update if we actually merged something new
  if (JSON.stringify(mergedVuetify) !== JSON.stringify(currentVuetify)) {
    vuetify.locale.messages.value = {
      ...messages,
      fa: {
        ...faMessages,
        $vuetify: mergedVuetify
      }
    }
  }
})
