import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

const STORAGE_KEY = 'ecommerce-wishlist'

const readFavorites = () => {
  try {
    const storedFavorites = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
    return Array.isArray(storedFavorites) ? storedFavorites : []
  } catch {
    return []
  }
}

export const useWishlistStore = defineStore('wishlist', () => {
  const favorites = ref(readFavorites())

  watch(
    favorites,
    (value) => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(value))
    },
    { deep: true },
  )

  const getProductId = (productOrId) =>
    typeof productOrId === 'object' ? productOrId?.id : productOrId

  function isFavorite(productOrId) {
    const productId = getProductId(productOrId)
    return favorites.value.some((product) => product.id === productId)
  }

  function toggleFavorite(product) {
    const productId = getProductId(product)
    const favoriteIndex = favorites.value.findIndex((item) => item.id === productId)

    if (favoriteIndex >= 0) {
      favorites.value.splice(favoriteIndex, 1)
      return false
    }

    favorites.value.push(product)
    return true
  }

  return {
    favorites,
    isFavorite,
    toggleFavorite,
  }
})