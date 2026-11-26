# internal/pkg

无业务色彩的可复用库：ID 生成、加解密、文件、时间等。按能力分子包（如 `pkg/nanoid/`）。

- 禁止：引用 `logic/`、`service/`、`dao/`；写业务规则。
- 带业务含义但跨业务共用的代码放 `internal/logic/common/`。
- 本目录替代 gf init 默认的 `utility/`（已删除），避免两个工具目录并存。
