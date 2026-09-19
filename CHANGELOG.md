# 更新日志

## v1.0.1

### 修复

1. **检查更新设置里模式选不了** — `DownloadDialog` 的初始化 effect 依赖了每次渲染都重新创建的 `visibleModes` / `variantsByMode`，父组件重渲染时会把刚选中的模式重置回初始值：点 API 后界面闪一下又弹回 browser，实际仍以 browser 模式发起检查更新。改为仅在对话框打开时同步一次
2. **`BookCard` 导出文件名不同步** — `useCallback` 缺 `title` 依赖，书名变化后 Android 导出用的仍是旧文件名
3. **`DetailPage` 章节流可能漏加载** — effect 缺 `isRemote` 依赖，`compareMode` 下 `isRemote` 变化不会重新拉取
4. **`SearchBar` URL 模式不纠正模式** — 漏 `urlHideApi` 依赖

### 重构

1. **拆分 Toast / Button 的非组件导出** — 拆出 `toast-context.ts` 与 `button-variants.ts`，修复 Vite Fast Refresh 失效（改该文件时整页刷新而非热更新）；`oxlint` 警告 8 -> 0

## v1.0.0

首个公开版本：仅内置 fanqie 书源。
