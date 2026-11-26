# 后端脚手架：GoFrame 官方 init + 经验增量

脚手架 = **官方 init 基线** + **经验增量（overlay）**。执行入口 `scaffold/init.py`，验收入口 `scaffold/verify.py`，增量实物在 `scaffold/overlay/goframe/`。

## 1. 基线表（官方 init）

| 项 | 值 | 说明 |
|---|---|---|
| 命令 | `gf init <dir> -g <module>` | 单仓模板 |
| gf CLI | `v2.10.0` 实测 | CLI 内置模板给的框架版本是 v2.7.1、`go 1.18`，偏旧 |
| 框架版本 | init 后 `go get github.com/gogf/gf/v2@<goframe>`（默认 `v2.10.5`） | 统一钉到选型表版本 |
| Go | `go 1.25` 起（gf v2.10.5 + pgsql 驱动要求） | |
| 数据库驱动 | `github.com/gogf/gf/contrib/drivers/pgsql/v2@<goframe>`，`main.go` 匿名引入 | |
| 镜像 | 未设置时 `GOPROXY=https://goproxy.cn,direct` | |
| 数据库驱动选择 | `SELECTION.database.engine`：`pgsql`（默认）或 `sqlite`（纯 Go 驱动 glebarez，免 CGO） | SQLite 库文件放 `data/` 并 gitignore |
| Win7 / Server 2008 线 | `deploy.os=windows` 且版本 ≤ 8 / 2012 时：GoFrame 须 v2.7.x；init.py 自动 `go mod edit -go=1.20` 并钉 x/sys v0.15.0、otel / metric / sdk / trace v1.21.0（照 Win7 内网项目实机组合）；发布包用 Go 1.20.x 编译 | 已实测：Go 1.20.14 下 vet、test、verify 全过，交叉编译出 Windows exe；只钉 otel 不钉 sdk 会编译失败；Win7 实机运行待验证 |
| 产出（官方） | `main.go`、`go.mod`、`Makefile`、`hack/`、`api/hello`、`internal/{cmd,consts,controller/hello,dao,logic,model/{do,entity},packed,service}`、`manifest/{config,deploy,docker,i18n,protobuf}`、`resource/`、`utility/` | |
| 统一响应 | 直接用官方 `ghttp.MiddlewareHandlerResponse`：`{code,message,data}` | 不另写平行包装 |

## 2. 增量表（经验）

| 路径 | 用途 | 种子文件 | 规则 |
|---|---|---|---|
| `api/<业务>/v1/<业务>.go` | 本业务全部 Req/Res 与路由元信息，一个业务一个文件 | `api/demo/v1/demo.go` | 不写业务逻辑 |
| `api/<业务>/<业务>.go` | 接口集合 `I<业务>V1`，手工维护 | `api/demo/demo.go` | 新增场景同步加方法 |
| `internal/controller/<业务>/<业务>.go` | HTTP 适配，一个业务一个文件；每个方法一行转调 logic 同名函数 | `controller/demo/demo.go` | 不写 SQL、不写规则 |
| `internal/logic/<业务>/` | 业务实现，与 api 同名；**一个业务场景一个文件**，函数直接收发 v1 Req/Res | `demo.go`（包说明）、`greet.go`（场景）、`greet_test.go` | 测试同目录；场景文件名对应动作（confirm、merge、import、progress…） |
| `internal/logic/common/` | 跨业务、带业务含义的公共代码（错误码、状态筛选…） | `bizerror.go` | 不放无业务色彩的工具 |
| `internal/pkg/` | 无业务色彩的库（ID、加解密、文件…） | `README.md` | 不引用 logic/dao |
| `internal/pkg/webhost/` | 后端进程托管前端构建产物，history 路由回 index.html，`/api` 404 不吞 | `webhost.go` | 只在 `config web.root` 非空时生效；`deploy.shape=single-binary` 时 init.py 填 `resource/public/html` |
| `internal/middleware/` | 鉴权、数据范围、日志等中间件 | `README.md` | 鉴权必须后端强制 |
| `internal/cmd/cmd.go` | 路由注册：业务接口统一挂 `/api`；启动 Ensure 挂这里 | `cmd.go` | 不写业务规则正文 |
| `api/health` + `controller/health` | 存活探针 `GET /api/health` | 同名文件 | 不碰库 |
| `manifest/config/config.example.yaml` | 配置示例（入库）；init 复制成 `config.yaml`（gitignore） | 同名 | 部署时保留现场配置，按示例深合并补缺键 |
| `migrations/` | 结构迁移 SQL，`NNNN_说明.sql` | `0001_init_schema.sql`、`README.md` | 只 DDL + 幂等种子；执行器按项目选型 |

调用链：**HTTP → api 契约 → controller → logic → dao → DB**。

不用 `service/` 层，也不跑 `gf gen ctrl` / `gf gen service`：前者会按方法拆 controller 文件，后者会多一层接口注册，都和上面的“一业务一 controller 文件、logic 包函数直调”冲突。确需接口隔离（如多实现、mock）时，在选型表轴 1 写明再启用。DAO/实体仍用 `gf gen dao`。

## 3. 删改表（对官方产物）

| 官方文件 | 动作 | 原因 |
|---|---|---|
| `api/hello`、`internal/controller/hello` | 删除 | 官方示例 |
| `utility/` | 删除 | 统一用 `internal/pkg/`，避免两个工具目录 |
| `manifest/docker`、`manifest/deploy`（kustomize） | 默认删除；`SELECTION.backend.keep_docker` / `keep_kustomize` 为 true 时保留 | 默认部署是 nginx + 本机二进制（轴 7） |
| `manifest/config/config.yaml` | 删除，改由 `config.example.yaml` 复制生成并 gitignore | 官方示例是 MySQL 且凭据入库 |
| `main.go` | 覆盖：加 pgsql 驱动匿名引入 | |
| `hack/config.yaml` | 覆盖：`gen dao` 连接改为 pgsql（占位密码 `CHANGE_ME`），删除 docker 段 | 官方示例是 MySQL |
| `internal/cmd/cmd.go` | 覆盖：路由前缀 `/api`，绑定 health 与业务 controller | |

## 4. Win7 实机验证包（init 之外的手工步骤）

本机没有 Win7 时，按下面打包，带到 Win7 64 位或 Server 2008 R2 上验证：

1. 用 Go 1.20.14（阿里云镜像 `mirrors.aliyun.com/golang/`）设 `GOROOT`、`GOTOOLCHAIN=local`，在后端目录执行 `GOOS=windows GOARCH=amd64 go build -trimpath -ldflags "-s -w" -o server.exe .`。
2. 前端 `npm run build`，把 `dist/` 复制到 `resource/public/html/`。
3. 打包 `server.exe`、`manifest/config/config.yaml`、`resource/public/html/`、空 `data/`，加一个纯 ASCII 的启动 bat（Win7 的 cmd 读 UTF-8 bat 会乱码）和带 BOM 的 UTF-8 说明文件；文件名用英文（Win7 自带解压不认 UTF-8 文件名）。
4. 实机核对：健康检查、页面打开、问候正反例、F5 刷新不 404。

## 5. 验收（verify.py）

`go vet`、`go test`、`go build` 通过 → 起服后 `GET /api/health` 返回 `code=0,status=ok` → 前端经代理调 `/api/demo/greet` 成功；空名字被 `v:"required"` 校验拦下（code 51），只含空格的名字被 logic 拦下（业务错误码 1001）。
