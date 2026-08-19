<template>
  <div class="min-h-screen bg-slate-100">
    <Navbar />

    <main class="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
      <div class="mb-8">
        <p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">Minha conta</p>
        <h1 class="mt-2 text-3xl font-black text-slate-900">Perfil</h1>
      </div>

      <section v-if="!auth.isAuthenticated" class="mx-auto max-w-lg rounded-3xl border border-slate-200 bg-white p-6 shadow-soft sm:p-8">
        <div class="flex rounded-2xl bg-slate-100 p-1">
          <button @click="activeTab = 'login'" :class="tabClass('login')">Login</button>
          <button @click="activeTab = 'register'" :class="tabClass('register')">Cadastro</button>
        </div>

        <form v-if="activeTab === 'login'" @submit.prevent="submitLogin" class="mt-8 space-y-5">
          <div>
            <label for="login-email" class="mb-2 block text-sm font-medium text-slate-700">E-mail</label>
            <input id="login-email" v-model="loginForm.email" type="email" required class="profile-input" placeholder="seu@email.com" />
          </div>
          <div>
            <label for="login-password" class="mb-2 block text-sm font-medium text-slate-700">Senha</label>
            <input id="login-password" v-model="loginForm.password" type="password" required class="profile-input" placeholder="********" />
          </div>
          <button :disabled="auth.loading" class="profile-button">
            {{ auth.loading ? 'Entrando...' : 'Entrar' }}
          </button>
        </form>

        <form v-else @submit.prevent="submitRegister" class="mt-8 space-y-5">
          <div>
            <label for="register-name" class="mb-2 block text-sm font-medium text-slate-700">Nome completo</label>
            <input id="register-name" v-model="registerForm.name" type="text" required class="profile-input" placeholder="Seu nome" />
          </div>
          <div>
            <label for="register-email" class="mb-2 block text-sm font-medium text-slate-700">E-mail</label>
            <input id="register-email" v-model="registerForm.email" type="email" required class="profile-input" placeholder="seu@email.com" />
          </div>
          <div>
            <label for="register-password" class="mb-2 block text-sm font-medium text-slate-700">Senha</label>
            <input id="register-password" v-model="registerForm.password" type="password" minlength="6" required class="profile-input" placeholder="Mínimo de 6 caracteres" />
          </div>
          <button :disabled="auth.loading" class="profile-button">
            {{ auth.loading ? 'Criando conta...' : 'Criar conta' }}
          </button>
        </form>

        <p v-if="auth.error" class="mt-4 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">{{ auth.error }}</p>
      </section>

      <section v-else class="space-y-8">
        <div class="grid gap-8 lg:grid-cols-[0.8fr_1.2fr]">
          <article class="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft">
            <div class="flex items-start justify-between gap-4">
              <div>
                <div class="flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-900 text-2xl font-black text-white">
                  {{ auth.user.name.charAt(0).toUpperCase() }}
                </div>
                <h2 class="mt-5 text-2xl font-black text-slate-900">{{ auth.user.name }}</h2>
                <p class="mt-1 text-sm text-slate-500">{{ auth.user.email }}</p>
              </div>
              <button @click="startEditing" class="rounded-full border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50">
                Editar perfil
              </button>
            </div>

            <form v-if="editing" @submit.prevent="saveProfile" class="mt-6 space-y-4 border-t border-slate-200 pt-6">
              <div>
                <label for="profile-name" class="mb-2 block text-sm font-medium text-slate-700">Nome</label>
                <input id="profile-name" v-model="editForm.name" type="text" required class="profile-input" />
              </div>
              <div>
                <label for="profile-password" class="mb-2 block text-sm font-medium text-slate-700">Nova senha</label>
                <input id="profile-password" v-model="editForm.password" type="password" minlength="6" class="profile-input" placeholder="Deixe vazio para manter" />
              </div>
              <div class="flex gap-3">
                <button :disabled="auth.loading" class="profile-button">Salvar</button>
                <button type="button" @click="editing = false" class="rounded-2xl border border-slate-200 px-4 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50">Cancelar</button>
              </div>
              <p v-if="auth.error" class="text-sm text-red-600">{{ auth.error }}</p>
            </form>

            <button @click="logout" class="mt-8 w-full rounded-2xl border border-red-200 px-4 py-3 text-sm font-semibold text-red-600 hover:bg-red-50">
              Sair
            </button>
          </article>

          <article class="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium uppercase tracking-[0.15em] text-slate-500">Atividade</p>
                <h2 class="mt-1 text-2xl font-black text-slate-900">Pedidos recentes</h2>
              </div>
              <span class="rounded-full bg-slate-100 px-3 py-1 text-sm font-semibold text-slate-600">{{ auth.user.orders.length }}</span>
            </div>

            <div v-if="!auth.user.orders.length" class="mt-8 rounded-2xl bg-slate-50 p-6 text-center text-sm text-slate-500">
              Você ainda não fez nenhum pedido.
            </div>
            <div v-else class="mt-6 divide-y divide-slate-200">
              <div v-for="order in auth.user.orders" :key="order.id" class="flex items-center justify-between gap-4 py-4">
                <div>
                  <p class="font-semibold text-slate-900">Pedido #{{ order.id }}</p>
                  <p class="mt-1 text-sm capitalize text-slate-500">{{ order.status }} · {{ formatDate(order.created_at) }}</p>
                </div>
                <p class="font-bold text-slate-900">R$ {{ Number(order.total).toFixed(2) }}</p>
              </div>
            </div>
          </article>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'
import { useAuthStore } from '../stores/useAuthStore'

const auth = useAuthStore()
const router = useRouter()
const activeTab = ref('login')
const editing = ref(false)
const loginForm = ref({ email: '', password: '' })
const registerForm = ref({ name: '', email: '', password: '' })
const editForm = ref({ name: '', password: '' })

const tabClass = (tab) => [
  'w-1/2 rounded-xl px-4 py-2.5 text-sm font-semibold transition',
  activeTab.value === tab ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700',
]

const submitLogin = async () => {
  try {
    await auth.login(loginForm.value)
  } catch {
    // The store exposes the request error in the form.
  }
}

const submitRegister = async () => {
  try {
    await auth.register(registerForm.value)
  } catch {
    // The store exposes the request error in the form.
  }
}

const startEditing = () => {
  editForm.value = { name: auth.user.name, password: '' }
  auth.error = ''
  editing.value = true
}

const saveProfile = async () => {
  try {
    const payload = { name: editForm.value.name }
    if (editForm.value.password) payload.password = editForm.value.password
    await auth.updateProfile(payload)
    editing.value = false
  } catch {
    // The store exposes the request error next to the form.
  }
}

const logout = () => {
  auth.logout()
  activeTab.value = 'login'
  router.push('/login')
}

const formatDate = (value) => new Intl.DateTimeFormat('pt-BR').format(new Date(value))

onMounted(async () => {
  if (auth.token && !auth.user) {
    try {
      await auth.fetchProfile()
    } catch {
      // An expired token is cleared by the store.
    }
  }
})
</script>

<style scoped>
.profile-input {
  @apply w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 placeholder:text-slate-400 focus:border-slate-400 focus:outline-none;
}

.profile-button {
  @apply w-full rounded-2xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-60;
}
</style>
