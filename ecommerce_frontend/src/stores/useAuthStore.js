import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

const API_URL = 'http://localhost:8000'
const TOKEN_KEY = 'ecommerce_token'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || '')
  const user = ref(null)
  const loading = ref(false)
  const error = ref('')

  const isAuthenticated = computed(() => Boolean(token.value && user.value))

  const request = async (path, options = {}) => {
    const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) }
    if (token.value) headers.Authorization = `Bearer ${token.value}`

    const response = await fetch(`${API_URL}${path}`, { ...options, headers })
    const data = await response.json().catch(() => ({}))
    if (!response.ok) throw new Error(data.detail || 'Não foi possível concluir a operação.')
    return data
  }

  const saveSession = async (accessToken) => {
    token.value = accessToken
    localStorage.setItem(TOKEN_KEY, accessToken)
    await fetchProfile()
  }

  const login = async (credentials) => {
    loading.value = true
    error.value = ''
    try {
      const data = await request('/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      })
      await saveSession(data.access_token)
      return user.value
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      loading.value = false
    }
  }

  const register = async (details) => {
    loading.value = true
    error.value = ''
    try {
      const data = await request('/register', {
        method: 'POST',
        body: JSON.stringify(details),
      })
      await saveSession(data.access_token)
      return user.value
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      loading.value = false
    }
  }

  const fetchProfile = async () => {
    if (!token.value) return null
    try {
      user.value = await request('/users/me')
      return user.value
    } catch (requestError) {
      logout()
      throw requestError
    }
  }

  const updateProfile = async (details) => {
    loading.value = true
    error.value = ''
    try {
      user.value = await request('/users/me', {
        method: 'PUT',
        body: JSON.stringify(details),
      })
      return user.value
    } catch (requestError) {
      error.value = requestError.message
      throw requestError
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem(TOKEN_KEY)
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    fetchProfile,
    updateProfile,
    logout,
  }
})
