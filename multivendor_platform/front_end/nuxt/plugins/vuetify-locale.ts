export default defineNuxtPlugin((nuxtApp) => {
  // Extend Persian locale with missing translations
  const vuetifyLocale = {
    input: {
      appendAction: 'عملیات اضافی',
      prependAction: 'عملیات اولیه',
      clear: 'پاک کردن',
      otp: 'لطفاً کد OTP خود را وارد کنید'
    },
    close: 'بستن',
    loading: 'در حال بارگذاری...',
    dataIterator: {
      noResultsText: 'نتیجه‌ای یافت نشد',
      loadingText: 'در حال بارگذاری...'
    },
    dataTable: {
      itemsPerPageText: 'ردیف در هر صفحه:',
      ariaLabel: {
        sortDescending: 'مرتب‌سازی نزولی',
        sortAscending: 'مرتب‌سازی صعودی',
        sortNone: 'بدون مرتب‌سازی',
        activateNone: 'غیرفعال کردن مرتب‌سازی',
        activateDescending: 'فعال کردن مرتب‌سازی نزولی',
        activateAscending: 'فعال کردن مرتب‌سازی صعودی'
      },
      sortBy: 'مرتب‌سازی بر اساس'
    },
    dataFooter: {
      itemsPerPageText: 'ردیف در هر صفحه:',
      itemsPerPageAll: 'همه',
      nextPage: 'صفحه بعد',
      prevPage: 'صفحه قبل',
      firstPage: 'صفحه اول',
      lastPage: 'صفحه آخر',
      pageText: '{0}-{1} از {2}'
    },
    dateRangeInput: {
      divider: 'تا'
    },
    datePicker: {
      itemsSelected: '{0} انتخاب شده',
      range: {
        title: 'تاریخ‌ها را انتخاب کنید',
        header: 'تاریخ‌ها را وارد کنید'
      },
      title: 'تاریخ را انتخاب کنید',
      header: 'تاریخ را وارد کنید',
      input: {
        placeholder: 'تاریخ را وارد کنید'
      }
    },
    noDataText: 'داده‌ای موجود نیست',
    carousel: {
      prev: 'اسلاید قبلی',
      next: 'اسلاید بعدی',
      ariaLabel: {
        delimiter: 'اسلاید {0} از {1}'
      }
    },
    calendar: {
      moreEvents: '{0} مورد دیگر',
      today: 'امروز'
    },
    fileInput: {
      counter: '{0} فایل',
      counterSize: '{0} فایل ({1} در کل)'
    },
    timePicker: {
      am: 'قبل از ظهر',
      pm: 'بعد از ظهر',
      title: 'زمان را انتخاب کنید'
    },
    pagination: {
      ariaLabel: {
        root: 'صفحه‌بندی',
        first: 'صفحه اول',
        previous: 'صفحه قبل',
        next: 'صفحه بعد',
        last: 'صفحه آخر',
        page: 'رفتن به صفحه {0}',
        currentPage: 'صفحه فعلی، صفحه {0}',
        wrapper: 'صفحه‌بندی'
      }
    },
    stepper: {
      next: 'بعدی',
      prev: 'قبلی'
    },
    rating: {
      ariaLabel: {
        item: 'امتیاز {0} از {1}'
      }
    },
    infiniteScroll: {
      loadMore: 'بارگذاری بیشتر',
      empty: 'داده‌ای موجود نیست'
    }
  }

  // Merge with Vuetify's locale
  if (nuxtApp.$vuetify?.locale) {
    nuxtApp.$vuetify.locale.messages.value.fa = {
      ...nuxtApp.$vuetify.locale.messages.value.fa,
      $vuetify: vuetifyLocale
    }
  }
})

