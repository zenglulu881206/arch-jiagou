# 通用后端规则

> 脚手架目录声明是**硬门槛**：无分层树 + 职责表，后端 harness 视为未完成。默认对齐 **Go + GoFrame**（`erp-go-vue-pg`），目录由 skill `scaffold/init.py` 生成；其它栈须声明等价分层（契约→适配→领域→持久化），禁止「一切塞 handler」。项目特化不写本文件。

## 技术边界

- 栈：`{{BE_STACK}}`（默认 Go + GoFrame）
- 应用根：`{{BE_ROOT}}`（默认 `server/`）
- 写/改前读本目录 README / 真实脚手架；不假设空目录
- 架构图：`docs/架构图/03-backend-layers.md`
- 计算只调公式说明书源头；写接口做上下游双闸（流程族）

## 标准应用脚手架（必须声明 · GoFrame）

由 `gf init` 官方基线 + 经验增量生成（来源见 skill `scaffold/goframe.md`）。树中 `[官]` = 官方 init 产物，`[增]` = 经验增量。

```text
{{BE_ROOT}}/
|-- main.go                    # [官] 进程入口；[增] 匿名引入 pgsql 驱动
|-- go.mod / go.sum / Makefile # [官]
|-- hack/                      # [官] gf 工具配置（gen dao 等）
|-- manifest/config/
|   |-- config.example.yaml    # [增] 配置示例入库；config.yaml 本机生成、gitignore
|-- migrations/                # [增] 结构迁移 SQL：NNNN_说明.sql；禁自动删业务数据
|-- resource/                  # [官] 静态资源（如有）
|-- api/
|   |-- health/                # [增] 存活探针 GET /api/health
|   `-- <业务>/
|       |-- <业务>.go          # [增] 接口集合 I<业务>V1，手工维护
|       `-- v1/<业务>.go       # [增] 本业务全部 Req/Res、路由元信息，一个业务一个文件
`-- internal/
    |-- cmd/cmd.go             # [官] 启动；[增] 业务接口统一挂 /api，启动 Ensure 挂这里
    |-- consts/                # [官] 常量
    |-- controller/<业务>/<业务>.go   # [增] 一个业务一个文件；方法只转调 logic 同名函数
    |-- logic/
    |   |-- common/            # [增] 跨业务、带业务含义的公共代码（错误码、状态筛选）
    |   `-- <业务>/            # [增] 与 api/<业务> 同名
    |       |-- <业务>.go      #       包说明 + 本业务共用常量/小工具
    |       |-- <场景>.go      #       一个业务场景一个文件（confirm/merge/import/progress…）
    |       `-- <场景>_test.go #       测试同目录
    |-- dao/  model/{entity,do}/       # [官] gf gen dao 生成，不手改
    |-- middleware/            # [增] 鉴权、数据范围、日志中间件
    |-- packed/                # [官] 资源打包
    `-- pkg/                   # [增] 无业务色彩的库（nanoid、加解密…）；替代官方 utility/
        `-- webhost/           # [增] 单 exe 交付时后端托管前端（config web.root 为空则不托管）
```

## 分层职责（必须遵守）

| 层 | 路径 | 职责 | 禁止 |
|---|---|---|---|
| API 契约 | `api/<业务>/v1/<业务>.go` | Req/Res、路由元数据、入参校验标签 | 塞业务逻辑或 SQL |
| 接口集合 | `api/<业务>/<业务>.go` | `I<业务>V1`，controller 实现它 | 漏登记新方法 |
| Controller | `internal/controller/<业务>/<业务>.go` | HTTP 适配，一行转调 logic | 拼 SQL、写规则、直访 DAO |
| Logic | `internal/logic/<业务>/<场景>.go` | 校验、流程、事务、调 DAO/源头函数；函数直接收发 v1 Req/Res | 一个文件塞全部场景；跨业务复制代码 |
| 公共逻辑 | `internal/logic/common/` | 错误码、跨业务共用规则 | 无业务色彩的工具 |
| DAO/实体 | `internal/dao/`、`internal/model/entity|do/` | 持久化访问（生成） | 业务编排；手改生成文件 |
| Cmd | `internal/cmd/` | 启动、路由注册、启动 Ensure | 写具体业务规则正文 |
| Migrations | `migrations/` | DDL + 幂等运行种子 | 客户业务补数、DELETE/TRUNCATE 自动跑 |

调用链：**HTTP → api 契约 → controller → logic → dao → DB**。不设 `service/` 层（官方空目录保留 `.gitkeep`）；确需接口隔离时在选型表轴 1 写明再启用。

## 新业务存放路径（必须遵守）

| 交付物 | 路径 |
|---|---|
| 接口契约 | `api/<业务>/v1/<业务>.go` |
| 接口集合 | `api/<业务>/<业务>.go` |
| HTTP 适配 | `internal/controller/<业务>/<业务>.go`，并在 `internal/cmd/cmd.go` Bind |
| 业务场景 | `internal/logic/<业务>/<场景>.go` + `<场景>_test.go` |
| 跨业务公共 | `internal/logic/common/`（带业务含义）或 `internal/pkg/`（无业务色彩） |
| 表访问 | `gf gen dao` → `internal/dao/` + `internal/model/entity|do` |
| 结构迁移 | `migrations/NNNN_说明.sql` |

推荐顺序：定 v1 契约 → 接口集合加方法 → logic 场景文件 + 测试 → controller 转调 → cmd 绑定。

## 存放与生成规范

1. 不跑 `gf gen ctrl` / `gf gen service`：前者按方法拆 controller 文件，后者多一层注册，均与本项目分层冲突。`gf gen dao` 照常用。
2. 自动生成文件（dao/entity/do）跟生成器，不手改。
3. API DTO ≠ DB entity：不要混用或重复维护两套同义字段。
4. 统一响应用官方 `ghttp.MiddlewareHandlerResponse`（`{code,message,data}`）；业务错误只用 `logic/common` 的错误码构造，文案面向操作者。
5. 库存过账/占用等有唯一源头的，只调登记函数（见数据 AGENT / 公式说明书）。

## 工程横切（举例，按项目扩展；细则见 backend-engineering.md）

| 类别 | 本项目口径 / 落点 | 禁令 |
|---|---|---|
| 并发与一致性 | 写接口幂等键 / 唯一约束；竞争资源唯一过账入口 + 锁；事务边界；协程规范 | 读-改-写无保护；长事务包远程调用；泄露协程 |
| 负载与资源 | 连接池上限与超时；限流；资源异常路径释放；大结果集分页 / 流式；耗时操作队列化 | 无超时下游调用；全量加载进内存；主请求阻塞跑后台任务 |
| 高效 | 禁 N+1 批量取数；索引与分页口径；计算只调源头函数；字段按需返回；慢路径阈值 | 循环内查库；平行 SQL 凑占用 / 余量；SELECT * |
| 对抗审查 / 安全 | 鉴权 + 数据范围后端强制；水平 / 垂直越权校验；入参契约校验；防重放；错误与日志脱敏；操作留痕 | 前端隐藏当鉴权；内部堆栈 / 密钥回传前端；日志记明文敏感信息 |

## 非 GoFrame 时

在本文件用同等表格声明：接口契约目录、HTTP 适配层、领域服务、仓储/DAO、迁移目录；必须仍满足「契约与实现分离、适配层不写 SQL」。

## 验证提示

- `gofmt`、相关 `go test`、构建；测试库与测完即清见测试 AGENT。
