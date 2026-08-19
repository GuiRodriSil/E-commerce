<template>
  <section class="mb-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4" aria-label="Benefícios da loja">
    <component :is="benefit.icon === 'support' ? 'router-link' : 'article'" v-for="benefit in benefits" :key="benefit.title" :to="benefit.icon === 'support' ? '/support' : undefined" class="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-soft" :class="benefit.icon === 'support' ? 'transition hover:-translate-y-0.5 hover:border-orange-200' : ''">
      <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-orange-100 text-orange-600">
        <svg v-if="benefit.icon === 'truck'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 7h11v10H3zM14 10h4l3 3v4h-7zM7 19a2 2 0 100-4 2 2 0 000 4zM18 19a2 2 0 100-4 2 2 0 000 4z" />
        </svg>
        <svg v-else-if="benefit.icon === 'shield'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 3l7 3v5c0 4.5-3 7.8-7 10-4-2.2-7-5.5-7-10V6l7-3z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4" />
        </svg>
        <svg v-else-if="benefit.icon === 'refresh'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
          <path stroke-linecap="round" stroke-linejoin="round" d="M20 11a8 8 0 00-14.8-3L3 10m0 0V5m0 5h5M4 13a8 8 0 0014.8 3L21 14m0 0v5m0-5h-5" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
          <path stroke-linecap="round" stroke-linejoin="round" d="M18 10a6 6 0 10-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9zM10 22h4" />
        </svg>
      </div>
      <div>
        <h2 class="text-sm font-bold text-slate-900">{{ benefit.title }}</h2>
        <p class="mt-1 text-xs leading-5 text-slate-500">{{ benefit.description }}</p>
      </div>
    </component>
  </section>
</template>

<script setup>
const benefits = [
  { title: 'Entrega Rápida', description: 'Receba seu pedido com agilidade.', icon: 'truck' },
  { title: 'Pagamento Seguro', description: 'Compra protegida do início ao fim.', icon: 'shield' },
  { title: 'Troca Grátis em 30 dias', description: 'Você compra tranquilo e sem pressa.', icon: 'refresh' },
  { title: 'Suporte 24/7', description: 'Estamos prontos para ajudar sempre.', icon: 'support' },
]
</script>
