<template>
  <div class="group overflow-hidden rounded-2xl bg-slate-100">
    <img
      :src="src"
      :alt="alt"
      class="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-110"
    />
  </div>
</template>

<script setup>
defineProps({
  src: {
    type: String,
    required: true,
  },
  alt: {
    type: String,
    required: true,
  },
})
</script>
