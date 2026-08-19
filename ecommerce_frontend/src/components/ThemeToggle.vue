<template>
  <button
    type="button"
    class="flex h-11 w-11 items-center justify-center rounded-full border border-slate-200 bg-slate-50 text-lg text-slate-700 shadow-sm hover:bg-slate-100 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700"
    :aria-label="isDark ? 'Ativar modo claro' : 'Ativar modo escuro'"
    :aria-pressed="isDark"
    @click="toggleTheme"
  >
    <span aria-hidden="true">{{ isDark ? '☀' : '☾' }}</span>
  </button>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const STORAGE_KEY = 'ecommerce-theme'
const isDark = ref(false)

const applyTheme = (dark) => {
  isDark.value = dark
  document.documentElement.classList.toggle('dark', dark)
  localStorage.setItem(STORAGE_KEY, dark ? 'dark' : 'light')
}

const toggleTheme = () => applyTheme(!isDark.value)

onMounted(() => {
  applyTheme(localStorage.getItem(STORAGE_KEY) === 'dark')
})
</script>
