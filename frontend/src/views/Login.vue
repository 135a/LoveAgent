<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="title">LoveAgent</h1>
      <p class="subtitle">你的 AI 虚拟伴侣</p>

      <el-form @submit.prevent="handleSubmit" class="form">
        <el-input
          v-model="form.username"
          placeholder="用户名"
          :prefix-icon="User"
          size="large"
          class="input"
        />
        <el-input
          v-model="form.password"
          type="password"
          placeholder="密码"
          :prefix-icon="Lock"
          size="large"
          class="input"
          show-password
        />
        <el-button type="primary" size="large" class="btn" @click="handleSubmit" :loading="loading">
          {{ isLogin ? '登录' : '注册' }}
        </el-button>
      </el-form>

      <p class="switch">
        {{ isLogin ? '还没有账号？' : '已有账号？' }}
        <a href="#" @click.prevent="isLogin = !isLogin">
          {{ isLogin ? '去注册' : '去登录' }}
        </a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const isLogin = ref(true)
const loading = ref(false)
const form = reactive({ username: '', password: '' })

async function handleSubmit() {
  if (!form.username || !form.password) {
    ElMessage.warning('请填写用户名和密码')
    return
  }
  if (!isLogin.value && form.password.length < 6) {
    ElMessage.warning('密码至少需要 6 位')
    return
  }

  loading.value = true
  try {
    if (isLogin.value) {
      await auth.login(form.username, form.password)
    } else {
      await auth.register(form.username, form.password)
    }
    ElMessage.success(isLogin.value ? '登录成功' : '注册成功')

    // Check if character exists
    const http = (await import('../utils/axios')).default
    const char = await http.get('/api/characters/my')
    if (char) {
      router.push('/chat')
    } else {
      router.push('/characters')
    }
  } catch (err) {
    const detail = err.response?.data?.detail || '操作失败'
    ElMessage.error(detail)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.login-card {
  background: white;
  border-radius: 16px;
  padding: 48px 40px;
  width: 400px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
  text-align: center;
}
.title {
  font-size: 32px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 4px;
}
.subtitle {
  color: #999;
  margin-bottom: 32px;
  font-size: 14px;
}
.form .input {
  margin-bottom: 16px;
}
.btn {
  width: 100%;
  margin-top: 8px;
}
.switch {
  margin-top: 24px;
  color: #999;
  font-size: 14px;
}
.switch a {
  color: #667eea;
  text-decoration: none;
}
</style>
