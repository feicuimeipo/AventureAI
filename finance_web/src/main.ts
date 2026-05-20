import { createApp } from 'vue'
import App from './App.vue'
import '@/styles/bootstrap.css';
import "@/styles/tailwind.css";
import '@/styles/index.css';
import router from "@/router";
import { createPinia } from 'pinia'
const pinia = createPinia()
import i18n from './i18n'
//导入进度条插件
import 'nprogress/nprogress.css'


const app = createApp(App)
app.use(router)
app.use(pinia)
app.use(i18n)
app.mount('#app')
