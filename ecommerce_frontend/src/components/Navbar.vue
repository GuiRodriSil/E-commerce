<template>
  <header class="sticky top-0 z-40 border-b border-slate-200 bg-white/90 backdrop-blur-md">
    <div class="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
      <router-link to="/" class="flex items-center gap-3">
        <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-900 text-lg font-bold text-white">
          E
        </div>
        <div>
          <p class="text-lg font-bold tracking-tight text-slate-900">Ecommerce</p>
          <p class="text-xs text-slate-500">Marketplace</p>
        </div>
      </router-link>

      <div class="hidden flex-1 items-center justify-center px-8 md:flex">
        <label class="flex w-full max-w-xl items-center gap-3 rounded-full border border-slate-200 bg-slate-50 px-4 py-2.5 shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35m1.85-5.15a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            v-model="search"
            type="text"
            placeholder="Buscar produtos..."
            class="w-full border-0 bg-transparent text-sm text-slate-700 placeholder:text-slate-400 focus:outline-none"
          />
        </label>
      </div>

      <router-link
        to="/cart"
        class="relative flex items-center justify-center rounded-full border border-slate-200 bg-slate-50 p-3 text-slate-700 shadow-sm hover:bg-slate-100"
        aria-label="Ir para o carrinho"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-1.5 7M17 13l1.5 7M9 20a1 1 0 100 2 1 1 0 000-2zm8 0a1 1 0 100 2 1 1 0 000-2z" />
        </svg>
        <span class="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-orange-500 text-[10px] font-bold text-white">
          {{ cartStore.itemCount }}
        </span>
      </router-link>
    </div>
  </header>
</template>

<script setup>
import { onBeforeUnmount, ref, watch } from 'vue'
import { useCartStore } from '../stores/cartStore'

const emit = defineEmits(['search-change'])
const search = ref('')
const cartStore = useCartStore()
let searchTimer

watch(search, (value) => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => emit('search-change', value.trim()), 350)
})

onBeforeUnmount(() => clearTimeout(searchTimer))
</script>
