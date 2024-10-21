import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'  // 引入Element Plus 所需
import 'element-plus/dist/index.css'  // 引入Element Plus 所需
import router from './router'; // 引入路由
import * as ElementPlusIconsVue from '@element-plus/icons-vue'  // 引入Element Plus icon 所需
import './assets/main.css'
import axios from './axios'; // 引入自定义的 Axios 实例
import 'uno.css'

const app = createApp(App)

// 将 Axios 实例挂载到 Vue 原型上
app.config.globalProperties.$axios = axios; // 注意这一行

// 引入Element Plus icon 所需
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(router)
app.use(ElementPlus)  // 引入Element Plus 所需
app.mount('#app')
