import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import http from '../utils/axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userId = ref(Number(localStorage.getItem('user_id')) || 0)
  const username = ref(localStorage.getItem('username') || '')

  const isLoggedIn = computed(() => !!token.value)

  async function login(usernameInput, password) {
    const res = await http.post('/api/auth/login', { username: usernameInput, password })
    setAuth(res.token, res.user_id, res.username)
    return res
  }

  async function register(usernameInput, password) {
    const res = await http.post('/api/auth/register', { username: usernameInput, password })
    setAuth(res.token, res.user_id, res.username)
    return res
  }

  function setAuth(t, uid, uname) {
    token.value = t
    userId.value = uid
    username.value = uname
    localStorage.setItem('token', t)
    localStorage.setItem('user_id', String(uid))
    localStorage.setItem('username', uname)
  }

  function logout() {
    token.value = ''
    userId.value = 0
    username.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
    localStorage.removeItem('username')
  }

  return { token, userId, username, isLoggedIn, login, register, logout, setAuth }
})
