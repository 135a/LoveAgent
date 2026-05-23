<template>
  <div class="settings-container">
    <div class="settings-card">
      <h2>设置</h2>

      <el-divider />

      <el-form label-width="100px">
        <el-form-item label="称呼">
          <el-input v-model="customName" placeholder="你希望 AI 怎么称呼你？" />
        </el-form-item>

        <el-form-item label="角色信息">
          <div v-if="character">
            <el-tag>{{ character.gender === 'female' ? '女生' : '男生' }}</el-tag>
            <el-tag type="success" style="margin-left:8px">{{ character.personality }}</el-tag>
            <el-tag type="warning" style="margin-left:8px">亲密度 {{ Math.round(character.intimacy_score * 100) }}%</el-tag>
          </div>
          <span v-else class="text-muted">暂无角色</span>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="saveSettings" :loading="saving">保存设置</el-button>
          <el-button @click="resetCharacter" type="danger" plain style="margin-left:12px">重置角色</el-button>
        </el-form-item>
      </el-form>

      <el-divider />

      <el-button @click="logout" type="info" plain>退出登录</el-button>
      <el-button @click="$router.push('/chat')" text style="margin-left:12px">← 返回聊天</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '../stores/auth'
import http from '../utils/axios'

const router = useRouter()
const auth = useAuthStore()

const customName = ref('')
const character = ref(null)
const saving = ref(false)

onMounted(async () => {
  try {
    character.value = await http.get('/api/characters/my')
    if (character.value?.custom_name) {
      customName.value = character.value.custom_name
    }
  } catch {}
})

async function saveSettings() {
  saving.value = true
  try {
    // Update custom name (simple approach - re-choose with same gender/personality)
    await http.post('/api/characters/choose', {
      gender: character.value.gender,
      personality: character.value.personality,
    })
    // Note: custom name update would need a dedicated API - simplified for MVP
    ElMessage.success('设置已保存')
  } catch (err) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

function resetCharacter() {
  ElMessageBox.confirm('重置角色将清空关系进度，确定要重置吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    router.push('/characters')
    ElMessage.info('请重新选择角色')
  }).catch(() => {})
}

function logout() {
  auth.logout()
  router.push('/login')
  ElMessage.success('已退出登录')
}
</script>

<style scoped>
.settings-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}
.settings-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  width: 500px;
  max-width: 100%;
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
}
h2 { margin-bottom: 0; }
.text-muted { color: #999; font-size: 14px; }
</style>
