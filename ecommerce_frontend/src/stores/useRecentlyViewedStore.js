import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

const STORAGE_KEY = 'ecommerce-recently-viewed'
const MAX_ITEMS = 6

const readRecentlyViewed = () => {
  try {
    const storedProducts = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
    return Array.isArray(storedProducts) ? storedProducts.slice(0, MAX_ITEMS) : []
  } catch {
    return []
  }
}

export const useRecentlyViewedStore = defineStore('recentlyViewed', () => {
  const products = ref(readRecentlyViewed())

  watch(
    products,
    (value) => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(value))
    },
    { deep: true },
  )

  function addProduct(product) {
    products.value = [
      product,
      ...products.value.filter((item) => item.id !== product.id),
    ].slice(0, MAX_ITEMS)
  }

  function clearHistory() {
    products.value = []
    localStorage.removeItem(STORAGE_KEY)
  }

  return {
    products,
    addProduct,
    clearHistory,
  }
})