import './assets/fonts.css'
import './assets/main.css'

import { createApp } from 'vue'
import pinia from './stores'

import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import i18n from './i18n'

const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(vuetify)
app.use(i18n)

app.mount('#app')
