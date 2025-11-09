// src/stores/utils/translations.js
export const persianTranslations = {
  // Common
  loading: 'در حال بارگذاری...',
  error: 'خطا',
  save: 'ذخیره',
  cancel: 'لغو',
  delete: 'حذف',
  edit: 'ویرایش',
  view: 'مشاهده',
  create: 'ایجاد',
  update: 'بروزرسانی',
  search: 'جستجو',
  filter: 'فیلتر',
  all: 'همه',
  active: 'فعال',
  inactive: 'غیرفعال',
  actions: 'عملیات',
  
  // Pagination
  previous: 'قبلی',
  next: 'بعدی',
  page: 'صفحه',
  of: 'از',
  
  // Status messages
  failedToFetch: 'خطا در دریافت اطلاعات',
  failedToCreate: 'خطا در ایجاد',
  failedToUpdate: 'خطا در بروزرسانی',
  failedToDelete: 'خطا در حذف',
  notFound: 'یافت نشد',
  
  // Product specific
  products: 'محصولات',
  product: 'محصول',
  myProducts: 'محصولات من',
  price: 'قیمت',
  stock: 'موجودی',
  description: 'توضیحات',
  image: 'تصویر',
  name: 'نام',
  inStock: 'موجود',
  outOfStock: 'ناموجود',
  soldBy: 'فروشنده',
  addToCart: 'افزودن به سبد خرید',
  
  // Category specific
  categories: 'دسته‌بندی‌ها',
  category: 'دسته‌بندی',
  subcategories: 'زیردسته‌ها',
  subcategory: 'زیردسته',
  departments: 'دپارتمان‌ها',
  department: 'دپارتمان',
  
  // Order specific
  orders: 'سفارش‌ها',
  order: 'سفارش',
  orderStatus: 'وضعیت سفارش',
  total: 'مجموع',
  quantity: 'تعداد',
  
  // Comments
  comments: 'نظرات',
  comment: 'نظر',
  rating: 'امتیاز',
  noCommentsYet: 'هنوز نظری ثبت نشده',
  
  // Search
  searchProducts: 'جستجوی محصولات...',
  searchCategories: 'جستجوی دسته‌بندی‌ها...',
  searchOrders: 'جستجوی سفارش‌ها...',
  
  // Sorting
  newestFirst: 'جدیدترین اول',
  oldestFirst: 'قدیمی‌ترین اول',
  priceLowToHigh: 'قیمت: کم به زیاد',
  priceHighToLow: 'قیمت: زیاد به کم',
  nameAToZ: 'نام: الف تا ی',
  nameZToA: 'نام: ی تا الف',
  
  // Form validation
  requiredField: 'این فیلد الزامی است',
  invalidFormat: 'فرمت نامعتبر است',
  
  // Confirmation dialogs
  confirmDelete: 'آیا مطمئن هستید که می‌خواهید حذف کنید؟',
  confirmUpdate: 'آیا مطمئن هستید که می‌خواهید بروزرسانی کنید؟',
  
  // Loading states
  loadingProduct: 'در حال بارگذاری محصول...',
  loadingProducts: 'در حال بارگذاری محصولات...',
  loadingCategories: 'در حال بارگذاری دسته‌بندی‌ها...',
  loadingOrders: 'در حال بارگذاری سفارش‌ها...',
  
  // Empty states
  noProductsFound: 'هیچ محصولی یافت نشد',
  noCategoriesFound: 'هیچ دسته‌بندی یافت نشد',
  noOrdersFound: 'هیچ سفارشی یافت نشد',
  noProductsAvailable: 'هنوز محصولی موجود نیست',
  
  // Navigation
  home: 'خانه',
  back: 'بازگشت',
  tryAgain: 'دوباره تلاش کنید'
};

export const getTranslation = (key) => {
  return persianTranslations[key] || key;
};
