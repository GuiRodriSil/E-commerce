<template>
  <Teleport to="body">
    <div
      v-if="cart.confirmationOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 p-4 backdrop-blur-sm"
      role="presentation"
      @click.self="cart.closeConfirmation"
    >
      <section
        class="w-full max-w-md rounded-3xl bg-white p-6 shadow-2xl"
        role="dialog"
        aria-modal="true"
        aria-labelledby="cart-confirmation-title"
      >
        <div class="flex items-start justify-between gap-4">
          <div>
            <p class="text-sm font-medium uppercase tracking-[0.2em] text-emerald-600">Adicionado com sucesso</p>
            <h2 id="cart-confirmation-title" class="mt-2 text-2xl font-black text-slate-900">Produto no carrinho</h2>
          </div>
          <button
            type="button"
            aria-label="Fechar confirmação"
            class="flex h-9 w-9 items-center justify-center rounded-full text-xl text-slate-400 hover:bg-slate-100 hover:text-slate-700"
            @click="cart.closeConfirmation"
          >
            ×
          </button>
        </div>

        <div v-if="cart.confirmationProduct" class="mt-6 flex items-center gap-4 rounded-2xl bg-slate-50 p-3">
          <img
            :src="cart.confirmationProduct.image"
            :alt="cart.confirmationProduct.name"
            class="h-20 w-20 rounded-xl object-cover"
          />
          <div>
            <h3 class="font-bold text-slate-900">{{ cart.confirmationProduct.name }}</h3>
            <p class="mt-1 text-sm text-slate-500">R$ {{ Number(cart.confirmationProduct.price).toFixed(2) }}</p>
          </div>
        </div>

        <div class="mt-6 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
          <button
            type="button"
            class="rounded-full border border-slate-200 px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
            @click="cart.closeConfirmation"
          >
            Continuar Comprando
          </button>
          <button
            type="button"
            class="rounded-full bg-slate-900 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-700"
            @click="goToCart"
          >
            Ir ao Carrinho
          </button>
        </div>
      </section>
    </div>
  </Teleport>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useCartStore } from '../stores/cartStore'

const router = useRouter()
const cart = useCartStore()

const goToCart = () => {
  cart.closeConfirmation()
  router.push('/cart')
}
</script>