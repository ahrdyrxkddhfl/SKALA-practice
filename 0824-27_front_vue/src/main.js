import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

// [폴더 트리] 라우터 인스턴스 전역 주입
app.use(router)

app.mount('#app')
