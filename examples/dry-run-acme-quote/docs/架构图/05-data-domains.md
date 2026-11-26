# 05 数据域

```mermaid
flowchart LR
  subgraph db [acme_quote]
    core[core]
    sales[sales]
    mig[schema_migration]
  end
```

`public` 空。单据头 `bill_` / 行 `line_`；数据ID nanoid24。
