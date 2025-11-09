import { createHead } from '@unhead/vue/client'

const head = createHead()

head.push({
  titleTemplate: (title) =>
    title ? `${title} | ایندکسو` : 'ایندکسو | بازارچه آنلاین تامین‌کنندگان صنعتی',
  htmlAttrs: {
    lang: 'fa',
    dir: 'rtl'
  },
  meta: [
    {
      key: 'description',
      name: 'description',
      content: 'ایندکسو، پلتفرم چندفروشنده برای خرید و فروش ماشین‌آلات صنعتی با تمرکز بر تامین‌کنندگان معتبر و تجربه کاربری فارسی و راست‌چین.'
    },
    {
      key: 'og:locale',
      property: 'og:locale',
      content: 'fa_IR'
    },
    {
      key: 'keywords',
      name: 'keywords',
      content: 'ایندکسو, پلتفرم چندفروشنده, ماشین‌آلات صنعتی, تامین‌کننده, خرید و فروش, صنعت, ایران'
    }
  ]
})

export default head

