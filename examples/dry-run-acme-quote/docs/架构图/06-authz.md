# 06 权限

```mermaid
flowchart TB
  Login[登录] --> PagePerm[页面权限]
  PagePerm --> Menu[侧栏]
  PagePerm --> Scope[数据范围]
  Scope --> Staff[业务员按bill_manager]
  Scope --> LeadFull[主管全量]
```
