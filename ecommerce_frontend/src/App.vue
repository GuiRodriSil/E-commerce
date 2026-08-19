<template>
  <div class="min-h-screen bg-slate-100 text-slate-800">
    <RouterView />
    <SupportChat />
    <CartConfirmationModal />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import CartConfirmationModal from './components/CartConfirmationModal.vue'
import SupportChat from './components/SupportChat.vue'
</script>
