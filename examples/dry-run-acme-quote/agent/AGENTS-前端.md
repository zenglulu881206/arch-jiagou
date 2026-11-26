# 通用前端规则

> **硬门槛**：① 脚手架目录树 + 职责/存放路径表；② **全站 UI 统一表**；③ **PC / 手机（H5）策略表**。缺任一块视为未完成。  
> UI 细则专册：[frontend-ui.md](skill:arch-jiagou/frontend-ui.md)（举例非穷举）。项目特化不写本文件。

## 技术边界

- 栈：`Vue 3 + TypeScript + Element Plus 2.14 + Vite（create-vue 3.24.0）`（默认 Vue 3 + TypeScript + Element Plus + Vite）
- 应用根：`vue/`（默认 `vue/`）
- 写/改前核对真实脚手架；复用优先；基础控件优先 Element Plus
- 界面面向操作者；业务数字只展示后端源头结果
- 架构图：`docs/架构图/04-frontend-shell.md`

## 标准应用脚手架（必须声明）

由 `create-vue --bare` 官方基线 + 经验增量生成（来源见 skill `scaffold/vue3.md`）。树中 `[官]` = 官方 init 产物，`[增]` = 经验增量，`[改]` = 覆盖过的官方文件。

```text
vue//
|-- index.html / package.json / tsconfig*.json / env.d.ts   # [官]
|-- eslint.config.ts           # [改] 仅放开 views/**/index.vue 的多词组件名规则
|-- .prettierrc.json / .oxlintrc.json                       # [官] 格式与 lint 以此为准
|-- vite.config.ts             # [改] 端口固定 + /api 代理到后端
|-- .npmrc                     # [增] npmmirror 镜像
|-- public/                    # [官]
`-- src/
    |-- main.ts / App.vue      # [改] 注册 router、Element Plus（中文）、styles 入口
    |-- router/index.ts        # [改] 业务页挂在 AppLayout 下
    |-- layouts/AppLayout.vue  # [增] 全站唯一壳（PC 侧栏，手机汉堡也在这里）
    |-- views/<模块>/<功能>/index.vue   # [增] 页面；单页私有组件放同目录 components/
    |-- api/request.ts         # [增] 全站唯一请求入口
    |-- api/<模块>/            # [增] 接口函数，与 views/<模块> 对应
    |-- model/                 # [增] 与后端 Req/Res 对应的类型
    |-- components/common/     # [增] 全站统一样式组件（PageCard、图标按钮、弹窗标题…）
    |-- components/            # [增] 业务组件（选择器、单据行…）
    |-- composables/           # [增] useXxx.ts，带响应式状态的复用逻辑
    |-- utils/                 # [增] 纯函数工具（debounce…）
    |-- constants/             # [增] 常量（壳尺寸、系统名、分页档位）
    `-- styles/                # [增] tokens.css 设计令牌 + index.css 唯一入口 + 窄屏单文件
```

## 目录职责与新功能落点

| 目录 | 放什么 | 禁止 |
|---|---|---|
| `layouts/` | 唯一外壳 | 各页复制侧栏/顶栏 |
| `views/<模块>/<功能>/` | 页面编排，入口 `index.vue` | 散落 URL；页内另写请求 |
| `api/<模块>/` | 接口函数，只经 `api/request.ts` | 重造 request / 第二个 fetch 封装 |
| `model/` | 接口类型 | 放逻辑 |
| `components/common/` | 统一样式组件 | 调业务接口 |
| `components/` | 业务复用组件 | 硬编码单页 API |
| `composables/` | 带状态的复用逻辑 | 放纯函数 |
| `utils/` | 纯函数 | 放 ref / 生命周期 |
| `constants/` | 常量 | 业务字典（来自后端） |
| `styles/` | 令牌与全站皮 | 业务页平行皮肤；写死色值 |

新功能：`views/<模块>/<功能>/index.vue` + `api/<模块>/` + `model/` + 路由；全站观感只改 `styles/` / `layouts/` / `components/common/`。

## 全站 UI 统一（举例，按项目扩展）

生成时填写本项目**唯一入口文件/组件**（下表「落点」列）。

| 类别 | 统一什么（举例） | 本项目落点 |
|---|---|---|
| Header / 顶栏 | 高度、全局搜索、消息、用户区 | `vue/src/layouts/AppLayout.vue`（el-header） |
| 侧边栏 | 菜单与权限同源、折叠 | `vue/src/layouts/AppLayout.vue`（el-aside + el-menu） |
| 底栏 / 分页 | 摘要+pager、默认 page size | 首个列表页时建 `components/common/ListPager.vue` 并回填本格 |
| 按钮 | 主/次/行内图标钮 | Element Plus `el-button`；图标钮首次出现时建 `components/common/IconActionButton.vue` |
| 消息 / 加载 | Toast、全屏加载 | `vue/src/api/request.ts`（ElMessage 统一报错） |
| 表格 | 字号、表头、对齐、排序列宽 | `el-table`；公共表格皮首次出现时建 `styles/table.css` |
| 筛选栏 | 间距与控件高度 | 首个筛选栏时建 `components/common/FilterBar.vue` |
| 弹窗 / 抽屉 | 三类壳、宽度档位、遮罩关 | 首个弹窗时建 `styles/dialog.css`（新建编辑 / 查看 / 选择三类） |
| 单据表单 | 信息卡、产品行、进度条 | 首张单据（报价单）时建 `styles/doc-form.css` |
| 列表外壳 | 铺满、表体滚、底栏钉底 | `vue/src/components/common/PageCard.vue` |
| （其它） | 页签/KPI/上传/树… | 先检索 styles 再扩展本表 |

禁止：为图省事在单页 scoped 复制一套平行 class。

## PC / 手机端（举例，按项目扩展）

| 端 | 策略（举例） | 本项目约定 |
|---|---|---|
| **PC** | 表体内部滚+底栏钉底；抽屉宽度视口档位；短列定宽、长列吃剩余宽；大表分页+列设置 | 表体内部滚动 + 底栏钉底；抽屉宽度按视口分档 |
| **手机 H5 壳** | 断点（如 ≤768）；侧栏进汉堡；顶栏简化；**只认唯一 layouts 壳** | `vue/src/layouts/AppLayout.vue`（≤768 侧栏进汉堡） |
| **窄屏样式** | 列表/筛选/表/弹窗/单据等窄屏规则集中单文件，main 末引入 | `vue/src/styles/mobile-h5.css`（首次做窄屏时建，`styles/index.css` 末尾 @import） |
| **宽表数据多** | **横向滑动**看全列；慎改卡片列表（易丢对齐与批量） | 宽表横向滑动，不改卡片列表 |
| **触控** | 可滚层、禁外层裁切无滚动；抽屉近全屏 | 同窄屏入口 |

双端验收：主列表 + 开抽屉在 PC 与窄屏各走一遍（见测试 AGENT「样式统一」）。

## 工程横切（举例，按项目扩展；细则见 frontend-engineering.md）

| 类别 | 本项目唯一入口 / 口径 | 落点 |
|---|---|---|
| 分页 / 列表口径 | 唯一 pager；服务端 / 本地分页；筛选重置页码 | `vue/src/constants/` 下建 `pager.ts`（首个列表页时） |
| 异步请求 / 竞态 | 统一 request 封装；在途取消 / 过期响应忽略；加载三态 | `vue/src/api/request.ts` |
| 队列 / 长任务 | 批量提交口径；轮询 / SSE / 推送同源；离页取消 | 暂无长任务；出现导入/批量时在 `composables/` 建唯一入口 |
| 鉴权态 | token 刷新；路由守卫；401 回跳；范围判断以后端为准 | `vue/src/router/index.ts` beforeEach + `api/request.ts` 401 处理（登录功能时建） |
| 防抖 / 节流 / 防重 | 防抖节流工具入口；提交禁用 + 幂等键；离页清定时器 | `vue/src/utils/debounce.ts` |
| 状态 / 缓存 | 服务端为真相；字典缓存失效口径；共享状态唯一 store | 服务端为真相；不引入 Pinia（选型 B2） |

禁止：页面直连第二套请求实例；旧响应覆盖新数据；本地平行维护业务数字；各页自造防抖定时器。

## 组织硬约束（摘要）

1. 缺脚手架先落地最小树。  
2. 禁止前端写死业务数据/字典/菜单清单（举例文案除外）。  
3. 长链只渲染后端 `flow.steps`；跨模块进度只读。  
4. UI 类别未覆盖的新控件：先补本表落点，再实现。

## 验证

- `package.json` 类型检查/构建；交互与双端样式见 `agent/AGENTS-测试.md`。
