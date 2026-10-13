# 更新日志

## v4.5.2

> 本仓库版本号自此与主线 `novelbase.__version__` 对齐（此前为独立的 `1.0.x` 版本线，
> `v1.0.1` 及更早内容见文末）。本次为整体同步，含书源体系扁平化与 WebUI/CLI 收口。

### 新增

1. **书源体系扁平化** — 每个书源一个目录（`novelbase/sources/<name>/`），内含 `source.json`（`source_name` / `source_alias` / `source_group` / `common`）与 4 个能力文件（`search.py` / `novel_info.py` / `chapter_list.py` / `chapter_content.py`）。公开接口收敛为 `list_sources()` / `get_manifest()` / `capabilities()` / `resolve()` / `resolve_book_url()`；旧的 `platform` / `mode` / `variant` 概念与相关路由一并移除
2. **书源分组与别名** — `source.json` 可选 `source_alias`（显示名，未设回落 `source_name`）与 `source_group`（分组），用户层可覆盖；书源管理并入设置页（每源一个折叠条），`/sources` 仅重定向 `/settings`
3. **按所选书源搜索** — 前端搜索页支持「全选 / 按分组 / 未分组」与逐源复选（默认全选、不持久化），后端 `GET /download/search?sources=a,b,c` 接收逗号分隔的源名；URL 解析改为手动选源
4. **下载并发模型重做** — 三层并发：任务级 `download.max_workers`（默认 3，超额任务显示「排队中」）、书源级 `concurrency`（跨任务共享）、能力级 `delay`（出厂默认 `[0,0]`，即不限速）
5. **发行产物新增 Windows Nuitka exe** — `build-dist` 一次触发即产出 Windows portable / **Windows onefile exe** / Linux x64 / Linux arm64 / Termux portable
6. **新增「番茄·oiapi」书源** — 经第三方服务 `https://oiapi.net/api/FqRead` 获取番茄小说信息与章节（`api` 模式，与 `browser` / `requests` 模式并存）；接口 `key` 由用户在 `config/sites/fanqie-api-oiapi.yaml` 自备，仓库内为空占位

### 变更

1. **`search` 改为单源单结果** — `novelbase.search(source_name, query, …)` 只搜一个书源并返回该源第一条命中（无结果 → `None`）；多源并发与逐源兜底上移到调用方，源报错不再被静默吞掉
2. **书源启用开关废弃** — 不再有「启用 / 禁用」概念，默认参与集为全部书源

### 修复

1. **WebUI 导出 txt 失败** — 导出请求只发 `{enabled: true}`，后端默认文件名模板是遗留占位符 `{name}`，而 txt 导出器的合法占位符只有 `{title}` 等，`format()` 因此抛 `KeyError('name')`，界面提示只显示 `'name'`。现统一为 `{title}`
2. **Nuitka exe 读不到同目录的 `app_data`** — 路径定位原先只认 PyInstaller 的 `sys.frozen`（Nuitka 产物不设该属性），于是 exe 旁的配置目录永远读不到、首次初始化还写进临时解包目录。现统一到 `shared/paths.py`（onefile 优先读 `NUITKA_ONEFILE_DIRECTORY`）
3. **浏览器登录态每次启动重置** — 出厂默认 `user_data_dir` 为空使浏览器走匿名 context，登录不落盘；现默认持久化 profile
4. **串行下载时顺序仍乱** — 书源额度的等待队列不是 FIFO（超时重新入队导致顺序随机），改为交接式 FIFO
5. **前端 effect 依赖缺失**（详情页章节流、搜索栏 URL 模式等），以及 Vite Fast Refresh 失效（Toast / Button 的非组件导出拆分为独立文件）

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
