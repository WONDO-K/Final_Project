import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
// Bootstrap sass -> custom.css 적용
import '/css/custom.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import { useKakao } from 'vue3-kakao-maps/@utils'


const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const KakaoApiKey = import.meta.env.VITE_APP_KAKAO_API_KEY
useKakao(KakaoApiKey, ['clusterer', 'services', 'drawing'])

app.use(pinia)
app.use(router)

app.mount('#app')
