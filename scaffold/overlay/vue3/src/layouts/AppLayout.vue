<script setup lang="ts">
import { useRoute } from 'vue-router'
import { ASIDE_WIDTH, APP_TITLE } from '@/constants/layout'

/** 全站唯一外壳：顶栏 + 侧栏菜单 + 内容区。各页只写内容，不复制侧栏和顶栏。 */
const route = useRoute()
</script>

<template>
  <el-container class="app-layout">
    <el-aside :width="ASIDE_WIDTH" class="app-layout__aside">
      <div class="app-layout__brand">{{ APP_TITLE }}</div>
      <el-menu router :default-active="route.path">
        <el-menu-item index="/demo/greet">问候示例</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="app-layout__header">{{ route.meta.title }}</el-header>
      <el-main class="app-layout__main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.app-layout {
  height: 100vh;
}

.app-layout__aside {
  background: var(--app-color-surface);
  border-right: 1px solid var(--app-color-border);
}

.app-layout__brand {
  height: var(--app-header-height);
  line-height: var(--app-header-height);
  padding: 0 var(--app-space-lg);
  font-weight: 600;
}

.app-layout__header {
  height: var(--app-header-height);
  line-height: var(--app-header-height);
  background: var(--app-color-surface);
  border-bottom: 1px solid var(--app-color-border);
}

.app-layout__main {
  background: var(--app-color-page);
}
</style>
