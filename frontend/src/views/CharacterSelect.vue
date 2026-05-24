<template>
  <div class="select-container">
    <div class="select-card">
      <h2 class="title">选择你的 AI 伴侣</h2>
      <p class="subtitle">{{ step === 1 ? '先选择性别' : '选择她的性格' }}</p>

      <!-- Step 1: Gender selection -->
      <div v-if="step === 1" class="gender-grid">
        <div
          v-for="g in genders"
          :key="g.value"
          class="gender-card"
          @click="selectGender(g.value)"
        >
          <div class="gender-icon">{{ g.icon }}</div>
          <div class="gender-name">{{ g.label }}</div>
          <div class="gender-desc">{{ g.desc }}</div>
        </div>
      </div>

      <!-- Step 2: Personality selection -->
      <div v-else class="personality-list">
        <div
          v-for="p in personalities"
          :key="p.id"
          class="personality-card"
          @click="selectPersonality(p)"
        >
          <div class="personality-name">{{ p.personality }}</div>
          <div class="personality-desc">{{ p.description }}</div>
          <div class="personality-traits">
            <el-tag v-for="t in p.traits" :key="t" size="small" class="trait">{{ t }}</el-tag>
          </div>
        </div>
        <el-button class="back-btn" text @click="step = 1">返回选择性别</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import http from '../utils/axios'

const router = useRouter()
const route = useRoute()
const step = ref(1)
const selectedGender = ref('')
const personalities = ref([])
const genders = [
  { value: 'female', label: '女生', icon: '🌸', desc: '慢热害羞，熟了之后会很粘人' },
  { value: 'male', label: '男生', icon: '🌻', desc: '活泼幽默，总是能逗你开心' },
]

async function selectGender(gender) {
  selectedGender.value = gender
  const res = await http.get('/api/characters/', { params: { gender } })
  personalities.value = res
  step.value = 2
}

async function selectPersonality(p) {
  try {
    await http.post('/api/characters/choose', {
      gender: selectedGender.value,
      personality: p.personality,
    })
    ElMessage.success(`${p.name} 来到了你的身边～`)
    router.push('/chat')
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '选择失败')
  }
}

onMounted(async () => {
  // If user already has a character, go to chat (unless we are manually switching)
  if (route.query.action === 'switch') return

  try {
    const char = await http.get('/api/characters/my')
    if (char) router.push('/chat')
  } catch {}
})
</script>

<style scoped>
.select-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}
.select-card {
  background: white;
  border-radius: 16px;
  padding: 48px;
  width: 560px;
  max-width: 100%;
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
  text-align: center;
}
.title {
  font-size: 24px;
  margin-bottom: 8px;
}
.subtitle {
  color: #999;
  margin-bottom: 32px;
}
.gender-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.gender-card {
  border: 2px solid #eee;
  border-radius: 12px;
  padding: 32px 20px;
  cursor: pointer;
  transition: all 0.3s;
}
.gender-card:hover {
  border-color: #667eea;
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(102,126,234,0.2);
}
.gender-icon {
  font-size: 48px;
  margin-bottom: 12px;
}
.gender-name {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 8px;
}
.gender-desc {
  font-size: 13px;
  color: #999;
}
.personality-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.personality-card {
  border: 2px solid #eee;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  text-align: left;
  transition: all 0.3s;
}
.personality-card:hover {
  border-color: #667eea;
  transform: translateX(4px);
}
.personality-name {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}
.personality-desc {
  font-size: 13px;
  color: #666;
  margin-bottom: 8px;
}
.trait {
  margin-right: 4px;
  margin-bottom: 4px;
}
.back-btn {
  margin-top: 8px;
}
</style>
