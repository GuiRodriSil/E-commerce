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
            <button class="mt-4 rounded-full bg-white px-5 py-2.5 text-sm font-semibold text-slate-900 hover:bg-slate-100">
              Ver ofertas
            </button>
          </div>
        </div>
      </section>

      <section>
        <div class="mb-6 flex items-center justify-between">
          <div>
            <p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">Catalogo</p>
            <h2 class="text-3xl font-bold text-slate-900">Produtos em destaque</h2>
          </div>
          <select v-model="selectedCategory" class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 outline-none hover:border-slate-300">
            <option value="">Todas as categorias</option>
            <option v-for="category in categories" :key="category.value" :value="category.value">{{ category.label }}</option>
          </select>
        </div>

        <p v-if="loading" class="py-10 text-center text-sm text-slate-500">Carregando produtos...</p>
        <p v-else-if="!displayedProducts.length" class="py-10 text-center text-sm text-slate-500">Nenhum produto encontrado.</p>

        <div v-else class="grid gap-8 sm:grid-cols-2 xl:grid-cols-3">
          <article v-for="product in displayedProducts" :key="product.id" class="group overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-soft">
            <div class="aspect-[4/3] overflow-hidden bg-slate-100">
              <img
                :src="product.image"
                :alt="product.name"
                class="h-full w-full object-cover transition duration-500 group-hover:scale-105"
              />
            </div>

            <div class="space-y-4 p-5">
              <div class="flex items-center justify-between gap-3">
                <span class="rounded-full bg-slate-100 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-widest text-slate-600">
                  {{ product.category }}
                </span>
                <span class="text-xs text-slate-500">{{ product.stock }} em estoque</span>
              </div>

              <div>
                <h3 class="text-xl font-bold text-slate-900">{{ product.name }}</h3>
                <p class="mt-2 line-clamp-2 text-sm text-slate-600">{{ product.description }}</p>
              </div>

              <div class="flex items-center justify-between">
                <span class="text-2xl font-black text-slate-900">R$ {{ product.price.toFixed(2) }}</span>
                <button
                  @click="cartStore.addItem(product)"
                  class="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-700"
                >
                  Adicionar
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
import { onMounted, ref, watch } from 'vue'
import Navbar from '../components/Navbar.vue'
import { useCartStore } from '../stores/cartStore'
import { products } from '../data/products'

const cartStore = useCartStore()
const displayedProducts = ref(products)
const selectedCategory = ref('')
const currentSearch = ref('')
const loading = ref(false)
const categories = [
  { label: 'Eletrônicos', value: 'Eletronicos' },
  { label: 'Áudio', value: 'Audio' },
  { label: 'Acessórios', value: 'Acessorios' },
  { label: 'Fotografia', value: 'Fotografia' },
  { label: 'Casa', value: 'Casa' },
]

const categoryLabels = Object.fromEntries(categories.map((category) => [category.value, category.label]))

const normalizeProduct = (product) => ({
  ...product,
  category: categoryLabels[product.category?.name || product.category] || product.category?.name || product.category || 'Sem categoria',
  image: product.image || product.image_url || '',
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

watch([currentSearch, selectedCategory], loadProducts)
onMounted(loadProducts)
</script>
