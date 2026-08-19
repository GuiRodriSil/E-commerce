<template>
  <nav aria-label="Navegação estrutural" class="flex items-center gap-2 text-sm text-slate-500">
    <template v-for="(item, index) in items" :key="`${item.label}-${index}`">
      <span v-if="index" aria-hidden="true" class="text-slate-300">/</span>

      <span v-if="index === items.length - 1" class="truncate font-medium text-slate-700" aria-current="page">
        {{ item.label }}
      </span>
      <router-link v-else :to="item.to" class="truncate hover:text-slate-900">
        {{ item.label }}
      </router-link>
    </template>
  </nav>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
    validator: (items) => items.every((item) => typeof item.label === 'string' && 'to' in item),
  },
})
</script>
