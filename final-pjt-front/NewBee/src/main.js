import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
// Bootstrap sass -> custom.css 적용
import '/css/custom.css'
import { useKakao } from 'vue3-kakao-maps/@utils'

const app = createApp(App)
// Kakao Map API는 차후 환경변수로 관리할 예정
useKakao('cff4f8a7ef45294fc4076aba8fc58f0d', ['clusterer', 'services', 'drawing'])

app.use(createPinia())
app.use(router)

app.mount('#app')
