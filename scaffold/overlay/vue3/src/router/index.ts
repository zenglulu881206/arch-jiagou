import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'

/**
 * 路由表：业务页都挂在 AppLayout 下，路径与 views/<模块>/<功能>/ 一致。
 * meta.title 显示在顶栏；鉴权守卫后续在本文件 beforeEach 统一加。
 */
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: AppLayout,
      redirect: '/demo/greet',
      children: [
        {
          path: 'demo/greet',
          component: () => import('@/views/demo/greet/index.vue'),
          meta: { title: '问候示例' },
        },
      ],
    },
  ],
})

export default router
