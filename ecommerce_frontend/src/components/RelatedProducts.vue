<template>
  <section class="mt-12">
    <div class="mb-6">
      <p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">Você também pode gostar</p>
      <h2 class="mt-1 text-3xl font-black text-slate-900">Produtos relacionados</h2>
    </div>

    <p v-if="loading" class="rounded-3xl border border-slate-200 bg-white p-8 text-center text-sm text-slate-500 shadow-soft">
      Carregando produtos relacionados...
    </p>
    <p v-else-if="error" class="rounded-3xl border border-red-100 bg-red-50 p-8 text-center text-sm text-red-700">
      Não foi possível carregar os produtos relacionados.
    </p>
    <p v-else-if="!relatedProducts.length" class="rounded-3xl border border-dashed border-slate-300 bg-white p-8 text-center text-sm text-slate-500 shadow-soft">
      Nenhum produto relacionado encontrado.
    </p>

    <div v-else class="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
      <article v-for="relatedProduct in relatedProducts" :key="relatedProduct.id" class="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-soft">
        <div class="relative aspect-[4/3] overflow-hidden bg-slate-100">
          <router-link :to="`/product/${relatedProduct.id}`" :aria-label="`Ver detalhes de ${relatedProduct.name}`" class="block h-full">
            <img :src="relatedProduct.image" :alt="relatedProduct.name" class="h-full w-full object-cover transition duration-500 hover:scale-105" />
          </router-link>
          <button
            type="button"
            :aria-label="wishlist.isFavorite(relatedProduct) ? `Remover ${relatedProduct.name} dos favoritos` : `Adicionar ${relatedProduct.name} aos favoritos`"
            :aria-pressed="wishlist.isFavorite(relatedProduct)"
            :class="wishlist.isFavorite(relatedProduct) ? 'bg-rose-500 text-white' : 'bg-white/90 text-slate-700 hover:bg-white'"
            class="absolute right-3 top-3 flex h-10 w-10 items-center justify-center rounded-full text-2xl shadow-md hover:scale-105"
            @click="wishlist.toggleFavorite(relatedProduct)"
          >
            {{ wishlist.isFavorite(relatedProduct) ? '♥' : '♡' }}
          </button>
        </div>

        <div class="space-y-4 p-4">
          <h3 class="truncate text-lg font-bold text-slate-900">{{ relatedProduct.name }}</h3>
          <div>
            <span v-if="relatedProduct.originalPrice" class="mr-2 text-sm text-slate-400 line-through">R$ {{ Number(relatedProduct.originalPrice).toFixed(2) }}</span>
            <span v-if="relatedProduct.offer" class="rounded-full bg-orange-100 px-2 py-1 text-[10px] font-bold uppercase tracking-widest text-orange-700">Oferta</span>
            <p class="mt-1 text-xl font-black text-slate-900">R$ {{ Number(relatedProduct.price).toFixed(2) }}</p>
          </div>
          <router-link
            :to="`/product/${relatedProduct.id}`"
            class="block rounded-full bg-slate-900 px-4 py-2.5 text-center text-sm font-semibold text-white hover:bg-slate-700"
          >
            Ver produto
          </router-link>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import { onBeforeUnmount, ref, watch } from 'vue'
import { useWishlistStore } from '../stores/useWishlistStore'
import { withOfferDetails } from '../data/products'

const props = defineProps({
  productId: {
    type: [Number, String],
    required: true,
  },
})

const wishlist = useWishlistStore()
const relatedProducts = ref([])
const loading = ref(false)
const error = ref(false)
let controller

const loadRelatedProducts = async (productId) => {
  controller?.abort()
  const requestController = new AbortController()
  controller = requestController
  loading.value = true
  error.value = false

  try {
    const response = await fetch(`http://localhost:8000/products/${productId}/related`, { signal: requestController.signal })
    if (!response.ok) throw new Error('Falha ao carregar produtos relacionados')

    const products = await response.json()
    relatedProducts.value = products.map((product) => withOfferDetails({
      ...product,
      image: product.image || product.image_url || '',
    }))
  } catch (requestError) {
    if (requestError.name !== 'AbortError') {
      relatedProducts.value = []
      error.value = true
    }
  } finally {
    if (!requestController.signal.aborted) loading.value = false
  }
}

watch(() => props.productId, loadRelatedProducts, { immediate: true })

onBeforeUnmount(() => controller?.abort())
</script>