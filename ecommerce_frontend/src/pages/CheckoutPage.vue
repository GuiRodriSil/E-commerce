<template>
  <div class="min-h-screen bg-slate-100">
    <Navbar />

    <main class="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
      <div class="mb-8">
        <p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">Checkout</p>
        <h1 class="mt-2 text-3xl font-black text-slate-900">Finalizar compra</h1>
        <p class="mt-2 text-sm text-slate-500">Pagamento seguro para {{ auth.user?.email }}</p>
      </div>

      <div v-if="cart.items.length === 0" class="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center shadow-soft">
        <p class="text-xl font-semibold text-slate-700">Seu carrinho está vazio.</p>
        <router-link to="/home" class="mt-4 inline-block rounded-full bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white hover:bg-slate-700">
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
            <div v-for="item in cart.items" :key="`summary-${item.id}`" class="flex justify-between text-xs text-slate-500">
              <span>{{ item.name }} × {{ item.quantity }}</span>
              <span>R$ {{ (item.price * item.quantity).toFixed(2) }}</span>
            </div>
            <div class="flex justify-between border-t border-slate-100 pt-3">
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

          <div class="mt-6">
            <p class="mb-3 text-sm font-semibold text-slate-700">Forma de pagamento</p>
            <div class="grid gap-3">
              <label v-for="method in paymentMethods" :key="method.value" class="flex cursor-pointer items-start gap-3 rounded-2xl border p-4 text-sm transition" :class="selectedMethod === method.value ? 'border-emerald-500 bg-emerald-50 ring-1 ring-emerald-500' : 'border-slate-200 hover:bg-slate-50'">
                <input v-model="selectedMethod" type="radio" name="payment-method" :value="method.value" class="mt-1 accent-emerald-600" />
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-900 text-xs font-black text-white">{{ method.icon }}</span>
                <span><strong class="block text-slate-900">{{ method.label }}</strong><small class="text-xs text-slate-500">{{ method.description }}</small></span>
              </label>
            </div>
          </div>

          <p v-if="errorMessage" class="mt-4 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">{{ errorMessage }}</p>

          <button
            @click="createPayment"
            :disabled="loading"
            class="mt-6 w-full rounded-full bg-emerald-600 px-5 py-3 text-sm font-semibold text-white hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {{ loading ? 'Processando pagamento...' : `Pagar com ${selectedMethodLabel}` }}
          </button>
          <p class="mt-3 text-center text-xs text-slate-500">Seus dados são processados com segurança pelo Mercado Pago.</p>
        </aside>
      </div>

      <div v-if="pixData" class="mt-10 rounded-3xl border border-emerald-200 bg-emerald-50 p-6 shadow-soft">
        <div class="flex items-start justify-between gap-4">
          <div><h2 class="text-2xl font-bold text-emerald-900">PIX pronto para pagamento</h2><p class="mt-1 text-sm text-emerald-700">Escaneie o QR Code ou copie o código abaixo.</p></div>
          <span class="rounded-full bg-emerald-200 px-3 py-1 text-xs font-bold text-emerald-800">Pendente</span>
        </div>
        <p class="mt-2 text-sm text-emerald-700">Pagamento ID: {{ pixData.payment_id }}</p>
        <p class="mt-4 text-lg font-semibold text-slate-900">Valor: R$ {{ pixData.transaction_amount.toFixed(2) }}</p>

        <div class="mt-6 flex flex-col items-center gap-4 md:flex-row md:items-start">
          <img v-if="pixData.qr_code_base64" :src="`data:image/png;base64,${pixData.qr_code_base64}`" alt="QR Code PIX" class="h-52 w-52 rounded-2xl bg-white p-3 shadow-sm" />
          <div class="flex-1 rounded-2xl bg-white p-4 shadow-sm">
            <p class="text-sm font-medium text-slate-500">Código PIX</p>
            <textarea readonly class="mt-2 h-32 w-full resize-none rounded-xl border border-slate-200 bg-slate-50 p-3 text-xs text-slate-700" :value="pixData.qr_code"></textarea>
            <button @click="copyPixCode" class="mt-3 rounded-xl bg-slate-900 px-4 py-2 text-xs font-semibold text-white hover:bg-slate-700">{{ copied ? 'Código copiado' : 'Copiar código PIX' }}</button>
          </div>
        </div>
      </div>
      <div v-if="checkoutUrl" class="mt-10 rounded-3xl border border-sky-200 bg-sky-50 p-6 shadow-soft">
        <h2 class="text-2xl font-bold text-sky-900">Pagamento pronto</h2>
        <p class="mt-2 text-sm text-sky-700">Continue com segurança no Mercado Pago.</p>
        <a :href="checkoutUrl" target="_blank" rel="noreferrer" class="mt-5 inline-block rounded-full bg-sky-600 px-5 py-3 text-sm font-semibold text-white hover:bg-sky-500">Continuar pagamento</a>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'
import { useCartStore } from '../stores/cartStore'
import { useAuthStore } from '../stores/useAuthStore'

const cart = useCartStore()
const auth = useAuthStore()
const router = useRouter()
const loading = ref(false)
const errorMessage = ref('')
const copied = ref(false)
const pixData = ref(null)
const checkoutUrl = ref('')
const selectedMethod = ref('pix')
const paymentMethods = [
  { value: 'pix', label: 'PIX', description: 'Aprovação imediata', icon: 'P' },
  { value: 'card', label: 'Cartão de crédito', description: 'Pagamento no checkout seguro', icon: 'C' },
  { value: 'boleto', label: 'Boleto bancário', description: 'Compensação em até 3 dias úteis', icon: 'B' },
]
const selectedMethodLabel = computed(() => paymentMethods.find((method) => method.value === selectedMethod.value)?.label || 'PIX')

const createPayment = async () => {
  if (!cart.items.length) return
  if (!auth.isAuthenticated) {
    router.push({ path: '/login', query: { redirect: '/checkout' } })
    return
  }

  loading.value = true
  errorMessage.value = ''
  pixData.value = null
  checkoutUrl.value = ''

  try {
    const payload = {
      payer_email: auth.user.email,
      payment_method: selectedMethod.value,
      items: cart.items.map((item) => ({
        id: item.id,
        title: item.name,
        quantity: item.quantity,
        unit_price: item.price,
      })),
    }

    const response = await fetch('http://localhost:8000/payments/mercadopago', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${auth.token}` },
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.detail || 'Não foi possível iniciar o pagamento.')
    }

    const data = await response.json()
    pixData.value = selectedMethod.value === 'pix' ? data : null
    checkoutUrl.value = selectedMethod.value === 'pix' ? '' : data.checkout_url
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    loading.value = false
  }
}

const copyPixCode = async () => {
  if (!pixData.value?.qr_code) return
  await navigator.clipboard.writeText(pixData.value.qr_code)
  copied.value = true
  window.setTimeout(() => { copied.value = false }, 2000)
}
</script>
