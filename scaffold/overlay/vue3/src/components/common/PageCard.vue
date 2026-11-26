<script setup lang="ts">
/** 全站统一页面卡片：标题区 + 操作区 + 内容区。各页用它包内容，不在页内另写卡片样式。 */
defineProps<{
  title: string
}>()
</script>

<template>
  <section class="page-card">
    <header class="page-card__header">
      <h2 class="page-card__title">{{ title }}</h2>
      <div class="page-card__actions">
        <slot name="actions" />
      </div>
    </header>
    <div class="page-card__body">
      <slot />
    </div>
  </section>
</template>

<style scoped>
.page-card {
  background: var(--app-color-surface);
  border-radius: var(--app-radius);
  padding: var(--app-space-lg);
}

.page-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--app-space-md);
}

.page-card__title {
  margin: 0;
  font-size: var(--app-font-size-lg);
}
</style>
