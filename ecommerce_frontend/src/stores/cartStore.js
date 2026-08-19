import { defineStore } from 'pinia'
import { computed, ref, watch } from 'vue'

const STORAGE_KEY = 'ecommerce-cart'

export const useCartStore = defineStore('cart', () => {
  const items = ref(JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'))

  const itemCount = computed(() =>
    items.value.reduce((total, item) => total + item.quantity, 0),
  )

  const total = computed(() =>
    items.value.reduce((sum, item) => sum + item.price * item.quantity, 0),
  )

  watch(
    items,
    (value) => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(value))
    },
    { deep: true },
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
