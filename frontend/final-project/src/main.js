import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
// Bootstrap sass -> custom.css 적용
import '/css/custom.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
