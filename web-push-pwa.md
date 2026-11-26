# 主屏幕 Web Push 标准方案（苹果 / PWA）

通用架构约束：面向「加到主屏幕的 Web App + 系统通知栏」。**禁止**写入具体业务单据名、角色名、事件码；业务只挂在项目消息目录与投递总线。

升格时机：要做手机系统通知、或已有事件总线要加苹果通道。选型 / 写前后端 AGENT 时读本文件。

## 1. 技术栈（定案）

| 层 | 选用 | 说明 |
|---|---|---|
| 协议 | **Web Push** + **VAPID** | 浏览器 Push Service（含苹果 `web.push.apple.com`） |
| 服务端库 | 成熟 Web Push 客户端（例 Go：`webpush-go`） | 负责加密载荷与 VAPID JWT；勿自造协议 |
| 客户端 | **Service Worker** + Push API + Notification API | 必须可展示系统通知 |
| 载体 | **HTTPS** + **加到主屏幕 / standalone** | 苹果：普通 Safari 标签页不可当作已通过依据；须主屏幕图标进入 |
| 密钥 | `vapidPublicKey` / `vapidPrivateKey` / `subject` 进现场 config | **不入库**；公钥可下发前端，私钥只服务端 |
| 并存通道 | 可选原生推送（个推等）与 Web Push **并列** | 各有设备表；同一投递总线可双发，禁止两套收件人算法 |

## 2. 数据模型（跟登录账号）

订阅表（模式随项目，常在主数据/core）：

| 列 | 约束 |
|---|---|
| `user_id` | 登录用户主键；账号删除级联清理 |
| `endpoint` | Push Service URL；**全局唯一** |
| `p256dh` / `auth` | 客户端密钥（base64url） |
| `user_agent` | 排障用 |
| `created_at` / `updated_at` | 首次 / 最近 |

规则：

1. **按 endpoint upsert**：同一设备改登账号 → 改绑到当前用户并刷新密钥，禁止一人一设备多行脏数据。
2. **推送服务 404/410 → 删行**：写路径清理失效订阅，避免反复失败。
3. **查绑定** = 订阅表 JOIN 用户表；无行 = 未开通或已退订。
4. 新表须纳入**工具账号**（Navicat 等）与运行账号的幂等 GRANT / DEFAULT PRIVILEGES，避免客户端「没有权限」。

## 3. 精准推送（禁止广播）

唯一口径：**事件收件人 → 登录用户 ID 集合 → 只向这些 ID 的订阅发**。

```text
业务写成功
  → 投递总线 DeliverEvent(eventCode, vars)   // 失败只打日志，不回滚业务
    → 与钉钉/邮件/短信同一套「收方人」解析
    → 人员/外部账号映射到已绑登录 user_id（未绑静默跳过）
    → SendToUsers(userIds, title, body, openURL)
         → WHERE user_id IN (...) 取订阅
         → 逐条 Web Push；无订阅 / 未配 VAPID = 静默 0 条
```

硬约束：

1. **不做全站广播**、不做「有订阅就全发」。
2. 收件人算法与其它通知渠道**同源**；Web Push 只多一步「人 → 登录账号 → 订阅」。
3. 业务写路径与投递解耦：单据已成功则投递失败不得让接口失败。
4. 测试接口只打**当前登录用户**的订阅，禁止测通路时全员推。

## 4. 深链（点通知进业务页）

### 4.1 载荷

JSON 最小集：`title` / `body` / `url`。

- `url` 必须是**同源相对路径**（含 query），例 `/module/page?openId=…&focusNo=…`。
- 服务端若拼了绝对 URL，发送前**收成 path+query**（剥 origin），供 SW 在 PWA 内打开。

### 4.2 事件登记

消息目录为每条事件登记：

| 字段 | 含义 |
|---|---|
| `openPath` | 落地页路由（须在**收方角色**可进的模块内） |
| 打开方式 | `openId`（精确开单）/ `focusNo`（单号兜底）等；**禁止只落到列表 keyword 误开兄弟单** |
| 模板变量 | 供拼 query 的单据 id / 单号 |

回执类事件：深链打开**收方日常办理的本域单据**，不要打开对方无权限的他域页。

### 4.3 Service Worker

1. `push`：解析 JSON → `showNotification`；`data.url` 写入 notification.data。苹果要求可见通知（`userVisibleOnly`）。
2. `notificationclick`：
   - 优先 `clients.matchAll` 找**同源已开窗** → `focus` + `postMessage({ type, url })`；
   - 否则 `clients.openWindow(绝对 URL)` 冷启动。
   - **不要依赖** `client.navigate`（iOS 常不可用）。
3. SW 版本变更后须 `skipWaiting` + `clients.claim`，避免旧 SW 丢深链逻辑。

### 4.4 前端页

1. 注册 SW 后监听 `message`：收到约定 type → 用与站内导航**同一套**打开函数（路由 + query），保证与铃铛/待办深链同口径。
2. 已登录会话下点开应直达目标；未登录先登录再消费待打开 URL（项目自定，须可验收）。

## 5. 开通与 UX（面向操作者）

| 步骤 | 要点 |
|---|---|
| 前置 | HTTPS；用户从**主屏幕图标**进入；系统设置允许该 Web App 通知 |
| 开启 | 前端 `Notification.requestPermission` → `pushManager.subscribe(applicationServerKey)` → `POST` 存订阅 |
| 测试 | 仅当前账号试推；成功后可藏「测试」或按账号记测通，避免重复打扰 |
| 已授权再进 | OS 已 granted 时可静默重绑订阅，不必反复点「开启」 |
| 文案 | 面向操作者；禁内部黑话 |

## 6. VAPID 与排障雷区

1. **`subject` 勿双写 `mailto:`**：部分库会对非 `https:` 值自动加 `mailto:`；配置若已带前缀会变成 `mailto:mailto:…`，苹果 JWT 403。入库/配置层做归一化（剥一层或统一用 `https://站点`）。
2. 假 endpoint / 过期订阅 → failed 计数 + 删行；勿当业务逻辑错误回滚。
3. 本机 `http://127.0.0.1` **不能**当苹果通过依据。
4. 交叉编译部署：目标机 OS/ARCH 必须匹配，否则 Exec format error。

## 7. 写入 harness 时落点

| 落点 | 写什么 |
|---|---|
| 根 AGENTS / 扩展索引 | 一行：主屏幕 Web Push 标准见本 skill；项目细节指针 |
| 后端 AGENT | 投递总线、`SendToUsers`、订阅表、VAPID config、失败不回滚写路径 |
| 前端 AGENT | SW 唯一入口、订阅/测试 UX、`postMessage` 与站内导航同口径 |
| 数据 AGENT / 说明书 | 订阅表字段；密钥不入库；工具账号 GRANT |
| 架构图 | 可选补进容器/部署：Push Service 外呼；密钥在 config |
| 项目特化 | 仅事件目录、openPath 映射、收方模块——**禁止**把本标准正文抄进特化 |

## 8. 验收清单（通用）

- [ ] 仅收方人设备收到；无关账号无通知
- [ ] 未开通 / 未绑登录账号 → 静默跳过，业务写仍成功
- [ ] 点通知打开约定页，且带精确定位参数（非误开列表兄弟行）
- [ ] 深链页在收方权限范围内
- [ ] 失效订阅被清理；VAPID 未配时不炸写路径
- [ ] 主屏幕 + HTTPS 路径可复测；文档写明苹果限制

## 9. 明确不做

- 不把 Web Push 当通用 BPM / 站内信替代品（站内信可并存，通道分开）。
- 不用可视化推送编排器充当收件人真相。
- 不为「省事」广播；不为测通路写死全员 user_id。
- 不在 skill / 通用 AGENT 里登记具体业务事件码与单据名。
