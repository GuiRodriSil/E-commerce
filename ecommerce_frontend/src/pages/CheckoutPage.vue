<template>
  <div class="min-h-screen bg-slate-100">
    <Navbar />

    <main class="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
      <div class="mb-8">
        <p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">Checkout</p>
        <h1 class="mt-2 text-3xl font-black text-slate-900">Pagamento com PIX</h1>
      </div>

      <div v-if="cart.items.length === 0" class="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center shadow-soft">
        <p class="text-xl font-semibold text-slate-700">Seu carrinho está vazio.</p>
        <router-link to="/" class="mt-4 inline-block rounded-full bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white hover:bg-slate-700">
          Voltar às compras
        </router-link>
      </div>

      <div v-else class="grid gap-8 lg:grid-cols-[1.3fr_0.7fr]">
        <section class="space-y-4">
          <div v-for="item in cart.items" :key="item.id" class="flex items-center gap-4 rounded-3xl border border-slate-200 bg-white p-4 shadow-soft">
            <img :src="item.image" :alt="item.name" class="h-20 w-20 rounded-2xl object-cover" />
            <div class="flex-1">
              <h2 class="text-lg font-bold text-slate-900">{{ item.name }}</h2>
              <p class="text-sm text-slate-500">R$ {{ item.price.toFixed(2) }} cada</p>
            </div>

            <div class="flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-2 py-1">
              <button @click="cart.updateQuantity(item.id, item.quantity - 1)" class="h-8 w-8 rounded-full text-lg text-slate-700 hover:bg-slate-200">−</button>
              <span class="min-w-6 text-center text-sm font-semibold text-slate-900">{{ item.quantity }}</span>
              <button @click="cart.updateQuantity(item.id, item.quantity + 1)" class="h-8 w-8 rounded-full text-lg text-slate-700 hover:bg-slate-200">+</button>
            </div>

            <button @click="cart.removeItem(item.id)" class="ml-2 text-sm font-medium text-red-600 hover:text-red-700">Remover</button>
          </div>
        </section>

        <aside class="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft">
          <h2 class="text-xl font-bold text-slate-900">Resumo</h2>

          <div class="mt-6 space-y-3 text-sm text-slate-600">
            <div class="flex justify-between">
              <span>Subtotal</span>
              <span>R$ {{ cart.total.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between">
              <span>Frete</span>
              <span>Grátis</span>
            </div>
            <div class="flex justify-between border-t border-slate-200 pt-3 text-base font-bold text-slate-900">
              <span>Total</span>
              <span>R$ {{ cart.total.toFixed(2) }}</span>
            </div>
          </div>

          <button
            @click="createPixPayment"
            :disabled="loading"
            class="mt-6 w-full rounded-full bg-emerald-600 px-5 py-3 text-sm font-semibold text-white hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {{ loading ? 'Gerando PIX...' : 'Pagar com PIX' }}
          </button>
        </aside>
      </div>

      <div v-if="pixData" class="mt-10 rounded-3xl border border-emerald-200 bg-emerald-50 p-6 shadow-soft">
        <h2 class="text-2xl font-bold text-emerald-900">Pagamento PIX gerado</h2>
        <p class="mt-2 text-sm text-emerald-700">Pagamento ID: {{ pixData.payment_id }}</p>
        <p class="mt-4 text-lg font-semibold text-slate-900">Valor: R$ {{ pixData.transaction_amount.toFixed(2) }}</p>

        <div class="mt-6 flex flex-col items-center gap-4 md:flex-row md:items-start">
          <img v-if="pixData.qr_code_base64" :src="`data:image/png;base64,${pixData.qr_code_base64}`" alt="QR Code PIX" class="h-52 w-52 rounded-2xl bg-white p-3 shadow-sm" />
          <div class="flex-1 rounded-2xl bg-white p-4 shadow-sm">
            <p class="text-sm font-medium text-slate-500">Código PIX</p>
            <textarea readonly class="mt-2 h-32 w-full resize-none rounded-xl border border-slate-200 bg-slate-50 p-3 text-xs text-slate-700" :value="pixData.qr_code"></textarea>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navbar from '../components/Navbar.vue'
import { useCartStore } from '../stores/cartStore'

const cart = useCartStore()
const loading = ref(false)
const pixData = ref(null)

const createPixPayment = async () => {
  if (!cart.items.length) return

  loading.value = true

  try {
    const payload = {
      payer_email: 'comprador@email.com',
      items: cart.items.map((item) => ({
        id: item.id,
        title: item.name,
        quantity: item.quantity,
        unit_price: item.price,
      })),
    }

    const response = await fetch('http://localhost:8000/payments/mercadopago/pix', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao gerar PIX')
    }

    pixData.value = await response.json()
  } catch (error) {
    alert(error.message)
  } finally {
    loading.value = false
  }
}
</script>
