import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'
import HomePage from './pages/HomePage.vue'
import ProductDetailPage from './pages/ProductDetailPage.vue'
import CheckoutPage from './pages/CheckoutPage.vue'
import CartPage from './pages/CartPage.vue'
import LoginPage from './pages/LoginPage.vue'
import RegisterPage from './pages/RegisterPage.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/product/:id', component: ProductDetailPage, props: true },
  { path: '/checkout', component: CheckoutPage },
  { path: '/cart', component: CartPage },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router)
app.mount('#app')
