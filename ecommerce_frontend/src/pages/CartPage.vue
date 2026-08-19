<template>
  <div class="min-h-screen bg-slate-100">
    <Navbar />

    <main class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div class="mb-8 flex items-center justify-between">
        <div>
          <p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">Carrinho</p>
          <h1 class="mt-2 text-3xl font-black text-slate-900">Seu pedido</h1>
        </div>
        <router-link to="/" class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
          Continuar comprando
        </router-link>
      </div>

      <div v-if="cart.items.length === 0" class="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center shadow-soft">
        <p class="text-xl font-semibold text-slate-700">Seu carrinho está vazio.</p>
        <router-link to="/" class="mt-4 inline-block rounded-full bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white hover:bg-slate-700">
          Explorar produtos
        </router-link>
      </div>

      <div v-else class="grid gap-8 lg:grid-cols-[1.5fr_0.8fr]">
        <section class="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-soft">
          <div class="hidden grid-cols-[1.6fr_0.9fr_0.9fr_0.7fr] border-b border-slate-200 px-6 py-4 text-xs font-semibold uppercase tracking-[0.15em] text-slate-500 md:grid">
            <span>Produto</span>
            <span>Preço</span>
            <span>Quantidade</span>
            <span>Total</span>
          </div>

          <div v-for="item in cart.items" :key="item.id" class="grid gap-4 border-b border-slate-200 px-6 py-5 md:grid-cols-[1.6fr_0.9fr_0.9fr_0.7fr] md:items-center">
            <div class="flex items-center gap-4">
              <img :src="item.image" :alt="item.name" class="h-20 w-20 rounded-2xl object-cover" />
              <div>
                <h2 class="text-lg font-bold text-slate-900">{{ item.name }}</h2>
                <button @click="cart.removeItem(item.id)" class="mt-1 text-sm text-red-600 hover:text-red-700">Remover</button>
              </div>
            </div>

            <div class="text-base font-semibold text-slate-900">R$ {{ item.price.toFixed(2) }}</div>

            <div class="flex items-center gap-2">
              <button @click="cart.updateQuantity(item.id, item.quantity - 1)" class="flex h-9 w-9 items-center justify-center rounded-full border border-slate-200 bg-slate-50 text-lg text-slate-700 hover:bg-slate-100">−</button>
              <span class="min-w-8 text-center text-base font-semibold text-slate-900">{{ item.quantity }}</span>
              <button @click="cart.updateQuantity(item.id, item.quantity + 1)" class="flex h-9 w-9 items-center justify-center rounded-full border border-slate-200 bg-slate-50 text-lg text-slate-700 hover:bg-slate-100">+</button>
            </div>

            <div class="text-base font-bold text-slate-900">R$ {{ (item.price * item.quantity).toFixed(2) }}</div>
          </div>
        </section>

        <aside class="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft">
          <h2 class="text-xl font-bold text-slate-900">Resumo</h2>

          <div class="mt-6 space-y-3 text-sm text-slate-600">
            <div class="flex items-center justify-between">
              <span>Subtotal</span>
              <span>R$ {{ subtotal.toFixed(2) }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span>Frete</span>
              <span>{{ shipping === 0 ? 'Grátis' : `R$ ${shipping.toFixed(2)}` }}</span>
            </div>

            <div class="mt-5 rounded-2xl border border-slate-200 bg-slate-50 p-3">
              <label for="coupon" class="mb-2 block text-xs font-semibold uppercase tracking-[0.15em] text-slate-500">Cupom de desconto</label>
              <div class="flex gap-2">
                <input
                  id="coupon"
                  v-model="couponCode"
                  type="text"
                  placeholder="DIGITE10"
                  class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-800 placeholder:text-slate-400 focus:border-slate-400 focus:outline-none"
                />
                <button @click="applyCoupon" class="rounded-xl bg-slate-900 px-3 py-2 text-sm font-semibold text-white hover:bg-slate-700">
                  Aplicar
                </button>
              </div>
              <p v-if="couponMessage" class="mt-2 text-xs" :class="couponApplied ? 'text-emerald-600' : 'text-red-600'">
                {{ couponMessage }}
              </p>
            </div>
          </div>

          <div class="mt-6 border-t border-slate-200 pt-4">
            <div class="flex items-center justify-between text-slate-600">
              <span>Desconto</span>
              <span>- R$ {{ discount.toFixed(2) }}</span>
            </div>
            <div class="mt-3 flex items-center justify-between text-lg font-black text-slate-900">
              <span>Total</span>
              <span>R$ {{ finalTotal.toFixed(2) }}</span>
            </div>
          </div>

          <router-link to="/checkout" class="mt-6 block rounded-full bg-emerald-600 px-5 py-3 text-center text-sm font-semibold text-white hover:bg-emerald-500">
            Finalizar pedido
          </router-link>
        </aside>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import Navbar from '../components/Navbar.vue'
import { useCartStore } from '../stores/cartStore'

const cart = useCartStore()
const couponCode = ref('')
const couponMessage = ref('')
const couponApplied = ref(false)

const subtotal = computed(() => cart.total)
const shipping = computed(() => (subtotal.value > 500 ? 0 : 25))

const discount = computed(() => {
  if (!couponApplied.value) return 0
  return Number((subtotal.value * 0.1).toFixed(2))
})

const finalTotal = computed(() => Math.max(subtotal.value + shipping.value - discount.value, 0))

const applyCoupon = () => {
  if (couponCode.value.trim().toUpperCase() === 'DIGITE10') {
    couponApplied.value = true
    couponMessage.value = 'Cupom aplicado com sucesso!'
    return
  }

  couponApplied.value = false
  couponMessage.value = 'Cupom inválido.'
}
</script>
