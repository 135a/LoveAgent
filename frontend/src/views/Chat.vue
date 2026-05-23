<template>
  <div class="chat-container">
    <!-- Messages -->
    <div class="messages" ref="messagesRef">
      <div v-if="messages.length === 0" class="welcome">
        <div class="welcome-icon">💬</div>
        <p class="welcome-text">开始和你的 AI 伴侣聊天吧～</p>
      </div>
      <div
        v-for="(msg, i) in messages"
        :key="i"
        :class="['message', msg.role === 'user' ? 'user' : 'ai']"
      >
        <div class="bubble">{{ msg.content }}</div>
      </div>
      <div v-if="loading" class="message ai">
        <div class="bubble typing">
          <span class="dot">.</span><span class="dot">.</span><span class="dot">.</span>
        </div>
      </div>
    </div>

    <!-- Input -->
    <div class="input-area">
      <el-input
        v-model="inputText"
        placeholder="说点什么吧～"
        size="large"
        @keyup.enter="sendMessage"
        :disabled="!connected || loading"
      >
        <template #append>
          <el-button @click="sendMessage" :disabled="!connected || loading || !inputText.trim()">
            发送
          </el-button>
        </template>
      </el-input>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useWebSocket } from '../composables/useWebSocket'
import http from '../utils/axios'

const router = useRouter()
const auth = useAuthStore()
const { connected, messages, relationship, connect, send, disconnect } = useWebSocket()

const inputText = ref('')
const loading = ref(false)
const messagesRef = ref(null)

function sendMessage() {
  const text = inputText.value.trim()
  if (!text || !connected.value) return
  send(text)
  inputText.value = ''
  loading.value = true
}

// Listen for AI response to stop loading
watch(messages, () => {
  loading.value = false
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}, { deep: true })

onMounted(() => {
  const token = auth.token
  if (token) {
    connect(token)
  }
})

onUnmounted(() => {
  disconnect()
})
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
  background: #f5f5f5;
}
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px 16px;
}
.welcome {
  text-align: center;
  margin-top: 120px;
}
.welcome-icon { font-size: 48px; margin-bottom: 12px; }
.welcome-text { color: #999; font-size: 15px; }
.message {
  margin-bottom: 16px;
  display: flex;
}
.message.user {
  justify-content: flex-end;
}
.bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 15px;
  line-height: 1.5;
}
.message.ai .bubble {
  background: white;
  border-bottom-left-radius: 4px;
}
.message.user .bubble {
  background: #667eea;
  color: white;
  border-bottom-right-radius: 4px;
}
.typing .dot {
  animation: blink 1.4s infinite;
  font-size: 24px;
  line-height: 1;
}
.typing .dot:nth-child(2) { animation-delay: 0.2s; }
.typing .dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink {
  0%, 60%, 100% { opacity: 0.3; }
  30% { opacity: 1; }
}
.input-area {
  padding: 12px 16px;
  background: white;
  border-top: 1px solid #eee;
}
</style>
