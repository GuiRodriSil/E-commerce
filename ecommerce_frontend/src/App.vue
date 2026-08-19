<template>
  <div class="min-h-screen bg-slate-100 text-slate-800">
    <RouterView />
    <SupportChat />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import SupportChat from './components/SupportChat.vue'
</script>
