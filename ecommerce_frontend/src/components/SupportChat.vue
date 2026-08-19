<template>
  <div class="fixed bottom-5 right-5 z-50 sm:bottom-6 sm:right-6">
    <section v-if="isOpen" class="mb-3 flex w-[min(22rem,calc(100vw-2.5rem))] flex-col overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-2xl">
      <header class="flex items-center justify-between bg-slate-900 px-5 py-4 text-white">
        <div>
          <p class="text-sm font-bold">Atendimento rápido</p>
          <p class="mt-0.5 text-xs text-slate-300">Online agora</p>
        </div>
        <button @click="isOpen = false" aria-label="Fechar chat" class="flex h-8 w-8 items-center justify-center rounded-full text-xl text-slate-300 hover:bg-white/10 hover:text-white">×</button>
      </header>

      <div ref="messagesElement" class="flex max-h-72 min-h-52 flex-col gap-3 overflow-y-auto bg-slate-50 p-4">
        <div v-for="message in messages" :key="message.id" class="flex" :class="message.from === 'customer' ? 'justify-end' : 'justify-start'">
          <p class="max-w-[85%] rounded-2xl px-3 py-2 text-sm leading-5" :class="message.from === 'customer' ? 'rounded-br-md bg-slate-900 text-white' : 'rounded-bl-md bg-white text-slate-700 shadow-sm'">
            {{ message.text }}
          </p>
        </div>
        <div v-if="isTyping" class="flex justify-start">
          <p class="rounded-2xl rounded-bl-md bg-white px-3 py-2 text-sm text-slate-400 shadow-sm">Digitando...</p>
        </div>
      </div>

      <div class="border-t border-slate-200 bg-white p-3">
        <div class="mb-3 flex flex-wrap gap-2">
          <button v-for="question in quickQuestions" :key="question" @click="sendMessage(question)" class="rounded-full bg-orange-50 px-3 py-1.5 text-xs font-semibold text-orange-700 hover:bg-orange-100">
            {{ question }}
          </button>
        </div>
        <form @submit.prevent="sendMessage(messageInput)" class="flex items-center gap-2">
          <input v-model="messageInput" type="text" placeholder="Digite sua dúvida..." class="min-w-0 flex-1 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none focus:border-slate-400" />
          <button type="submit" aria-label="Enviar mensagem" class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-orange-500 text-lg text-white hover:bg-orange-600">↑</button>
        </form>
      </div>
    </section>

    <button @click="isOpen = !isOpen" :aria-expanded="isOpen" aria-label="Abrir chat de suporte" class="ml-auto flex h-14 w-14 items-center justify-center rounded-full bg-orange-500 text-white shadow-xl shadow-orange-500/30 hover:-translate-y-1 hover:bg-orange-600">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
        <path stroke-linecap="round" stroke-linejoin="round" d="M8 10h8M8 14h5m7-2a8 8 0 01-8 8 8.5 8.5 0 01-3.7-.85L4 20l.85-3.3A8 8 0 1112 20" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { nextTick, ref } from 'vue'

const isOpen = ref(false)
const messageInput = ref('')
const isTyping = ref(false)
const messagesElement = ref(null)
let nextMessageId = 2

const messages = ref([
  { id: 1, from: 'support', text: 'Olá! Como posso ajudar você hoje?' },
])

const quickQuestions = ['Onde está meu pedido?', 'Como faço uma troca?', 'Quais pagamentos aceitam?']

const responses = {
  'Onde está meu pedido?': 'Você pode acompanhar pedidos recentes no seu Perfil, na seção “Pedidos recentes”.',
  'Como faço uma troca?': 'A troca é gratuita em até 30 dias. Consulte nossa equipe pelo formulário de suporte.',
  'Quais pagamentos aceitam?': 'Aceitamos PIX, cartão de crédito e boleto bancário.',
}

const scrollToBottom = async () => {
  await nextTick()
  messagesElement.value?.scrollTo({ top: messagesElement.value.scrollHeight, behavior: 'smooth' })
}

const sendMessage = (text) => {
  const cleanText = text.trim()
  if (!cleanText || isTyping.value) return

  messages.value.push({ id: nextMessageId++, from: 'customer', text: cleanText })
  messageInput.value = ''
  scrollToBottom()
  isTyping.value = true

  window.setTimeout(() => {
    messages.value.push({
      id: nextMessageId++,
      from: 'support',
      text: responses[cleanText] || 'Obrigado pela mensagem! Para uma resposta detalhada, envie uma solicitação na página de suporte.',
    })
    isTyping.value = false
    scrollToBottom()
  }, 650)
}
</script>
