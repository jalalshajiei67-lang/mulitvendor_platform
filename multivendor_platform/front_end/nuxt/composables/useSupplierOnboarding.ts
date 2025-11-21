import { driver, type DriveStep, type Config } from 'driver.js'
import 'driver.js/dist/driver.css'

// Custom styles for larger, friendlier tour popovers
const customTourStyles = `
  .driver-popover {
    font-size: 18px !important;
    line-height: 1.6 !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
    max-width: 450px !important;
  }

  .driver-popover .driver-popover-title {
    font-size: 24px !important;
    font-weight: 700 !important;
    color: #1976d2 !important;
    margin-bottom: 12px !important;
  }

  .driver-popover .driver-popover-description {
    font-size: 18px !important;
    color: #424242 !important;
    margin-bottom: 16px !important;
  }

  .driver-popover .driver-popover-next-btn,
  .driver-popover .driver-popover-prev-btn,
  .driver-popover .driver-popover-close-btn,
  .driver-popover .driver-popover-done-btn {
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    border-radius: 8px !important;
    min-width: 80px !important;
  }

  .driver-popover .driver-popover-next-btn {
    background-color: #1976d2 !important;
    color: white !important;
  }

  .driver-popover .driver-popover-next-btn:hover {
    background-color: #1565c0 !important;
  }

  .driver-popover .driver-popover-prev-btn {
    background-color: #757575 !important;
    color: white !important;
  }

  .driver-popover .driver-popover-prev-btn:hover {
    background-color: #616161 !important;
  }

  .driver-popover .driver-popover-close-btn {
    color: #757575 !important;
    font-size: 20px !important;
  }

  .driver-popover .driver-popover-progress-text {
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #1976d2 !important;
  }

  /* RTL specific adjustments */
  [dir="rtl"] .driver-popover {
    text-align: right !important;
  }

  [dir="rtl"] .driver-popover .driver-popover-next-btn::before {
    content: "← ";
  }

  [dir="rtl"] .driver-popover .driver-popover-prev-btn::after {
    content: " →";
  }

  /* Highlighted element styling */
  .driver-highlighted-element {
    border-radius: 8px !important;
    box-shadow: 0 0 0 4px rgba(25, 118, 210, 0.3) !important;
  }
`

// Inject custom styles
if (typeof document !== 'undefined') {
  const styleElement = document.createElement('style')
  styleElement.textContent = customTourStyles
  document.head.appendChild(styleElement)
}

interface TourStep {
  id: string
  element?: string
  title: string
  description: string
  action?: 'click' | 'input' | 'navigate' | 'save' | 'upload'
  actionTarget?: string
  side?: 'top' | 'bottom' | 'left' | 'right'
  align?: 'start' | 'center' | 'end'
  waitForAction?: boolean
  nextButtonText?: string
}

export const useSupplierOnboarding = () => {
  const TOUR_STORAGE_KEY = 'supplier_tour_completed'
  const TOUR_DISMISSED_KEY = 'supplier_tour_dismissed'
  const TOUR_PROGRESS_KEY = 'supplier_tour_progress'

  // Check if tour should be shown
  const shouldShowTour = (): boolean => {
    if (typeof window === 'undefined') return false
    const completed = localStorage.getItem(TOUR_STORAGE_KEY)
    const dismissed = localStorage.getItem(TOUR_DISMISSED_KEY)
    return !completed && !dismissed
  }

  // Mark tour as completed
  const markTourCompleted = (): void => {
    if (typeof window !== 'undefined') {
      localStorage.setItem(TOUR_STORAGE_KEY, 'true')
      localStorage.removeItem(TOUR_PROGRESS_KEY)
    }
  }

  // Mark tour as dismissed (don't show again)
  const dismissTour = (): void => {
    if (typeof window !== 'undefined') {
      localStorage.setItem(TOUR_DISMISSED_KEY, 'true')
    }
  }

  // Reset tour (for testing or if user wants to see it again)
  const resetTour = (): void => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(TOUR_STORAGE_KEY)
      localStorage.removeItem(TOUR_DISMISSED_KEY)
      localStorage.removeItem(TOUR_PROGRESS_KEY)
    }
  }

  // Get current tour progress
  const getTourProgress = (): number => {
    if (typeof window === 'undefined') return 0
    const progress = localStorage.getItem(TOUR_PROGRESS_KEY)
    return progress ? parseInt(progress) : 0
  }

  // Save tour progress
  const saveTourProgress = (stepIndex: number): void => {
    if (typeof window !== 'undefined') {
      localStorage.setItem(TOUR_PROGRESS_KEY, stepIndex.toString())
    }
  }

  // Interactive tour steps for new suppliers
  const getInteractiveTourSteps = (): TourStep[] => {
    return [
      {
        id: 'welcome',
        title: '🌟 بیایید فروشگاه شما را راه‌اندازی کنیم!',
        description: 'ما شما را قدم به قدم راهنمایی می‌کنیم. اولین قدم: اضافه کردن اولین محصول شما.',
        side: 'bottom',
        align: 'start'
      },
      {
        id: 'products-tab',
        element: '[data-tour="products-tab"]',
        title: '📦 محصولات شما',
        description: 'اینجا محصولاتی که می‌فروشید را اضافه کنید. هر چه محصول بیشتر باشد، فروش بیشتر!',
        action: 'click',
        actionTarget: '[data-tour="products-tab"]',
        waitForAction: true,
        side: 'bottom',
        align: 'start',
        nextButtonText: 'بزنید روی محصولات'
      },
      {
        id: 'add-product-btn',
        element: '[data-tour="add-product-btn"]',
        title: '➕ افزودن محصول جدید',
        description: 'حالا روی این دکمه کلیک کنید تا محصول اول خود را اضافه کنیم.',
        action: 'click',
        actionTarget: '[data-tour="add-product-btn"]',
        waitForAction: true,
        side: 'left',
        align: 'start',
        nextButtonText: 'کلیک کنید'
      },
      {
        id: 'product-name',
        element: '[data-tour="product-name-input"]',
        title: '✏️ نام محصول',
        description: 'نام محصول را بنویسید. مثلاً "مبل راحتی سه نفره" یا "یخچال سامسونگ"',
        action: 'input',
        actionTarget: '[data-tour="product-name-input"]',
        waitForAction: true,
        side: 'top',
        align: 'start',
        nextButtonText: 'وقتی نام را نوشتید'
      },
      {
        id: 'product-description',
        element: '[data-tour="product-description-input"]',
        title: '📝 توضیحات محصول',
        description: 'توضیحات کامل محصول را بنویسید. مشتریان می‌خواهند بدانند محصول شما چه ویژگی‌هایی دارد.',
        action: 'input',
        actionTarget: '[data-tour="product-description-input"]',
        waitForAction: true,
        side: 'top',
        align: 'start',
        nextButtonText: 'وقتی توضیحات را نوشتید'
      },
      {
        id: 'product-price',
        element: '[data-tour="product-price-input"]',
        title: '💰 قیمت محصول',
        description: 'قیمت محصول را به تومان وارد کنید. مثلاً اگر محصول ۲ میلیون تومان است، بنویسید: ۲۰۰۰۰۰۰',
        action: 'input',
        actionTarget: '[data-tour="product-price-input"]',
        waitForAction: true,
        side: 'top',
        align: 'start',
        nextButtonText: 'وقتی قیمت را نوشتید'
      },
      {
        id: 'product-category',
        element: '[data-tour="product-category-input"]',
        title: '📂 دسته‌بندی محصول',
        description: 'محصول خود را در دسته مناسب قرار دهید. مثلاً "مبلمان" یا "لوازم خانگی"',
        action: 'input',
        actionTarget: '[data-tour="product-category-input"]',
        waitForAction: true,
        side: 'top',
        align: 'start',
        nextButtonText: 'وقتی دسته را انتخاب کردید'
      },
      {
        id: 'product-save',
        element: '[data-tour="product-save-button"]',
        title: '💾 ذخیره محصول',
        description: 'حالا روی دکمه ذخیره کلیک کنید تا محصول شما اضافه شود.',
        action: 'click',
        actionTarget: '[data-tour="product-save-button"]',
        waitForAction: true,
        side: 'top',
        align: 'start',
        nextButtonText: 'ذخیره کنید'
      },
      {
        id: 'product-success',
        title: '🎉 عالی! محصول شما اضافه شد',
        description: 'تبریک! اولین محصول شما با موفقیت اضافه شد. حالا بیایید صفحه فروشگاه شما را طراحی کنیم.',
        side: 'top',
        align: 'center'
      },
      {
        id: 'miniwebsite-tab',
        element: '[data-tour="miniwebsite-tab"]',
        title: '🌐 صفحه فروشگاه شما',
        description: 'این بخش مثل ویترین مغازه شماست. مشتریان اینجا شما و محصولاتتان را می‌بینند.',
        action: 'click',
        actionTarget: '[data-tour="miniwebsite-tab"]',
        waitForAction: true,
        side: 'bottom',
        align: 'start',
        nextButtonText: 'بزنید روی وب‌سایت مینی'
      },
      {
        id: 'miniwebsite-settings',
        element: '[data-tour="miniwebsite-settings"]',
        title: '🎨 تنظیمات فروشگاه',
        description: 'اینجا نام فروشگاه و توضیحات خود را وارد کنید تا مشتریان شما را بشناسند.',
        action: 'click',
        actionTarget: '[data-tour="miniwebsite-settings"]',
        waitForAction: true,
        side: 'right',
        align: 'start',
        nextButtonText: 'کلیک کنید'
      },
      {
        id: 'store-name',
        element: '[data-tour="store-name-input"]',
        title: '🏪 نام فروشگاه',
        description: 'نام فروشگاه خود را بنویسید. مثلاً "فروشگاه مبلمان رضایی" یا "لوازم خانگی احمدی"',
        action: 'input',
        actionTarget: '[data-tour="store-name-input"]',
        waitForAction: true,
        side: 'top',
        align: 'start',
        nextButtonText: 'وقتی نام را نوشتید'
      },
      {
        id: 'store-description',
        element: '[data-tour="store-description-input"]',
        title: '📖 درباره فروشگاه',
        description: 'چند جمله درباره تجربه کاری، تخصص و محصولات خود بنویسید. مشتریان دوست دارند بدانند با چه کسی طرف هستند.',
        action: 'input',
        actionTarget: '[data-tour="store-description-input"]',
        waitForAction: true,
        side: 'top',
        align: 'start',
        nextButtonText: 'وقتی توضیحات را نوشتید'
      },
      {
        id: 'settings-save',
        element: '[data-tour="settings-save-button"]',
        title: '💾 ذخیره تنظیمات',
        description: 'روی این دکمه کلیک کنید تا اطلاعات فروشگاه شما ذخیره شود.',
        action: 'click',
        actionTarget: '[data-tour="settings-save-button"]',
        waitForAction: true,
        side: 'top',
        align: 'start',
        nextButtonText: 'ذخیره کنید'
      },
      {
        id: 'portfolio-tab',
        element: '[data-tour="miniwebsite-portfolio"]',
        title: '💼 نمونه کارها',
        description: 'اینجا عکس از محصولاتی که فروخته‌اید یا کارهایی که انجام داده‌اید بگذارید. مثل ویترین مغازه!',
        action: 'click',
        actionTarget: '[data-tour="miniwebsite-portfolio"]',
        waitForAction: true,
        side: 'right',
        align: 'start',
        nextButtonText: 'کلیک کنید'
      },
      {
        id: 'add-portfolio',
        element: '[data-tour="add-portfolio-button"]',
        title: '📸 اضافه کردن نمونه کار',
        description: 'روی این دکمه کلیک کنید تا اولین نمونه کار خود را اضافه کنیم.',
        action: 'click',
        actionTarget: '[data-tour="add-portfolio-button"]',
        waitForAction: true,
        side: 'top',
        align: 'start',
        nextButtonText: 'کلیک کنید'
      },
      {
        id: 'team-tab',
        element: '[data-tour="miniwebsite-team"]',
        title: '👥 معرفی تیم',
        description: 'اینجا خودتان و همکارانتان را معرفی کنید. مشتریان دوست دارند بدانند با چه کسانی طرف هستند.',
        action: 'click',
        actionTarget: '[data-tour="miniwebsite-team"]',
        waitForAction: true,
        side: 'right',
        align: 'start',
        nextButtonText: 'کلیک کنید'
      },
      {
        id: 'add-team',
        element: '[data-tour="add-team-button"]',
        title: '👤 اضافه کردن عضو تیم',
        description: 'روی این دکمه کلیک کنید تا خودتان را به عنوان عضو تیم معرفی کنید.',
        action: 'click',
        actionTarget: '[data-tour="add-team-button"]',
        waitForAction: true,
        side: 'top',
        align: 'start',
        nextButtonText: 'کلیک کنید'
      },
      {
        id: 'completion',
        title: '🎊 تبریک! فروشگاه شما آماده است',
        description: 'حالا فروشگاه آنلاین شما کامل شده! مشتریان می‌توانند محصولات شما را ببینند و با شما تماس بگیرند. موفق باشید!',
        side: 'top',
        align: 'center'
      }
    ]
  }

  // Quick tour steps for experienced users
  const getQuickTourSteps = (): DriveStep[] => {
    return [
      {
        element: '[data-tour="welcome"]',
        popover: {
          title: '🌟 خوش آمدید!',
          description: 'یک یادآوری سریع از امکانات پنل فروشنده.',
          side: 'bottom',
          align: 'start'
        }
      },
      {
        element: '[data-tour="products-tab"]',
        popover: {
          title: '📦 محصولات',
          description: 'محصولات خود را اینجا مدیریت کنید.',
          side: 'bottom',
          align: 'start'
        }
      },
      {
        element: '[data-tour="miniwebsite-tab"]',
        popover: {
          title: '🌐 وب‌سایت مینی',
          description: 'صفحه عمومی فروشگاه خود را اینجا طراحی کنید.',
          side: 'bottom',
          align: 'start'
        }
      },
      {
        element: '[data-tour="profile-tab"]',
        popover: {
          title: '📝 پروفایل',
          description: 'اطلاعات شخصی خود را کامل کنید.',
          side: 'bottom',
          align: 'start'
        }
      },
      {
        popover: {
          title: '✅ آماده هستید؟',
          description: 'حالا می‌توانید فروشگاه آنلاین خود را مدیریت کنید!',
          side: 'top',
          align: 'center'
        }
      }
    ]
  }

  // Wait for user action to complete
  const waitForAction = (actionType: string, target: string, timeout = 30000): Promise<void> => {
    return new Promise((resolve, reject) => {
      const timeoutId = setTimeout(() => {
        reject(new Error('Action timeout'))
      }, timeout)

      const checkAction = () => {
        let completed = false

        switch (actionType) {
          case 'click':
            // Check if element was clicked (we'll track this via events)
            const element = document.querySelector(target)
            if (element && element.classList.contains('tour-action-completed')) {
              completed = true
            }
            break
          case 'input':
            // Check if input has value
            const input = document.querySelector(target) as HTMLInputElement
            if (input && input.value && input.value.trim().length > 0) {
              completed = true
            }
            break
          case 'navigate':
            // Check if user navigated to the right tab/section
            if (target.includes('products') && window.location.hash.includes('#products')) {
              completed = true
            }
            break
        }

        if (completed) {
          clearTimeout(timeoutId)
          resolve()
        } else {
          setTimeout(checkAction, 500)
        }
      }

      checkAction()
    })
  }

  // Interactive tour driver configuration
  const getInteractiveDriverConfig = (onComplete?: () => void, onDismiss?: () => void): Config => {
    const steps = getInteractiveTourSteps()

    return {
      showProgress: true,
      progressText: '{{current}} از {{total}}',
      showButtons: ['next', 'previous', 'close'],
      allowClose: true,
      overlayClickNext: false,

      // RTL support
      rtl: true,

      // Button texts in Persian
      nextBtnText: 'بعدی ←',
      prevBtnText: '→ قبلی',
      doneBtnText: '✓ تمام شد',

      // Callbacks
      onDestroyed: () => {
        if (onComplete) onComplete()
      },

      onDestroyStarted: () => {
        if (onDismiss) onDismiss()
      },

      onNextClick: (element, step, opts) => {
        // Get current step index from driver state
        const state = opts.state
        const currentIndex = state.activeIndex ?? 0
        
        // Save progress
        saveTourProgress(currentIndex + 1)
        
        // Let driver handle moving to next step
        opts.moveNext()
      },

      onPrevClick: (element, step, opts) => {
        // Get current step index from driver state
        const state = opts.state
        const currentIndex = state.activeIndex ?? 0
        
        // Save progress
        if (currentIndex > 0) {
          saveTourProgress(currentIndex - 1)
        }
        
        // Let driver handle moving to previous step
        opts.movePrevious()
      },

      // Custom steps with interactive elements
      steps: steps.map((step) => ({
        element: step.element,
        popover: {
          title: step.title,
          description: step.description,
          side: step.side || 'bottom',
          align: step.align || 'start'
        }
      }))
    }
  }

  // Quick tour driver configuration
  const getQuickDriverConfig = (onComplete?: () => void, onDismiss?: () => void): Config => {
    return {
      showProgress: true,
      showButtons: ['next', 'previous', 'close'],
      allowClose: true,
      overlayClickNext: false,

      rtl: true,
      nextBtnText: 'بعدی ←',
      prevBtnText: '→ قبلی',
      doneBtnText: '✓ متوجه شدم',

      onDestroyed: () => {
        if (onComplete) onComplete()
      },

      onDestroyStarted: () => {
        if (onDismiss) onDismiss()
      },

      steps: getQuickTourSteps()
    }
  }

  // Store driver instance for explicit control
  let activeDriverInstance: ReturnType<typeof driver> | null = null

  // Start interactive tour (for new users)
  const startInteractiveTour = (onComplete?: () => void, onDismiss?: () => void) => {
    if (typeof window === 'undefined') return

    // Destroy any existing instance first
    if (activeDriverInstance) {
      try {
        activeDriverInstance.destroy()
      } catch (e) {
        // Ignore
      }
      activeDriverInstance = null
    }

    const wrappedOnComplete = () => {
      markTourCompleted()
      if (activeDriverInstance) {
        activeDriverInstance.destroy()
        activeDriverInstance = null
      }
      if (onComplete) onComplete()
    }

    const wrappedOnDismiss = () => {
      if (activeDriverInstance) {
        activeDriverInstance.destroy()
        activeDriverInstance = null
      }
      if (onDismiss) onDismiss()
    }

    activeDriverInstance = driver(getInteractiveDriverConfig(wrappedOnComplete, wrappedOnDismiss))
    const startStep = getTourProgress()
    activeDriverInstance.drive(startStep)
  }

  // Start quick tour (for returning users)
  const startQuickTour = (onComplete?: () => void, onDismiss?: () => void) => {
    if (typeof window === 'undefined') return

    // Destroy any existing instance first
    if (activeDriverInstance) {
      try {
        activeDriverInstance.destroy()
      } catch (e) {
        // Ignore
      }
      activeDriverInstance = null
    }

    const wrappedOnComplete = () => {
      if (activeDriverInstance) {
        activeDriverInstance.destroy()
        activeDriverInstance = null
      }
      if (onComplete) onComplete()
    }

    const wrappedOnDismiss = () => {
      if (activeDriverInstance) {
        activeDriverInstance.destroy()
        activeDriverInstance = null
      }
      if (onDismiss) onDismiss()
    }

    activeDriverInstance = driver(getQuickDriverConfig(wrappedOnComplete, wrappedOnDismiss))
    activeDriverInstance.drive()
  }

  // Main tour start function (decides which tour to show)
  const startTour = (onComplete?: () => void, onDismiss?: () => void) => {
    if (shouldShowTour()) {
      startInteractiveTour(onComplete, onDismiss)
    } else {
      startQuickTour(onComplete, onDismiss)
    }
  }

  // Mark action as completed (called from components)
  const markActionCompleted = (actionId: string) => {
    if (typeof window !== 'undefined') {
      const element = document.querySelector(`[data-tour="${actionId}"]`)
      if (element) {
        element.classList.add('tour-action-completed')
      }
    }
  }

  return {
    shouldShowTour,
    markTourCompleted,
    dismissTour,
    resetTour,
    startTour,
    startInteractiveTour,
    startQuickTour,
    markActionCompleted,
    getTourProgress,
    getInteractiveTourSteps,
    getQuickTourSteps
  }
}


