import { createHead } from '@unhead/vue/client'

const head = createHead()

head.push({
  titleTemplate: (title) =>
    title ? `${title} | ایندکسو` : 'ایندکسو | خرید و فروش آسان ماشین‌آلات',
  htmlAttrs: {
    lang: 'fa',
    dir: 'rtl'
  },
  meta: [
    {
      key: 'description',
      name: 'description',
      content: 'ایندکسو: خرید و فروش آسان ماشین‌آلات و تجهیزات از بهترین تولیدکنندگان کشور. بدون واسطه و با اطمینان کامل.'
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

