import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
// Add the necessary CSS

import {createBootstrap} from 'bootstrap-vue-next'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'
import 'fomantic-ui-css/semantic.min.css'
import './assets/base.css'


const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(createBootstrap({components: true, directives: true}))

app.mount('#app')
