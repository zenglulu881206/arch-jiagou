# 前端脚手架：Vue 3 官方 init + 经验增量

脚手架 = **官方 init 基线** + **经验增量（overlay）**。基线由官方维护、随版本升级；skill 只沉淀增量。
执行入口：`scaffold/init.py`（读 `SELECTION.json`）；验收入口：`scaffold/verify.py`。增量文件实物在 `scaffold/overlay/vue3/`。

## 1. 基线表（官方 init）

| 项 | 值 | 说明 |
|---|---|---|
| 命令 | `npx -y create-vue@<create_vue> <features> --bare <dir>` | `--bare` 不带官方示例页 |
| create-vue | `3.24.0`（`SELECTION.frontend.create_vue`） | 换版本须重跑 verify 并校对本表 |
| 默认 features | `--ts --router --eslint --prettier` | 访谈可加 `--pinia`、`--vitest`、`--playwright` |
| Node | `^22.18.0 \|\| >=24.12.0`（create-vue 3.24 的 engines） | |
| 产出（官方） | `index.html`、`package.json`、`vite.config.ts`、`tsconfig*.json`、`eslint.config.ts`、`.oxlintrc.json`、`.prettierrc.json`、`env.d.ts`、`public/`、`src/{main.ts,App.vue,router/index.ts}` | 版本 3.24.0 实测 |
| 镜像 | overlay 的 `.npmrc`：`registry=https://registry.npmmirror.com` | 官方源只作兜底 |
| UI 库 | `element-plus@<element_plus>`（默认 `2.14.8`），init 后单独安装 | 中文 locale 在 `main.ts` 注入 |
| 格式化 | 以官方 `.prettierrc.json` 为准（无分号、单引号、100 列）；init 末尾跑 `npm run format`、`npm run lint` | overlay 源文件已按此格式化 |

## 2. 增量表（经验）

| 路径 | 用途 | 种子文件 | 规则 |
|---|---|---|---|
| `src/layouts/` | 全站唯一外壳（顶栏 + 侧栏 + 内容区；手机端汉堡后续也在这里） | `AppLayout.vue` | 页面不复制侧栏/顶栏 |
| `src/views/<模块>/<功能>/` | 页面，一个功能一个目录，入口固定 `index.vue` | `views/demo/greet/index.vue` | 单页私有组件放同目录 `components/` |
| `src/api/<模块>/` | 接口函数，与 `views/<模块>/` 对应 | `api/demo/greet.ts` | 只经 `api/request.ts` 发请求 |
| `src/api/request.ts` | 全站唯一请求入口：解包 `{code,message,data}`，出错弹后端文案 | `request.ts` | 鉴权头、401、全屏加载只在这里扩展 |
| `src/model/` | 与后端 Req/Res 对应的 TS 类型 | `model/demo.ts` | 不放逻辑 |
| `src/components/common/` | 全站统一样式组件（页面卡片、图标按钮、弹窗标题、筛选控件…） | `PageCard.vue` | 不调业务接口 |
| `src/components/` 根 | 业务组件（选择器、单据行…） | `README.md` | 被第二个页面用到才提到这里 |
| `src/composables/` | 带响应式状态的复用逻辑 `useXxx.ts` | `README.md` | 纯函数放 utils |
| `src/utils/` | 纯函数工具（防抖、格式化…） | `debounce.ts` | 同类只留一个入口 |
| `src/constants/` | 常量（壳尺寸、分页档位、系统名） | `layout.ts` | 不放业务字典（字典来自后端） |
| `src/styles/` | 设计令牌 + 全站公共皮；`index.css` 是唯一入口 | `tokens.css`、`index.css` | 页面只用变量，不写死色值 |

## 3. 删改表（对官方产物）

| 官方文件 | 动作 | 原因 |
|---|---|---|
| `src/App.vue` | 覆盖为只放 `<router-view />` | 官方示例文案删除，壳交给 layouts |
| `src/main.ts` | 覆盖：注册 router、Element Plus（中文）、引入 `styles/index.css` | |
| `src/router/index.ts` | 覆盖：业务页挂在 `AppLayout` 下 | 官方 routes 为空 |
| `vite.config.ts` | 覆盖：保留官方 alias 与 devtools；加 `server`/`preview` 端口（`strictPort`）与 `/api` 代理；`build.target` 按选型 `clients.browser_min`（如 `chrome-109` → `chrome109`/`edge109`），未填用 Vite 默认（Chrome 111 起） | 前端代码只写相对 `/api/...`；Win7 上 Chrome 最高 109 |
| `eslint.config.ts` | 覆盖：在官方配置上只加一段，`src/views/**/index.vue` 关闭 `vue/multi-word-component-names` | 页面入口固定 `index.vue` 与官方规则冲突 |

## 4. 示例业务 demo

`views/demo`、`api/demo`、`model/demo.ts` 与后端 demo 一起演示一条完整调用链，`verify.py` 靠它验收。首个真实业务落地后整组删除。

## 5. 验收（verify.py）

`npm run build`（含 `vue-tsc` 类型检查）通过 → `vite preview` 起在约定端口 → 浏览器打开 `/demo/greet`：输入名字看到问候语；名字为空看到后端错误提示。
