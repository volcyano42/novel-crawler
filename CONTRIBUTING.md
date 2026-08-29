# 为 novel-crawler 做贡献

感谢您对 novel-crawler 的兴趣！本文档帮助快速上手开发。

## 目录

- [前置条件](#前置条件)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [依赖方向](#依赖方向)
- [测试](#测试)
- [扩展开发](#扩展开发)
- [PR 流程](#pr-流程)

---

## 前置条件

- **Python 3.10+** — 后端与核心库（开发环境 3.13）
- **Node.js 20+ / npm** — 前端开发（当前环境 Node 24）
- **git** — 版本控制
- **Chromium**（可选）— `browser` 模式需要，`drissionpage` 会自动管理

## 快速开始

```bash
# 克隆
git clone https://github.com/volcyano42/novel-crawler.git
cd novel-crawler

# 安装后端依赖（可编辑安装）
pip install -e .

# 安装前端依赖
cd frontend
npm install
cd ..
```

运行方式：

```bash
python main.py                    # CLI 交互式菜单（委托 cli.interactive.main）
python cli.py search --platform fanqie "关键词"   # 非交互命令行（委托 cli.main）
python app.py                     # 一键启动前后端（默认 0.0.0.0:8000）
uvicorn backend.main:app --reload                # 单独起 Web 后端
cd frontend && npm run dev                       # 前端开发服务器（端口 5173）
```

## 项目结构

```
novel-crawler/
├── main.py                       # 交互式 CLI 入口（委托 cli.interactive.main）
├── cli.py                        # 非交互命令行入口（委托 cli.main）
├── app.py                        # 统一启动器（一键启动前后端，Ctrl+C 优雅关闭）
├── init_config.py                # 配置初始化（template/config → app_data/config）
├── requirements.txt              # 依赖清单（beautifulsoup4/lxml/playwright/fastapi/httpx/Pillow/PyYAML/...）
│
├── novelbase/                    # 核心库（source 驱动）
│   ├── core/
│   │   ├── downloader.py         # 门面：search / resolve_meta / resolve_chapter_list /
│   │   │                         #       resolve_chapter / export / get_source / list_sources
│   │   ├── engine.py             # Engine(ABC) + APIEngine/BrowserEngine/RequestsEngine
│   │   │                         #       + create_engine(options)（mode_map 分发）
│   │   ├── exceptions.py         # NovelDownloaderError / SourceNotFoundError / ParseError / ...
│   │   ├── options.py            # 配置数据类（Options/APIOptions/BrowserOptions/...）
│   │   └── storage.py            # LocalStorage（SQLite，每本小说独立 .db）
│   │
│   ├── models/novel.py           # 纯数据模型 Novel/Chapter/Chapters/Illustration/SearchResult
│   │
│   ├── sources/                  # 站点解析器（按 平台/模式/variant 组织）
│   │   └── fanqie/               #   番茄（browser/ requests/ api/oiapi/ api/rain/）
│   │       └── {mode}/{variant}/search.py, novel_info.py, chapter_list.py, chapter_content.py
│   │
│   ├── exporters/                # 导出器（纯函数，无类实例状态）
│   │   ├── txt.py                #   export() + TXTExportOptions
│   │   ├── epub.py               #   export() + EPUBExportOptions（含图片优化）
│   │   ├── img.py                #   export() + IMGExportOptions
│   │   └── base.py / contracts.py
│   │
│   ├── utils/
│   │   ├── build_manifest.py     # 生成 _manifest.py（Nuitka onefile 用）
│   │   ├── logger.py             # 日志系统
│   │   ├── hooks.py              # SourceHooks（来源钩子）
│   │   ├── encoding.py           # 编码检测
│   │   ├── urls.py               # canonical_book_url 等 URL 规范化
│   │   └── template_utils.py     # 模板工具
│   ├── source.py                 # 公共 API：capabilities / resolve / list_sources
│   └── sources/contracts.py      # Protocol 契约 + CAPABILITY_META（单一数据源）
│
├── cli/                          # CLI 层
│   ├── main.py                   #   非交互 argparse 命令（cli.py 委托于此）
│   ├── interactive.py            #   交互式主菜单（main.py 委托于此）
│   ├── config.py                 #   配置加载
│   ├── core.py                   #   下载/更新编排（纯非交互）
│   ├── menus.py / ui.py          #   交互菜单与界面
│   └── notify.py                 #   通知
│
├── backend/                      # Web 后端（FastAPI）
│   ├── main.py                   #   入口 + V2ResponseMiddleware（{ok, message, data} 包装）
│   ├── routers/                  #   download / storage / export / config / engine / history
│   ├── services/                 #   task_manager / engine_manager
│   └── schemas/                  #   pydantic 请求/响应模型
│
├── frontend/                     # Web 前端（React + TypeScript + Tailwind + shadcn/ui）
│   └── src/
│       ├── features/             #   bookshelf / detail / download / reader / settings
│       ├── hooks/                #   React Query hooks（useNovels/useConfig/...）
│       ├── api/                  #   endpoints.ts（API 函数）+ client.ts（fetch 封装）
│       ├── components/           #   UI 组件库
│       └── utils/                #   sessionCache / chapterCache
│
├── shared/                       # 跨端共享（config.py 配置加载 / user_data.py 用户库模板）
├── template/config/              # 默认配置模板（config.yaml + sites/*.yaml + formats/*.yaml + groups.yaml）
├── app_data/                     # 运行时数据（config/ storage/ exports/，gitignored）
├── scripts/                      # 构建脚本（build-portable/build-nuitka）+ check_public.py
├── tests/                        # 单元测试（280 passed / 2 skipped）
├── docs/                         # 子仓库 docs（历史遗留；权威文档在外层容器 docs/）
└── build-*.ps1 / build-*.sh      # 构建脚本（build-portable / build-nuitka）
```

## 依赖方向

项目遵循 **严格单向依赖**：

```
models/（纯数据模型，无业务依赖）
   ↓
utils/logger.py · utils/hooks.py（基础设施）
core/exceptions.py
   ↓
core/options.py（配置数据类，供 engine / exporters / API 层共用）
core/engine.py（三种引擎 → exceptions, options）
core/storage.py（→ models, exceptions）
   ↓
sources/{platform}/{mode}/{variant}/...（底层抓取函数，通过 source.resolve() 动态调用）
exporters/*.py（纯函数 export → options, models）
   ↓
core/downloader.py（门面：search / resolve_* / export，内部用 source 分发）
   ↓
novelbase/__init__.py（公开接口）
   ↓
入口层：cli/（CLI）· cli.py（非交互）· backend/（Web API）· scripts/
```

**核心规则**：

1. **禁止反向依赖**：`core/` 不 import `sources/`、`exporters/` 的具体实现；一律通过 `source.resolve(name, mode, function, variant)` / `register_exporter()` 动态分发。
2. **sources 底层函数**：每个 `{platform}/{mode}/{variant}/` 目录导出模块级函数 `search` / `novel_info` / `chapter_list` / `chapter_content`，签名接收 `(url 或 query, engine, **kwargs)`；能力元数据由 `sources/contracts.py` 的 `CAPABILITY_META` 映射（旧 `FUNC_FILE_MAP` 已退役）。
3. **exporters 是纯函数**：`export(chapters, novel, options=..., **kwargs)`，无类实例状态。
4. **前端只通过 API v2 通信**：响应格式 `{ok, message, data}`，不直接 import novelbase。

新增模块时请遵循此方向，勿引入反向依赖。

## 测试

```bash
# 全量测试（当前 280 passed / 2 skipped，Docker nld-test:3.11 实测）
python -m pytest tests/ -v --tb=short

# 后端导入验证
python -c "from novelbase import *; print('OK')"

# 前端类型检查
cd frontend && npx tsc --noEmit --project tsconfig.app.json

# 前端构建
cd frontend && npm run build
```

测试文件按 `test_{模块名}.py` 命名放在 `tests/`，另有 `tests/check_imports.py` 校验公开接口。

### 环境变量

API key 优先从环境变量读取（`{VARIANT}_API_KEY`），回退到 YAML 配置。
例如：`OIAPI_API_KEY=oiapi-xxxxx`。

## 扩展开发

### 新数据源（platform source）

1. 在 `novelbase/sources/` 下新建目录 `{name}/`，`__init__.py` 中定义模块级常量：

   ```python
   NAME = "fanqie"
   SHOW_NAME = "番茄"
   HOSTS = ("fanqienovel.com", "changdunovel.com")
   ```

   | 常量 | 必需 | 说明 |
   |------|:--:|------|
   | `NAME` | ✅ | 内部标识（目录名） |
   | `SHOW_NAME` | ✅ | 前端显示名 |
   | `HOSTS` | ✅ | 域名列表，`platform_from_url()` 用来自动识别 URL 所属平台 |

   > `ID_PATTERN` / `ORIGIN_ID_PATTERN` / `BOOK_URL_TEMPLATE` 已退役（2026-08-22）：`Novel.id` 由 `resolve_meta()` 中心化生成 `sha256(canonical_book_url(url, platform))[:32]`，无需也无法从 id 反查。

2. 按引擎模式创建子目录：`browser/`、`requests/`、`api/{variant}/`（单实现模式用 `default` 作 variant 名）。
3. 每个模式目录实现模块级函数：`search.py`、`novel_info.py`、`chapter_list.py`、`chapter_content.py`（函数名与 capabilities 功能名一致，由 `contracts.py` 的 `CAPABILITY_META` 映射）。
4. 在 `template/config/sites/` 下添加 `{name}.yaml`（模板可参考现有平台），并在 `app_data/config/sites/` 生成运行时配置。
5. **生成 manifest**：运行 `python -m novelbase.utils.build_manifest` 重新生成 `novelbase/utils/_manifest.py`。此文件供 Nuitka onefile 模式读取（exe 内无目录结构可扫描），删/增书源后必须重新生成。
6. 若打包便携版：portable 构建脚本全量复制 `novelbase`，无需额外配置；如需裁剪请同步修改 `build-portable.ps1/.sh` 的复制清单。

### 移除书源

1. 删除 `novelbase/sources/{platform}/` 目录。
2. 运行 `python -m novelbase.utils.build_manifest` 重新生成 manifest。
3. 删除 `app_data/config/sites/{platform}.yaml` 与 `template/config/sites/{platform}.yaml`。
4. 完成。前端搜索 / 后端 URL 识别 / CLI 平台推断全部自动失效（数据驱动，无硬编码残留），`/api/v2/download/sources` 不再返回该书源。

### Manifest 机制

- **开发模式**：`register_source()` 和 `capabilities()` 直接扫描 `sources/` 目录，零配置。
- **Nuitka onefile 模式**：exe 解压后无 `.py` 文件可扫描 → 读取构建时 `build_manifest.py` 预生成的 `novelbase/utils/_manifest.py`，内容与目录扫描结果完全一致。
- **构建流程**：`build-nuitka.ps1` 在 Nuitka 编译前自动调用 `python -m novelbase.utils.build_manifest`，确保 manifest 与源码同步。

### 新导出器

1. 在 `novelbase/exporters/` 下新建 `{name}.py`：
   - 定义 `{Name}ExportOptions`（继承 `core.options.ExportOptions`）
   - 定义模块级纯函数 `export(chapters, novel, options=..., **kwargs) -> Path`
2. registry 会扫描 `exporters/` 目录自动发现（`register_exporter()`），无需手动注册。
3. 在 `template/config/formats/` 下添加 `{name}.yaml`。

### 新引擎

1. 在 `novelbase/core/engine.py` 创建类 `{Name}Engine`，继承 `Engine`，实现所有抽象方法。
2. 在 `create_engine` 的 `mode_map` 字典中添加映射。
3. 若新引擎有专属配置，在 `core/options.py` 添加对应 Options 数据类。

## PR 流程

1. Fork 仓库，创建功能分支（建议从 `dev` 分支切出）。
2. 改动后确保 `python -m pytest tests/ -v --tb=short` 全部通过，前端改动需 `tsc --noEmit` 通过。
3. CI 会自动跑语法检查 + 导入验证 + 单元测试（Python 3.10/3.11/3.12）。
4. PR 到 `main` 分支。
5. 维护者 review 后合并。

### 提交约定

- 提交消息使用**中文**，描述改动内容。
- **一个方面一条 commit**：每次提交只做一件事，不要把无关改动混在一起。
- 禁止 `git add -A`：显式指定要添加的文件/路径。
