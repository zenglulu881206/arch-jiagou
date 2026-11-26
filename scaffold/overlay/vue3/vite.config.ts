import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

/** 后端地址：开发与预览都把 /api 代理到本机后端，前端代码只写相对路径 /api/...。 */
const apiProxy = {
  '/api': 'http://127.0.0.1:__APP_PORT__',
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  build: {
    // 浏览器下限来自选型题 E4；Win7 上 Chrome 最高 109，低于 Vite 默认目标（Chrome 111）
    target: __FE_BUILD_TARGET__,
  },
  server: {
    port: __FE_PORT__,
    strictPort: true,
    proxy: apiProxy,
  },
  preview: {
    port: __FE_PORT__,
    strictPort: true,
    proxy: apiProxy,
  },
})
