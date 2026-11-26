<script setup lang="ts">
import { ref } from 'vue'
import { fetchGreet } from '@/api/demo/greet'
import PageCard from '@/components/common/PageCard.vue'

const name = ref('')
const message = ref('')
const loading = ref(false)

/** 点「问候」：调后端示例接口，把返回的问候语显示在页面上；提交中禁用按钮防重复点击。 */
async function submit() {
  loading.value = true
  try {
    const res = await fetchGreet(name.value)
    message.value = res.message
  } catch {
    message.value = ''
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <PageCard title="问候示例">
    <el-form inline @submit.prevent="submit">
      <el-form-item label="名字">
        <el-input v-model="name" data-test="greet-name" placeholder="请输入名字" clearable />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit" :loading="loading" data-test="greet-submit">
          问候
        </el-button>
      </el-form-item>
    </el-form>
    <p v-if="message" class="greet-message" data-test="greet-message">{{ message }}</p>
  </PageCard>
</template>

<style scoped>
.greet-message {
  color: var(--app-color-text);
  font-size: var(--app-font-size-lg);
}
</style>
