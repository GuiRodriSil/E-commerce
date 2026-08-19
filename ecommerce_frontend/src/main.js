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
import ProfilePage from './pages/ProfilePage.vue'
import SupportPage from './pages/SupportPage.vue'
import WishlistPage from './pages/WishlistPage.vue'
import { useAuthStore } from './stores/useAuthStore'

const savedTheme = localStorage.getItem('ecommerce-theme')
document.documentElement.classList.toggle('dark', savedTheme === 'dark')

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/home', component: HomePage },
  { path: '/product/:id', component: ProductDetailPage, props: true },
  { path: '/checkout', component: CheckoutPage },
  { path: '/cart', component: CartPage },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/profile', component: ProfilePage },
  { path: '/wishlist', component: WishlistPage },
  { path: '/support', component: SupportPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  },
})

router.beforeEach((to) => {
  if (to.path === '/checkout' && !localStorage.getItem('ecommerce_token')) {
    return { path: '/login', query: { redirect: '/checkout' } }
  }
})

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router)

const authStore = useAuthStore(pinia)
if (authStore.token) {
  authStore.fetchProfile().catch(() => {})
}

app.mount('#app')
