# composables

带响应式状态或生命周期的可复用逻辑，命名 `useXxx.ts`（如 `useListQuery.ts`）。

- 纯函数（无 ref、无生命周期）放 `utils/`。
- 写前先检索本目录，同类能力只留一个入口。
