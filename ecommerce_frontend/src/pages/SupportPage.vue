<template>
  <div class="min-h-screen bg-slate-100">
    <Navbar />

    <main class="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
      <section class="rounded-3xl bg-slate-900 px-6 py-10 text-white shadow-soft sm:px-10">
        <p class="text-sm font-medium uppercase tracking-[0.2em] text-orange-300">Suporte 24/7</p>
        <h1 class="mt-3 text-3xl font-black sm:text-4xl">Como podemos ajudar?</h1>
        <p class="mt-3 max-w-2xl text-slate-300">Encontre respostas rápidas ou fale diretamente com nossa equipe.</p>
        <label class="mt-7 flex max-w-2xl items-center gap-3 rounded-2xl bg-white px-4 py-3 text-slate-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35m1.85-5.15a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input v-model="searchTerm" type="search" placeholder="Busque por uma dúvida..." class="w-full bg-transparent text-sm text-slate-800 outline-none placeholder:text-slate-400" />
        </label>
      </section>

      <div class="mt-8 grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
        <section class="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft sm:p-8">
          <div class="flex items-end justify-between gap-4">
            <div>
              <p class="text-sm font-medium uppercase tracking-[0.15em] text-slate-500">Central de ajuda</p>
              <h2 class="mt-1 text-2xl font-black text-slate-900">Perguntas Frequentes</h2>
            </div>
            <span class="text-sm text-slate-500">{{ filteredFaqs.length }} encontradas</span>
          </div>

          <div class="mt-6 divide-y divide-slate-200">
            <article v-for="(faq, index) in filteredFaqs" :key="faq.question" class="py-4 first:pt-0 last:pb-0">
              <button @click="toggleFaq(index)" class="flex w-full items-center justify-between gap-4 text-left text-sm font-bold text-slate-900">
                <span>{{ faq.question }}</span>
                <span class="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-slate-100 text-lg font-normal text-slate-600">{{ openFaq === index ? '−' : '+' }}</span>
              </button>
              <p v-if="openFaq === index" class="mt-3 pr-10 text-sm leading-6 text-slate-600">{{ faq.answer }}</p>
            </article>
          </div>
          <p v-if="!filteredFaqs.length" class="mt-6 rounded-2xl bg-slate-50 p-5 text-sm text-slate-500">Não encontramos uma resposta para essa busca.</p>
        </section>

        <div class="space-y-8">
          <section>
            <p class="text-sm font-medium uppercase tracking-[0.15em] text-slate-500">Fale conosco</p>
            <h2 class="mt-1 text-2xl font-black text-slate-900">Canais rápidos</h2>
            <div class="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-1">
              <a href="https://wa.me/5511999999999" target="_blank" rel="noreferrer" class="flex items-center gap-4 rounded-2xl border border-emerald-200 bg-emerald-50 p-5 hover:bg-emerald-100">
                <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-600 text-xl font-black text-white">W</span>
                <span><strong class="block text-sm text-emerald-950">WhatsApp</strong><small class="text-xs text-emerald-800">Resposta em poucos minutos</small></span>
              </a>
              <a href="mailto:suporte@pulsemarket.com" class="flex items-center gap-4 rounded-2xl border border-sky-200 bg-sky-50 p-5 hover:bg-sky-100">
                <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-sky-600 text-xl font-black text-white">@</span>
                <span><strong class="block text-sm text-sky-950">E-mail</strong><small class="text-xs text-sky-800">suporte@pulsemarket.com</small></span>
              </a>
            </div>
          </section>

          <section class="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft sm:p-8">
            <p class="text-sm font-medium uppercase tracking-[0.15em] text-slate-500">Atendimento</p>
            <h2 class="mt-1 text-2xl font-black text-slate-900">Envie uma mensagem</h2>
            <form @submit.prevent="submitMessage" class="mt-5 space-y-4">
              <input v-model="form.name" required type="text" placeholder="Seu nome" class="support-input" />
              <input v-model="form.email" required type="email" placeholder="Seu e-mail" class="support-input" />
              <textarea v-model="form.message" required rows="4" placeholder="Como podemos ajudar?" class="support-input resize-none"></textarea>
              <button class="w-full rounded-2xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white hover:bg-slate-700">Enviar mensagem</button>
            </form>
            <p v-if="sent" class="mt-4 rounded-xl bg-emerald-50 px-4 py-3 text-sm text-emerald-700">Mensagem enviada. Nossa equipe responderá em breve.</p>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import Navbar from '../components/Navbar.vue'

const searchTerm = ref('')
const openFaq = ref(null)
const sent = ref(false)
const form = ref({ name: '', email: '', message: '' })

const faqs = [
  { question: 'Qual é o prazo de entrega?', answer: 'O prazo varia conforme seu endereço. Após a confirmação do pagamento, você recebe o acompanhamento por e-mail.' },
  { question: 'Como acompanho meu pedido?', answer: 'Acesse seu Perfil para consultar o histórico de pedidos e o status de cada compra.' },
  { question: 'Posso trocar um produto?', answer: 'Sim. Você pode solicitar a troca gratuitamente em até 30 dias após o recebimento.' },
  { question: 'Quais formas de pagamento são aceitas?', answer: 'Aceitamos Pix e os principais cartões através do nosso checkout seguro.' },
  { question: 'Como atualizo meus dados?', answer: 'Acesse Perfil, clique em Editar perfil e salve suas novas informações.' },
]

const filteredFaqs = computed(() => {
  const term = searchTerm.value.trim().toLowerCase()
  if (!term) return faqs
  return faqs.filter((faq) => `${faq.question} ${faq.answer}`.toLowerCase().includes(term))
})

const toggleFaq = (index) => {
  openFaq.value = openFaq.value === index ? null : index
}

const submitMessage = () => {
  sent.value = true
  form.value = { name: '', email: '', message: '' }
}
</script>

<style scoped>
.support-input {
  @apply w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 placeholder:text-slate-400 focus:border-slate-400 focus:outline-none;
}
</style>
