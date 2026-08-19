<template>
  <Teleport to="body">
    <div v-if="open" class="fixed inset-0 z-50 bg-slate-950/40" @click.self="close">
      <aside class="ml-auto flex h-full w-full max-w-md flex-col bg-white shadow-2xl" aria-label="Drawer do carrinho">
        <div class="flex items-center justify-between border-b border-slate-200 px-5 py-4">
          <div>
            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Seu carrinho</p>
            <h2 class="mt-1 text-2xl font-black text-slate-900">{{ cart.itemCount }} itens</h2>
          </div>
          <button type="button" aria-label="Fechar carrinho" class="flex h-10 w-10 items-center justify-center rounded-full text-2xl text-slate-400 hover:bg-slate-100 hover:text-slate-700" @click="close">
            ×
          </button>
        </div>

        <div v-if="!cart.items.length" class="flex flex-1 items-center justify-center p-8 text-center">
          <div>
            <p class="text-lg font-semibold text-slate-700">Seu carrinho está vazio.</p>
            <button type="button" class="mt-4 rounded-full bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white hover:bg-slate-700" @click="close">
              Continuar comprando
            </button>
          </div>
        </div>

        <div v-else class="flex-1 divide-y divide-slate-200 overflow-y-auto px-5">
          <div v-for="item in cart.items" :key="item.id" class="flex items-center gap-3 py-4">
            <router-link :to="`/product/${item.id}`" :aria-label="`Ver detalhes de ${item.name}`" @click="close">
              <img :src="item.image" :alt="item.name" class="h-16 w-16 rounded-xl object-cover transition hover:scale-105" />
            </router-link>
            <div class="min-w-0 flex-1">
              <router-link :to="`/product/${item.id}`" class="block truncate font-semibold text-slate-900 hover:text-slate-600" @click="close">
                {{ item.name }}
              </router-link>
              <p class="mt-1 text-sm text-slate-500">{{ item.quantity }} × R$ {{ Number(item.price).toFixed(2) }}</p>
            </div>
          </div>
        </div>

        <div class="border-t border-slate-200 p-5">
          <div class="mb-4 flex items-center justify-between text-lg font-black text-slate-900">
            <span>Total</span>
            <span>R$ {{ cart.total.toFixed(2) }}</span>
          </div>
          <router-link to="/cart" class="block rounded-full bg-slate-900 px-5 py-3 text-center text-sm font-semibold text-white hover:bg-slate-700" @click="close">
            Ver carrinho completo
          </router-link>
        </div>
      </aside>
    </div>
  </Teleport>
</template>

<script setup>
import { useCartStore } from '../stores/cartStore'

defineProps({
  open: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close'])
const cart = useCartStore()
const close = () => emit('close')
</script>