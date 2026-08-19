<template>
  <div>
    <Navbar />

    <main v-if="product" class="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
      <div class="mb-6 text-sm text-slate-500">
        <router-link to="/home" class="hover:text-slate-800">Home</router-link>
        <span class="mx-2">/</span>
        <span>{{ product.category }}</span>
      </div>

      <div class="grid gap-10 rounded-3xl border border-slate-200 bg-white p-6 shadow-soft lg:grid-cols-2 lg:p-8">
        <div class="overflow-hidden rounded-2xl bg-slate-100">
          <img :src="product.image" :alt="product.name" class="h-full w-full object-cover" />
        </div>

        <div class="flex flex-col justify-center">
          <span class="mb-3 inline-flex w-fit rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.15em] text-slate-600">
            {{ product.category }}
          </span>
          <h1 class="text-4xl font-black tracking-tight text-slate-900">{{ product.name }}</h1>

          <div class="mt-5 flex flex-wrap items-center gap-4">
            <span v-if="product.originalPrice" class="text-base text-slate-400 line-through">R$ {{ product.originalPrice.toFixed(2) }}</span>
            <span class="text-3xl font-black text-slate-900">R$ {{ product.price.toFixed(2) }}</span>
            <span v-if="product.offer" class="rounded-full bg-orange-100 px-2.5 py-1 text-xs font-semibold text-orange-700">Oferta</span>
            <span class="rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-semibold text-emerald-700">
              {{ product.stock }} em estoque
            </span>
          </div>

          <p class="mt-6 text-base leading-7 text-slate-600">{{ product.description }}</p>

          <div class="mt-8 flex flex-col gap-3 sm:flex-row">
            <button
              :disabled="!cartStore.canAddItem(product)"
              @click="cartStore.addItem(product)"
              class="flex-1 rounded-full bg-slate-900 px-6 py-3 text-sm font-semibold text-white hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {{ cartStore.canAddItem(product) ? 'Adicionar ao carrinho' : 'Estoque máximo' }}
            </button>
            <button class="rounded-full border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50">
              Comprar agora
            </button>
          </div>
        </div>
      </div>

      <RelatedProducts :product-id="product.id" />
    </main>

    <main v-else class="mx-auto max-w-6xl px-4 py-10 text-center">
      <p class="text-lg text-slate-500">Produto não encontrado.</p>
    </main>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from '../components/Navbar.vue'
import RelatedProducts from '../components/RelatedProducts.vue'
import { useCartStore } from '../stores/cartStore'
import { useRecentlyViewedStore } from '../stores/useRecentlyViewedStore'
import { products } from '../data/products'

const route = useRoute()
const cartStore = useCartStore()
const recentlyViewedStore = useRecentlyViewedStore()
const product = computed(() => products.find((item) => item.id === Number(route.params.id)))

watch(() => route.params.id, () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

watch(product, (visitedProduct) => {
  if (visitedProduct) recentlyViewedStore.addProduct(visitedProduct)
}, { immediate: true })
</script>
