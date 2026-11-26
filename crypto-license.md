# 加解密与授权（分场景）

禁止「全站一个算法」；按场景选型并画进 `07-license-crypto.md`。

| 场景 | 推荐 | 禁止 |
|---|---|---|
| 传输 | HTTPS/TLS（nginx 终结或前置） | 明文公网传口令 |
| 登录密码存储 | bcrypt（或项目已有等价慢哈希） | 明文、可逆加密当哈希 |
| 会话 | 服务端 session + Bearer token | 把长期密钥塞 localStorage 当唯一防线 |
| 申请码（机器码外传） | 公钥 RSA-OAEP+SHA256 加密，现场只出密文 | 明文机器码当申请码发出 |
| License 文件 | 私钥签发（PKCS1v15+SHA256 等与验签对齐）；公钥随运行包装 | 私钥打进客户包或进 git |
| 字段级业务加密 | 仅当合规要求；密钥走环境/独立文件，config 深合并保留 | 业务库当密钥库 |
| 开发覆盖机器码 | 仅本地校验比对，不得当作申请码 | 用覆盖值申请正式 license |

## 密钥边界（硬）

```text
admin/encrypt/ca.key     → 只在开发机，不进包、不入库
server/.../public_key.pem → 随包，只验签
license.lic               → 现场上传，绑定机器码
```

## 与 erp-go-vue-pg 对齐要点

- 申请码：运行时公钥加密明文机器码 → hex
- 签发：admin 私钥解密申请码 → 写入 license.data.machine_code → 签名
- 校验：机器码比对 + 验签；可缓存日检；未授权是否阻断启动由项目定（样板 ERP：不阻断启动便于先部署后上传）
