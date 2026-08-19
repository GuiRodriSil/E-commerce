<template>
  <div>
    <Navbar @search-change="handleSearch" />

    <main class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <section class="mb-10 overflow-hidden rounded-3xl bg-gradient-to-r from-slate-900 via-slate-800 to-slate-700 p-8 text-white shadow-soft">
        <div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div class="max-w-xl">
            <span class="mb-3 inline-flex rounded-full bg-white/10 px-3 py-1 text-xs font-medium uppercase tracking-[0.2em] text-slate-200">
              Novo lançamento
            </span>
            <h1 class="text-4xl font-black tracking-tight sm:text-5xl">Seu próximo favorito está aqui.</h1>
            <p class="mt-4 text-base text-slate-200 sm:text-lg">
              Produtos premium para casa, trabalho e estilo de vida — com entrega expressa e qualidade premium.
            </p>
          </div>

          <div class="rounded-2xl bg-white/10 p-5 backdrop-blur-sm ring-1 ring-white/10">
            <p class="text-sm uppercase tracking-[0.2em] text-slate-300">Oferta do dia</p>
            <p class="mt-2 text-3xl font-black">até 40% off</p>
            <button @click="toggleOffers" class="mt-4 rounded-full bg-white px-5 py-2.5 text-sm font-semibold text-slate-900 hover:bg-slate-100">
              {{ showOffers ? 'Ver todos os produtos' : 'Ver ofertas' }}
            </button>
          </div>
        </div>
      </section>

      <BenefitsBanner />

      <section v-if="recentlyViewedStore.products.length" class="mb-12">
        <div class="mb-5 flex items-center justify-between gap-4">
          <div>
            <p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">Continue de onde parou</p>
            <h2 class="mt-1 text-3xl font-bold text-slate-900">Vistos Recentemente</h2>
          </div>
          <div class="flex items-center gap-2">
            <button
              type="button"
              class="rounded-full border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-600 shadow-sm hover:bg-slate-50"
              @click="clearRecentlyViewed"
            >
              Limpar histórico
            </button>
            <button
              type="button"
              aria-label="Ver produtos anteriores"
              class="flex h-10 w-10 items-center justify-center rounded-full border border-slate-200 bg-white text-lg text-slate-700 shadow-sm hover:bg-slate-50"
              @click="scrollRecentProducts(-1)"
            >
              ←
            </button>
            <button
              type="button"
              aria-label="Ver próximos produtos"
              class="flex h-10 w-10 items-center justify-center rounded-full border border-slate-200 bg-white text-lg text-slate-700 shadow-sm hover:bg-slate-50"
              @click="scrollRecentProducts(1)"
            >
              →
            </button>
          </div>
        </div>

        <div ref="recentProductsCarousel" class="flex snap-x gap-5 overflow-x-auto pb-3 scrollbar-hide">
          <router-link
            v-for="product in recentlyViewedStore.products"
            :key="product.id"
            :to="`/product/${product.id}`"
            class="group min-w-[260px] snap-start overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-soft sm:min-w-[300px]"
          >
            <div class="aspect-[16/10] overflow-hidden bg-slate-100">
              <img :src="product.image" :alt="product.name" class="h-full w-full object-cover transition duration-500 group-hover:scale-105" />
            </div>
            <div class="p-4">
              <h3 class="truncate font-bold text-slate-900">{{ product.name }}</h3>
              <span v-if="product.originalPrice" class="mr-2 text-sm text-slate-400 line-through">R$ {{ Number(product.originalPrice).toFixed(2) }}</span>
              <span v-if="product.offer" class="rounded-full bg-orange-100 px-2 py-1 text-[10px] font-bold uppercase tracking-widest text-orange-700">Oferta</span>
              <p class="mt-2 text-lg font-black text-slate-900">R$ {{ Number(product.price).toFixed(2) }}</p>
            </div>
          </router-link>
        </div>
      </section>

      <section ref="productsSection">
        <div class="mb-6 flex items-center justify-between">
          <div>
            <p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">Catalogo</p>
            <h2 class="text-3xl font-bold text-slate-900">{{ showOffers ? 'Ofertas em destaque' : 'Produtos em destaque' }}</h2>
          </div>
          <div class="flex flex-wrap items-center justify-end gap-3">
            <select v-model="selectedCategory" class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 outline-none hover:border-slate-300">
              <option value="">Todas as categorias</option>
              <option v-for="category in categories" :key="category.value" :value="category.value">{{ category.label }}</option>
            </select>
            <button v-if="showOffers" @click="showAllProducts" class="rounded-full border border-orange-200 bg-orange-50 px-4 py-2 text-sm font-semibold text-orange-700 hover:bg-orange-100">
              Mostrar todos
            </button>
          </div>
        </div>

        <p v-if="loading" class="py-10 text-center text-sm text-slate-500">Carregando produtos...</p>
        <p v-else-if="!visibleProducts.length" class="py-10 text-center text-sm text-slate-500">Nenhum produto encontrado.</p>

        <div v-else class="grid gap-8 sm:grid-cols-2 xl:grid-cols-3">
          <article v-for="product in visibleProducts" :key="product.id" class="group overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-soft">
            <div class="relative aspect-[4/3] overflow-hidden bg-slate-100">
              <router-link :to="`/product/${product.id}`" :aria-label="`Ver detalhes de ${product.name}`" class="block h-full">
                <img
                  :src="product.image"
                  :alt="product.name"
                  class="h-full w-full object-cover transition duration-500 group-hover:scale-105"
                />
              </router-link>
              <button
                type="button"
                :aria-label="wishlistStore.isFavorite(product) ? `Remover ${product.name} dos favoritos` : `Adicionar ${product.name} aos favoritos`"
                :aria-pressed="wishlistStore.isFavorite(product)"
                :class="wishlistStore.isFavorite(product) ? 'bg-rose-500 text-white' : 'bg-white/90 text-slate-700 hover:bg-white'"
                class="absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-full text-2xl shadow-md transition hover:scale-105"
                @click="wishlistStore.toggleFavorite(product)"
              >
                {{ wishlistStore.isFavorite(product) ? '♥' : '♡' }}
              </button>
            </div>

            <div class="space-y-4 p-5">
              <div class="flex items-center justify-between gap-3">
                <span class="rounded-full bg-slate-100 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-widest text-slate-600">
                  {{ product.category }}
                </span>
                <span v-if="product.offer" class="rounded-full bg-orange-100 px-2.5 py-1 text-[10px] font-bold uppercase tracking-widest text-orange-700">Oferta</span>
                <span class="text-xs text-slate-500">{{ product.stock }} em estoque</span>
              </div>

              <div>
                <h3 class="text-xl font-bold text-slate-900">{{ product.name }}</h3>
                <p class="mt-2 line-clamp-2 text-sm text-slate-600">{{ product.description }}</p>
              </div>

              <div class="flex items-center justify-between">
                <div>
                  <span v-if="product.originalPrice" class="mr-2 text-sm text-slate-400 line-through">R$ {{ product.originalPrice.toFixed(2) }}</span>
                  <span class="text-2xl font-black text-slate-900">R$ {{ product.price.toFixed(2) }}</span>
                </div>
                <button
                  :disabled="!cartStore.canAddItem(product)"
                  @click="cartStore.addItem(product)"
                  class="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {{ cartStore.canAddItem(product) ? 'Adicionar' : 'Estoque máximo' }}
                </button>
              </div>

              <router-link :to="`/product/${product.id}`" class="inline-flex text-sm font-medium text-slate-700 hover:text-slate-900">
                Ver detalhes →
              </router-link>
            </div>
          </article>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import Navbar from '../components/Navbar.vue'
import BenefitsBanner from '../components/BenefitsBanner.vue'
import { useCartStore } from '../stores/cartStore'
import { useRecentlyViewedStore } from '../stores/useRecentlyViewedStore'
import { useWishlistStore } from '../stores/useWishlistStore'
import { products, withOfferDetails } from '../data/products'

const cartStore = useCartStore()
const recentlyViewedStore = useRecentlyViewedStore()
const wishlistStore = useWishlistStore()
const displayedProducts = ref(products)
const selectedCategory = ref('')
const currentSearch = ref('')
const loading = ref(false)
const showOffers = ref(false)
const productsSection = ref(null)
const recentProductsCarousel = ref(null)
const categories = [
  { label: 'Eletrônicos', value: 'Eletronicos' },
  { label: 'Áudio', value: 'Audio' },
  { label: 'Acessórios', value: 'Acessorios' },
  { label: 'Fotografia', value: 'Fotografia' },
  { label: 'Casa', value: 'Casa' },
]

const categoryLabels = Object.fromEntries(categories.map((category) => [category.value, category.label]))
const offerDetails = {
  ...Object.fromEntries(products.filter((product) => product.offer).map((product) => [product.name, product.originalPrice])),
  'Teclado Mecanico RGB': 399.9,
  'Caixa de Som Portatil': 299.9,
}

const normalizeProduct = (product) => ({
  ...withOfferDetails(product),
  category: categoryLabels[product.category?.name || product.category] || product.category?.name || product.category || 'Sem categoria',
  image: product.image || product.image_url || '',
  originalPrice: offerDetails[product.name] ?? product.originalPrice,
  offer: Boolean(offerDetails[product.name] ?? product.originalPrice),
})

const loadProducts = async () => {
  loading.value = true
  const params = new URLSearchParams()
  if (currentSearch.value) params.set('search', currentSearch.value)
  if (selectedCategory.value) params.set('category', selectedCategory.value)

  try {
    const response = await fetch(`http://localhost:8000/products?${params.toString()}`)
    if (!response.ok) throw new Error('Falha ao carregar produtos')
    displayedProducts.value = (await response.json()).map(normalizeProduct)
  } catch {
    const searchText = currentSearch.value.toLowerCase()
    displayedProducts.value = products.filter((product) => {
      const matchesSearch = !searchText || `${product.name} ${product.description}`.toLowerCase().includes(searchText)
      const selectedLabel = categoryLabels[selectedCategory.value]
      const matchesCategory = !selectedCategory.value || product.category === selectedLabel
      return matchesSearch && matchesCategory
    })
  } finally {
    loading.value = false
  }
}

const handleSearch = (value) => {
  currentSearch.value = value
}

const visibleProducts = computed(() => showOffers.value ? displayedProducts.value.filter((product) => product.offer) : displayedProducts.value)

const scrollRecentProducts = (direction) => {
  recentProductsCarousel.value?.scrollBy({ left: direction * 320, behavior: 'smooth' })
}

const clearRecentlyViewed = () => {
  recentlyViewedStore.clearHistory()
}

const showOffersAndScroll = () => {
  showOffers.value = true
  productsSection.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const showAllProducts = () => {
  showOffers.value = false
}

const toggleOffers = () => {
  if (showOffers.value) {
    showAllProducts()
    return
  }

  showOffersAndScroll()
}

watch([currentSearch, selectedCategory], loadProducts)
onMounted(loadProducts)
</script>
