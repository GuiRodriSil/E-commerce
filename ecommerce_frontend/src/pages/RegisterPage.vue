<template>
  <div class="flex min-h-screen items-center justify-center bg-slate-100 px-4 py-10">
    <div class="w-full max-w-lg rounded-3xl border border-slate-200 bg-white p-8 shadow-soft">
      <div class="mb-8 text-center">
        <router-link to="/" class="inline-flex items-center gap-3">
          <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-900 text-xl font-black text-white">E</div>
          <div>
            <p class="text-lg font-black text-slate-900">Ecommerce</p>
            <p class="text-xs text-slate-500">Crie sua conta</p>
          </div>
        </router-link>
      </div>

      <h1 class="text-3xl font-black text-slate-900">Cadastrar</h1>
      <p class="mt-2 text-sm text-slate-500">Preencha os dados abaixo para criar sua conta.</p>

      <form @submit.prevent="handleSubmit" class="mt-8 space-y-5">
        <div>
          <label for="name" class="mb-2 block text-sm font-medium text-slate-700">Nome completo</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            placeholder="Seu nome"
            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 placeholder:text-slate-400 focus:border-slate-400 focus:outline-none"
          />
          <p v-if="errors.name" class="mt-1 text-xs text-red-600">{{ errors.name }}</p>
        </div>

        <div>
          <label for="email" class="mb-2 block text-sm font-medium text-slate-700">E-mail</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="seu@email.com"
            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 placeholder:text-slate-400 focus:border-slate-400 focus:outline-none"
          />
          <p v-if="errors.email" class="mt-1 text-xs text-red-600">{{ errors.email }}</p>
        </div>

        <div>
          <label for="password" class="mb-2 block text-sm font-medium text-slate-700">Senha</label>
          <div class="relative">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="********"
              class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 pr-11 text-sm text-slate-800 placeholder:text-slate-400 focus:border-slate-400 focus:outline-none"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute inset-y-0 right-3 flex items-center text-slate-500 hover:text-slate-700"
            >
              <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7a9.973 9.973 0 012.17-3.6M6.3 6.3A9.954 9.954 0 0112 5c4.478 0 8.268 2.943 9.542 7a10.024 10.024 0 01-4.063 5.178M9.88 9.88A3 3 0 0114.12 14.12M3 3l18 18" />
              </svg>
            </button>
          </div>
          <p v-if="errors.password" class="mt-1 text-xs text-red-600">{{ errors.password }}</p>
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full rounded-2xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {{ loading ? 'Cadastrando...' : 'Criar conta' }}
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-slate-600">
        Já tem conta?
        <router-link to="/login" class="font-semibold text-slate-900 hover:text-slate-700">Fazer login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const showPassword = ref(false)

const form = ref({
  name: '',
  email: '',
  password: '',
})

const errors = ref({
  name: '',
  email: '',
  password: '',
})

const validate = () => {
  let valid = true
  errors.value = { name: '', email: '', password: '' }

  if (!form.value.name.trim()) {
    errors.value.name = 'Informe seu nome.'
    valid = false
  }

  if (!form.value.email.trim()) {
    errors.value.email = 'Informe seu e-mail.'
    valid = false
  } else if (!/\S+@\S+\.\S+/.test(form.value.email)) {
    errors.value.email = 'E-mail inválido.'
    valid = false
  }

  if (!form.value.password.trim()) {
    errors.value.password = 'Informe uma senha.'
    valid = false
  } else if (form.value.password.length < 6) {
    errors.value.password = 'A senha deve ter pelo menos 6 caracteres.'
    valid = false
  }

  return valid
}

const handleSubmit = async () => {
  if (!validate()) return

  loading.value = true

  try {
    const response = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: form.value.name,
        email: form.value.email,
        password: form.value.password,
      }),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'Erro ao cadastrar usuário')
    }

    localStorage.setItem('ecommerce_token', data.access_token)
    router.push('/')
  } catch (error) {
    errors.value.email = error.message
  } finally {
    loading.value = false
  }
}
</script>
