import { defineStore } from 'pinia'
import { computed, ref, watch } from 'vue'
import { useAuthStore } from './useAuthStore'
import { products, withOfferDetails } from '../data/products'

const STORAGE_KEY_PREFIX = 'ecommerce-cart-user-'
const LEGACY_STORAGE_KEY = 'ecommerce-cart'

const hydrateCartItem = (item) => {
  const catalogProduct = products.find((product) => product.id === item.id)
  return {
    ...withOfferDetails(item),
    stock: item.stock ?? catalogProduct?.stock ?? 0,
  }
}

const readCart = (userId) => {
  if (!userId) return []

  try {
    return JSON.parse(localStorage.getItem(`${STORAGE_KEY_PREFIX}${userId}`) || '[]').map(hydrateCartItem)
  } catch {
    return []
  }
}

export const useCartStore = defineStore('cart', () => {
  const auth = useAuthStore()
  const items = ref([])
  const confirmationProduct = ref(null)
  const confirmationOpen = ref(false)

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
    const stock = Number(product.stock)

    if (!Number.isFinite(stock) || stock <= 0 || (existingItem && existingItem.quantity >= stock)) {
      return false
    }

    if (existingItem) {
      existingItem.stock = stock
      existingItem.quantity += 1
      confirmationProduct.value = product
      confirmationOpen.value = true
      return true
    }

    items.value.push({
      id: product.id,
      name: product.name,
      price: product.price,
      image: product.image,
      originalPrice: product.originalPrice,
      offer: product.offer,
      stock,
      quantity: 1,
    })
    confirmationProduct.value = product
    confirmationOpen.value = true
    return true
  }

  function closeConfirmation() {
    confirmationOpen.value = false
  }

  function canAddItem(product) {
    const existingItem = items.value.find((item) => item.id === product.id)
    const stock = Number(product.stock)
    return Number.isFinite(stock) && stock > 0 && (!existingItem || existingItem.quantity < stock)
  }

  function canIncrease(productId) {
    const item = items.value.find((cartItem) => cartItem.id === productId)
    return Boolean(item && item.quantity < item.stock)
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

    if (quantity > item.stock) return

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
    confirmationProduct,
    confirmationOpen,
    closeConfirmation,
    canAddItem,
    canIncrease,
    removeItem,
    updateQuantity,
    clearCart,
  }
})
