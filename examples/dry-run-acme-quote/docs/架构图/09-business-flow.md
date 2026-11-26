# 09 业务主链

```mermaid
flowchart LR
  Inquiry[询价单] --> Quote[报价单]
  Quote --> Confirm[客户确认]
  Confirm --> Archive[归档草稿]
```

报价确认→归档草稿：自动下推（无分批决策）。询价→报价：手动。进度现算。
