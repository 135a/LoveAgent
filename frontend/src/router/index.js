import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/Login.vue'
import CharacterSelect from '../views/CharacterSelect.vue'
import Chat from '../views/Chat.vue'
import Settings from '../views/Settings.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/characters', name: 'CharacterSelect', component: CharacterSelect, meta: { requiresAuth: true } },
  { path: '/chat', name: 'Chat', component: Chat, meta: { requiresAuth: true } },
  { path: '/settings', name: 'Settings', component: Settings, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Auth guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
