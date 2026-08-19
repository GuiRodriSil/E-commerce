<template>
  <div class="min-h-screen bg-slate-100">
    <Navbar />

    <main class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div class="mb-8 flex items-end justify-between gap-4">
        <div>
          <p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">Sua seleção</p>
          <h1 class="mt-2 text-3xl font-black text-slate-900">Favoritos</h1>
        </div>
        <span class="rounded-full bg-white px-4 py-2 text-sm font-semibold text-slate-600 shadow-sm">
          {{ wishlist.favorites.length }} {{ wishlist.favorites.length === 1 ? 'produto' : 'produtos' }}
        </span>
      </div>

      <section v-if="!wishlist.favorites.length" class="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center shadow-soft">
        <p class="text-xl font-semibold text-slate-700">Você ainda não tem favoritos.</p>
        <p class="mt-2 text-sm text-slate-500">Toque no coração dos produtos que deseja guardar.</p>
        <router-link to="/home" class="mt-6 inline-block rounded-full bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white hover:bg-slate-700">
          Explorar produtos
        </router-link>
      </section>

      <section v-else class="grid gap-8 sm:grid-cols-2 xl:grid-cols-3">
        <article v-for="product in favoriteProducts" :key="product.id" class="group overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-soft">
          <div class="relative aspect-[4/3] overflow-hidden bg-slate-100">
            <router-link :to="`/product/${product.id}`" :aria-label="`Ver detalhes de ${product.name}`" class="block h-full">
              <img :src="product.image" :alt="product.name" class="h-full w-full object-cover transition duration-500 group-hover:scale-105" />
            </router-link>
            <button
              type="button"
              :aria-label="`Remover ${product.name} dos favoritos`"
              class="absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-full bg-rose-500 text-2xl text-white shadow-md transition hover:scale-105"
              @click="wishlist.toggleFavorite(product)"
            >
              ♥
            </button>
          </div>

          <div class="space-y-4 p-5">
            <div>
              <h2 class="text-xl font-bold text-slate-900">{{ product.name }}</h2>
              <p class="mt-2 line-clamp-2 text-sm text-slate-600">{{ product.description }}</p>
            </div>

            <div class="flex items-center justify-between gap-3">
              <div>
                <span v-if="product.originalPrice" class="mr-2 text-sm text-slate-400 line-through">R$ {{ Number(product.originalPrice).toFixed(2) }}</span>
                <span v-if="product.offer" class="rounded-full bg-orange-100 px-2 py-1 text-[10px] font-bold uppercase tracking-widest text-orange-700">Oferta</span>
                <span class="mt-1 block text-2xl font-black text-slate-900">R$ {{ Number(product.price).toFixed(2) }}</span>
              </div>
              <button
                type="button"
                :disabled="!cart.canAddItem(product)"
                class="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
                @click="cart.addItem(product)"
              >
                {{ cart.canAddItem(product) ? 'Adicionar' : 'Estoque máximo' }}
              </button>
            </div>

            <router-link :to="`/product/${product.id}`" class="inline-flex text-sm font-medium text-slate-700 hover:text-slate-900">
              Ver detalhes →
            </router-link>
          </div>
        </article>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Navbar from '../components/Navbar.vue'
import { useCartStore } from '../stores/cartStore'
import { withOfferDetails } from '../data/products'
import { useWishlistStore } from '../stores/useWishlistStore'

const cart = useCartStore()
const wishlist = useWishlistStore()
const favoriteProducts = computed(() => wishlist.favorites.map(withOfferDetails))
</script>