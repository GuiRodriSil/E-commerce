import { defineStore } from 'pinia'
import { computed, ref, watch } from 'vue'
import { useAuthStore } from './useAuthStore'

const STORAGE_KEY_PREFIX = 'ecommerce-cart-user-'
const LEGACY_STORAGE_KEY = 'ecommerce-cart'

const readCart = (userId) => {
  if (!userId) return []

  try {
    return JSON.parse(localStorage.getItem(`${STORAGE_KEY_PREFIX}${userId}`) || '[]')
  } catch {
    return []
  }
}

export const useCartStore = defineStore('cart', () => {
  const auth = useAuthStore()
  const items = ref([])

  localStorage.removeItem(LEGACY_STORAGE_KEY)

  const itemCount = computed(() =>
    items.value.reduce((total, item) => total + item.quantity, 0),
  )

  const total = computed(() =>
    items.value.reduce((sum, item) => sum + item.price * item.quantity, 0),
  )

  watch(
    items,
    (value) => {
      const userId = auth.user?.id
      if (userId) {
        localStorage.setItem(`${STORAGE_KEY_PREFIX}${userId}`, JSON.stringify(value))
      }
    },
    { deep: true },
  )

  watch(
    () => auth.user?.id,
    (userId) => {
      items.value = readCart(userId)
    },
    { immediate: true },
  )

  function addItem(product) {
    const existingItem = items.value.find((item) => item.id === product.id)

    if (existingItem) {
      existingItem.quantity += 1
      return
    }

    items.value.push({
      id: product.id,
      name: product.name,
      price: product.price,
      image: product.image,
      quantity: 1,
    })
  }

  function removeItem(productId) {
    items.value = items.value.filter((item) => item.id !== productId)
  }

  function updateQuantity(productId, quantity) {
    const item = items.value.find((item) => item.id === productId)

    if (!item) return

    if (quantity <= 0) {
      removeItem(productId)
      return
    }

    item.quantity = quantity
  }

  function clearCart() {
    items.value = []
  }

  return {
    items,
    itemCount,
    total,
    addItem,
    removeItem,
    updateQuantity,
    clearCart,
  }
})
