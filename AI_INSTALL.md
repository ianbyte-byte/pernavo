# Pernavo AI 安装执行手册

## 复制给安装 AI 的提示词

```text
请为我安装 Pernavo 的完整 Skills 系统。完整执行手册：
https://raw.githubusercontent.com/ianbyte-byte/pernavo/refs/heads/main/AI_INSTALL.md

默认参数：来源使用官方 GitHub 仓库 https://github.com/ianbyte-byte/pernavo；安装给当前用户
**本机所有支持 global 安装的 agent harness**；范围为 global；目标为手册列出的全部 8 个
Skills；安装方式为固定 SHA checkout 中的 copy。CLI 使用 `--agent '*'`，不是只安装 Codex 或
当前会话那一个宿主。远程 URL 只用于发现和 clone，不直接作为安装源。

开始前必须读取完整手册，重新检查 skills CLI 的 version/help，确认写入授权，精确核对远程
--list 的 8 项，并用 JSON 快照检查同名冲突。不要直接盲跑安装命令，不要使用 --all，
不要使用 remove --all。遇到来源不同的同名项时，默认采用方案 A：保存可精确恢复的旧登记后，
仅按名称定向移除冲突项，再从固定 SHA checkout 重装；旧来源、revision 或影响范围无法可靠
恢复时必须停止。若远程 --list 不是精确 8 项，停止并说明该版本尚未发布。
安装后按手册完成 JSON diff、新会话触发验证、报告和可定向回滚记录。
默认安装集合是：全部 8 个 Skills（写入本机全部支持 global 的 agent harness）、跨项目
`AGENTS.md` 规则、API 测试 Stop 门禁、`~/.pernavo` 运行日志 Hook，以及 checkout 内只读
`agentctl` harness 检查。
由本手册中的安装代理阅读现有文件后再写入，不要用脚本整文件覆盖宿主配置。
安装 Skills 成功后：
1. 将固定 checkout 中的 `AGENTS-PERNAVO.md` 同步到 Codex、Claude Code、Cursor、Grok 各自
   会加载的用户级规则路径（见手册目标表）。目标不存在或普通文件长度为 0 时写入；已相同则
   跳过；非空且不同则停止且不得覆盖。不要覆盖 Claude Code 的 `~/.claude/AGENTS.md`（常为
   其它插件正文）；Claude 使用 `~/.claude/rules/pernavo.md`。Cursor 使用
   `$HOME/.cursor/rules/pernavo.mdc`（须含 `alwaysApply: true`）；默认安装不得写入
   `$HOME/.cursor/AGENTS.md`，也不得改写项目 `AGENTS.md`。
2. 先读取 Claude `settings.json`、Codex `hooks.json`、Cursor `hooks.json` 与 Grok
   `~/.grok/hooks/*.json`，按现有 Hook 数组形状把 API 测试完成门禁合并进去；保持已有 Hook
   与其它键不变，不得整文件替换，不得 mkdir 缺失的 vendor 根目录。
   命令路径必须指向已落盘 test-engineering 副本中的 `api_test_stop_hook.py`。
   合并后用只读 `--check` 核对；禁止对默认宿主路径直接 `--apply`。
3. 将固定 checkout 中的 `scripts/pernavo-runtime-hook.py` 复制到
   `$HOME/.pernavo/hooks/runtime-hook.py`，并按现有形状合并运行日志 Hook；日志写入
   `$HOME/.pernavo/logs/runtime.jsonl`。不得记录原文 prompt、命令、工具输出或凭据。
   不得整文件替换宿主 Hook 文件。Cursor / Grok 的 `PERNAVO_RUNTIME_SOURCE` 分别为
   `cursor` 与 `grok`。
```

本手册供 AI 安装代理逐步执行，不是 Shell 脚本。上述默认值只补全用户未指定的参数；安装代理
不得再次要求用户复述这些默认值，除非用户明确要求缩小或改变目标。默认值不能替代授权、全文
阅读、冲突检查或逐步验证。若本 Raw URL 不可用、为空或不是本文件，立即停止；
不得退回 README 中的旧命令，也不得宣称当前本地未提交内容已经发布到远程。

本文曾用 `skills` CLI 1.5.21 验证。CLI 会变化，每次安装仍必须重新读取当前
`npx --yes skills --help` 以及相关子命令帮助，并以当次输出为准。

说明：本手册的 8 个 Skills 是当前仓库和远程发布安装集合。名称集合、固定 revision、触发
语料和验证数字必须保持同步；如果远程 `--list` 不包含本手册的全部 8 项，必须停止。

## 默认安装画像

除非用户明确覆盖，所有安装代理必须使用同一组参数：

| 参数 | 默认值 |
|---|---|
| 来源 | `https://github.com/ianbyte-byte/pernavo`，固定 full commit SHA |
| 目标 | 当前用户本机所有支持 global 安装的 agent harness |
| CLI 目标选择 | `--agent '*'`；不要把显示名称（如 `Claude Code`）当作 CLI ID；不要只装当前会话宿主 |
| 范围 | global |
| 内容 | 下方完整的 8 个 Skills |
| 复制方式 | `--copy` |
| 冲突策略 | 方案 A；来源无法恢复时 `blocked` |
| 全局 AGENTS.md | 按宿主写入下表专用路径；不存在或空文件则创建；已相同则跳过；非空且不同则停止 |
| API 测试 Stop 门禁 | 安装代理先读取再合并进 Claude、Codex、Cursor、Grok 各自的 Hook 文件；不得替换已有 Hook |
| `~/.pernavo` 运行日志 | 复制 `pernavo-runtime-hook.py` 到 `$HOME/.pernavo/hooks/`，合并 SessionStart/Prompt/Tool/Stop 等事件；best-effort 不阻断 |
| 本机 agent harness | `--agent '*'` 写入 CLI 支持的全部 global 目标；checkout 内只读运行 `agentctl`；不把 `agentctl` 安装进宿主 |

`--agent '*'` 表示当前 CLI 支持的全部 agent 目标，不等于“只安装当前会话使用的 agent”。
不同版本可能枚举不同数量；必须记录当次 CLI 输出中的实际 agent 列表和不支持 global 的目标，
不能把旧版本的数量写死为成功条件。当前 `skills@1.5.22` 的全局登记显示 66 个常规 agent；
Eve 和 PromptScript 的 global 安装不受支持，属于已知能力边界，不能通过重试或手工删除绕过。

## 默认成功路径

| 顺序 | 操作 | 通过条件 |
|---|---|---|
| 1 | 确认写入授权 | 当前用户、本机全部支持 global 的 agent harness、官方来源、8 项、copy、AGENTS 同步与 Stop 门禁合并均获授权；不得把本提示理解成覆盖非空全局 `AGENTS.md` 或整份 Hook 文件 |
| 2 | 检查 CLI | version 和 help 可用，参数与本手册兼容 |
| 3 | 远程 `--list` | 名称集合精确等于下方 8 项；远程 URL 仅用于发现 |
| 4 | 固定来源 | 安全临时目录中 `--single-branch` clone 默认分支，记录 full HEAD SHA，detach、校验 8 项；不 fetch 其他分支 |
| 5 | 保存全局 JSON 快照 | `skills ls --global --json`；agent 列表从登记的 `agents` 字段汇总 |
| 6 | 分类同名项 | 每项是 `absent`、`same-source` 或 `conflict` |
| 7 | 处理并安装 | `same-source` 不触碰；安装 `absent`；`conflict` 默认按方案 A 定向替换 |
| 8 | 同步分发规则 | 目标不存在或空文件则写入且 `cmp` 通过；已相同则跳过；符号链接、非普通文件、父目录不可用或非空且不同则停止且不写入 |
| 9 | 合并 API 测试 Stop 门禁 | 先读取宿主 JSON，按现有数组形状追加；before 中的 Hook 命令 after 仍在；只读 `--check` 通过；无整文件替换、无 `--apply` |
| 10 | 合并 `~/.pernavo` 运行日志 | 先复制 hook 脚本再按现有形状追加；日志目录 `0700`；before 中的 Hook 命令 after 仍在；无密钥落盘 |
| 11 | 本机 harness | `--agent '*'` 覆盖 CLI 支持的全部 global 目标；checkout 内只读 `agentctl` 通过 |
| 12 | 安装后 JSON diff | absent 正确新增、conflict 正确换源，无意外 Agent 或范围 |
| 13 | 新会话验证 | 3 个代表性 smoke，或完整 24-case corpus |
| 14 | 报告与回滚 | 区分新增与替换；`AGENTS.md` 与各 Hook 条目分别给出定向回滚 |

## 安全契约与系统边界

安装代理必须遵守：

1. 写入前确认用户授权的来源、当前系统用户、目标 Agent、范围、名称集合和 copy/symlink
   方式。默认写入当前用户本机所有支持 global 安装的 agent harness；用 `--agent '*'` 交给
   当前 CLI 枚举目标，不要只写 Codex 或当前会话宿主。
2. 保留既有 Skills、配置、记忆、目录和未提交工作。不得通配删除、递归清理、修改 Shell
   启动文件、静默安装系统依赖或运行 `skills remove --all`。
3. 不在 Pernavo 自己的 checkout 中做项目级自安装；那会创建 `.agents/skills` 副本并与
   `skills/` 源竞争。
4. `absent` 直接安装，`same-source` 保持不变；`conflict` 默认采用方案 A，在旧来源、固定
   revision、影响 Agent 和恢复命令均已记录后定向替换。任一恢复条件不完整时停止，不得覆盖。
5. 安装 8 个入口 Skills 会提供成本感知的自动工作流政策，包括生命周期、数据、性能、测试和
审查路由规则。默认安装还会由安装代理把 API 测试完成门禁和 `~/.pernavo` 运行日志 Hook
合并进宿主配置：必须先读取现有 JSON，按已有数组形状追加，不得整文件替换。不得安装 MCP、
权限、Mem0 或 skill-usage logger，也不得把 `scripts/agentctl.py` 复制进宿主。默认必须把
Skills 写入 CLI 支持的全部 global agent harness，并在固定 checkout 内做只读 `agentctl`
检查。运行日志 Hook 是 best-effort，不得阻断宿主。合并写入只证明配置被编辑，不证明宿主
已触发该 Hook。
6. 真正的子 Agent 派生，以及 Skill 是否 `loaded`/`executed`，只能在安装后的宿主新会话中
   观察；命令成功、目录存在或模型自述均不是运行时证明。
7. 分发规则同步只使用固定 checkout 中的 `AGENTS-PERNAVO.md`，不使用项目 `AGENTS.md`。目标
   不存在、或普通文件长度为 0 时写入；内容已相同则跳过；目标为符号链接、非普通文件、父目录
   不存在/不是目录/是符号链接，或已存在、非空且内容不同时停止且不得 `cp`。不得把粘贴提示
   理解成覆盖非空文件的授权。该文件只保存跨项目可复用规范，不包含 Skills 清单、安装命令或
   项目专属规则。

### Agent 目标与实际落盘

`skills ls --global --json` 的一个登记可能包含多个 `agents`，这只能证明 CLI 的全局登记；
安装后还要按登记中的 `path` 检查 `SKILL.md` 实际存在，并按 agent 目录抽样或逐项检查文件。
报告至少区分以下状态：

| 状态 | 判定 |
|---|---|
| `registered` | JSON 登记包含名称和目标 agent |
| `materialized` | 登记的 `path/SKILL.md` 存在，且 SHA-256 与固定 checkout 对应文件一致 |
| `shared-registration` | 多个 agents 共享同一全局 path；不重复声称创建了多份独立副本 |
| `unsupported-global` | CLI 明确拒绝该 agent 的 global 安装，例如 Eve、PromptScript |
| `blocked-source` | 已有同名登记的 `source/sourceUrl` 缺失或 revision 无法固定，不能覆盖 |

目标 agent 的实际显示名和 CLI ID 可能不同。命令参数使用 CLI 支持的 ID 或 `'*'`；报告同时
记录 JSON 中的显示名。不要把目录“看起来存在”、命令退出 0 或模型自述当成正文已加载证据。

### 证据层级

| 层级 | 可接受证据 | 不能证明 |
|---|---|---|
| `source-valid` | 固定 checkout 校验通过，或远程 `--list` 精确列出预期集合 | 已写入目标 Agent |
| `installed` | 安装后 global JSON 快照显示正确名称、范围、来源和 agent 登记 | 新会话已加载正文 |
| `loaded` | 宿主 trace、日志或等价事件显示对应 `SKILL.md` 正文被加载 | Skill 内工具实际执行 |
| `executed` | 目标工具、子 Agent、Hook、MCP 或 Harness 确有执行结果 | 外部目标状态已改变 |
| `target-observed` | 用例要求的 expected owners 全部加载，且 forbidden owners 均未加载 | 交付、部署或外部环境行为正确 |
| `environment-observed` | 对授权的外部目标环境做独立观测，结果与预期一致 | 其他未观测环境也一致 |

结论只能到达实际证据支持的最高层级；无法观察正文加载时应报告
`installed; runtime activation unverified`。

## 唯一预期的 8 个入口 Skills

```text
codebase-slimming
change-review
data-work
engineering-workflow
performance-work
repository-governance
report-writer
test-engineering
```

比较时按名称集合精确比较：少一项、多一项、重复项或未知项都必须停止。

## 1. 只读预检

先记录版本和完整帮助。不要依据本文对旧版本的描述猜参数：

```bash
git --version
node --version
npx --yes skills --version
npx --yes skills --help
npx --yes skills add --help
npx --yes skills ls --help
npx --yes skills update --help
npx --yes skills remove --help
```

1.5.21 已验证语义如下：`add` 支持 `-g/-a/-s/-l/-y/--copy`；`ls` 支持
`-g/-a/--json`；`update` 只有 `-g/-p/-y`，没有 `--agent`；`remove` 可用
`-g/-a` 和字面名称定向移除。若当前帮助不兼容，停止并报告，不要试错写入。

默认先对官方远程做只读发现：

```bash
PERNAVO_REMOTE="https://github.com/ianbyte-byte/pernavo"
npx --yes skills add "$PERNAVO_REMOTE" --list
```

输出必须精确对应上述 8 个名称。如果不是，停止并说明：远程版本尚未发布或与本手册不一致。
该 URL 指向可变远程，只能证明发现时的列表，不能作为 installed revision 证据，也不能把当前
本地 dirty 内容当成远程内容。

### 固定默认安装来源

创建仅当前用户可访问的新临时目录，验证路径确为本次新目录，然后 clone 官方仓库的默认分支。
不得使用已有路径，不得覆盖内容，默认不得 `fetch --all`：远程上其它分支可能仍含与 Skills
无关的大文件，会把安装 clone 拉回数百 MB。

```bash
umask 077
PERNAVO_INSTALL_TMP="$(mktemp -d "${TMPDIR:-/tmp}/pernavo-install.XXXXXX")"
test -n "$PERNAVO_INSTALL_TMP"
test -d "$PERNAVO_INSTALL_TMP"
test ! -L "$PERNAVO_INSTALL_TMP"
chmod 700 "$PERNAVO_INSTALL_TMP"
PERNAVO_CHECKOUT="$PERNAVO_INSTALL_TMP/checkout"
test ! -e "$PERNAVO_CHECKOUT"
git clone --single-branch --branch main --depth 1 "$PERNAVO_REMOTE" "$PERNAVO_CHECKOUT"
PERNAVO_COMMIT_SHA="$(git -C "$PERNAVO_CHECKOUT" rev-parse --verify 'HEAD^{commit}')"
git -C "$PERNAVO_CHECKOUT" checkout --detach "$PERNAVO_COMMIT_SHA"
git -C "$PERNAVO_CHECKOUT" rev-parse --verify 'HEAD^{commit}'
npx --yes skills add "$PERNAVO_CHECKOUT" --list
"$PERNAVO_CHECKOUT/scripts/validate-skills.sh"
```

`--list` 的发现 clone 不能代替上述固定 checkout：它不是已记录 SHA、已 detach、已跑
`validate-skills.sh` 的安装源。发现 clone 与固定 checkout 各做一次是预期的；不要为了省一次
clone 而把远程 URL 交给 `skills add` 当安装源。

再次确认 checkout 的列表精确为 8 项、校验通过，并在报告中记录完整 SHA。若用户要求指定
非 HEAD 的 revision，先确认该 full commit SHA 存在，再改用无 `--depth 1` 的 clone 并 detach
到该 SHA 后执行相同校验。不得把 branch、tag 或远程 `main` 名称当成安装 revision。

临时 checkout 和所有 JSON 快照必须保留到安装报告、diff 和回滚信息全部完成；不要自动删除。
报告其路径，由用户决定何时清理。

若用户明确要求从已有本地 checkout 安装，还要记录 `git status --short`；dirty 时先报告“将
安装含未提交内容的工作树”，只有用户明确授权才继续。开发 checkout 的校验命令为：

```bash
cd /absolute/new/path/pernavo
./scripts/validate-skills.sh
```

验证器缺失可标为 `partial`；其他校验失败必须停止。默认官方安装路径要求完整校验通过，不能
以 `partial` 继续写入。

## 2. JSON 快照与冲突分类

把原始 JSON 写入刚创建、权限为 `0700` 的 `$PERNAVO_INSTALL_TMP`。先验证变量非空、路径存在、
不是 symlink，且目标文件尚不存在；不得覆盖旧快照：

```bash
test -n "$PERNAVO_INSTALL_TMP"
test -d "$PERNAVO_INSTALL_TMP"
test ! -L "$PERNAVO_INSTALL_TMP"
test ! -e "$PERNAVO_INSTALL_TMP/pernavo-before-global.json"
npx --yes skills ls --global --json > "$PERNAVO_INSTALL_TMP/pernavo-before-global.json"
```

不要对 `ls` 使用 `--agent '*'`：CLI 1.5.22 会拒绝该过滤器。`add` 与 `remove` 仍使用
`--agent '*'`。每个登记的目标 Agent 从 JSON 的 `agents` 数组汇总；需要按单个 CLI ID 抽样时，
用 help 里的合法 ID，不要用星号。

对 8 个请求名称逐项读取 `name`、`path`、`scope`、`source`、`sourceUrl` 和所有 Agent 登记，并分类：

- `absent`：全局 JSON 中无同名登记，且没有不明同名来源；可安装。
- `same-source`：已来自同一个官方仓库；或 `source`/`sourceUrl` 为空，但落盘
  `path/SKILL.md`（`test-engineering` 还要 `scripts/api_test_stop_hook.py` 与
  `scripts/grade_api_jsonl.py`）的 SHA-256 与本次 checkout 对应文件一致。本次不触碰、不重装、
  不隐式更新。
- `conflict`：来自其他来源，或来源无法可靠判断且内容 SHA 与本次 checkout 不一致；进入下方
  方案 A 的替换安全门，不能直接覆盖。

如果旧来源显示 `tuloong/pernavo`、`tuloong/loongclaude` 或其他 fork/mirror，只有 GitHub 解析后的
canonical repository（`full_name` 或 `html_url`）等于 `ianbyte-byte/pernavo`，或内容 SHA 与本次
checkout 一致时，才可视为 `same-source`。不得只因为仓库名称相似或内容看起来相同就跳过冲突处理。

安装前必须同时保存：8 项分类、原始 JSON、已授权目标、“安装后全局名称集合减安装前全局名称
集合”的新增项回滚计算规则，以及每个替换项的旧来源、固定 revision、Agent、scope 和恢复
命令。不得根据请求列表猜测新增项或替换项。

### 默认冲突策略：方案 A（受控替换）

存在 `conflict` 时默认执行方案 A，不再仅因“来源不同”要求用户在 A/B/C 中再次选择：

1. 把冲突项进一步标为 `replaceable` 或 `blocked`。
2. 只有旧登记的来源 repository、可取得的固定 full commit SHA、目标 Agent、scope、路径和精确
   恢复命令均已记录，才可标为 `replaceable`。
3. 仅按字面名称、目标 Agent 和 global scope 定向移除 `replaceable` 冲突项；不得使用通配符、
   `remove --all`、递归目录删除或扩大到其他 Agent。
4. 移除后立即重读 JSON，证明只有预期冲突登记消失，再从本次固定 checkout 安装这些名称。
5. 来源不明、旧 revision 无法固定、CLI 无法隔离 Agent、无法枚举影响范围或无法写出精确恢复
   命令的冲突项一律标为 `blocked`，停止写入并报告 `rollback blocked`。

方案 A 只授权替换本手册请求的 8 个同名 Skill 登记，不授权删除其他 Skill、配置、Hook、MCP、
Harness、记忆、目录或系统依赖。用户明确要求保留旧来源或接受混合来源时，才可偏离方案 A，且
必须在报告中记录覆盖本默认值的授权。

## 3. 安装

只有写入前 8 项全部是 `absent` 时，才可使用星号选择全部 Skills。这里的“全部 absent”可以是
原本全部 absent，也可以是方案 A 已定向移除全部 replaceable conflict 并完成移除后 JSON 校验的
结果。安装源必须是已经 detach、记录 full SHA 并校验通过的 `$PERNAVO_CHECKOUT`，不能是
`$PERNAVO_REMOTE`：

```bash
npx --yes skills add "$PERNAVO_CHECKOUT" \
  --global \
  --agent '*' \
  --skill '*' \
  --yes \
  --copy
```

### 同步分发规则

固定 checkout 中的 `AGENTS-PERNAVO.md` 是可分发规则源。Skills 安装成功后，对下表每个目标各自
分类并写入；默认不得覆盖已有文件（空文件除外）；粘贴提示不构成覆盖授权。不要覆盖
`~/.claude/AGENTS.md`。

| 宿主 | 用户级规则路径 | 允许创建的子目录 |
|---|---|---|
| Codex | `${CODEX_HOME:-$HOME/.codex}/AGENTS.md` | 不得 mkdir `$CODEX_HOME` |
| Claude Code | `$HOME/.claude/rules/pernavo.md` | 父目录 `~/.claude` 已是真实目录时可 `mkdir` `rules/` |
| Cursor | `$HOME/.cursor/rules/pernavo.mdc` | 父目录 `~/.cursor` 已是真实目录时可 `mkdir` `rules/`；须 `.mdc` 且 `alwaysApply: true` |
| Grok | `$HOME/.grok/rules/pernavo.md` | 父目录 `~/.grok` 已是真实目录时可 `mkdir` `rules/` |

Cursor Agent 仍会读取项目 `AGENTS.md`（仓库根与子目录）。默认安装不得改写项目
`AGENTS.md`，也不得写入 `$HOME/.cursor/AGENTS.md`。Cursor 规则必须是 `.mdc`：纯 `.md` 会被
忽略。正文与 `AGENTS-PERNAVO.md` 相同，文件头固定为：

```text
---
description: Pernavo cross-project guidance
alwaysApply: true
---
```

判定 `skipped-identical` 时，去掉 YAML frontmatter 后的正文须与来源 `cmp -s` 相同。Cursor
的 Stop 与运行日志仍合并进 `$HOME/.cursor/hooks.json`。

```bash
PERNAVO_AGENTS_SOURCE="$PERNAVO_CHECKOUT/AGENTS-PERNAVO.md"
PERNAVO_GLOBAL_AGENTS="${CODEX_HOME:-$HOME/.codex}/AGENTS.md"
PERNAVO_GLOBAL_AGENTS_PARENT="$(dirname -- "$PERNAVO_GLOBAL_AGENTS")"
test -f "$PERNAVO_AGENTS_SOURCE"
test ! -L "$PERNAVO_AGENTS_SOURCE"
```

对每个目标路径使用同一套状态表。把 Codex 路径记为 `$PERNAVO_GLOBAL_AGENTS` 以便回滚模板复用。

按目标分类，只执行匹配分支，不得先备份再无条件 `cp`。先判断
`test -L` 目标；损坏的符号链接也属于 `blocked-symlink`，不得写入。

| 状态 | 判定 | 动作 |
|---|---|---|
| `blocked-source-missing` | 来源不是普通文件或是符号链接 | 停止，不写入 |
| `blocked-symlink` | 目标存在且是符号链接 | 停止，不写入 |
| `blocked-not-file` | 目标存在且不是普通文件 | 停止，不写入 |
| `skipped-identical` | 目标是普通文件且与来源 `cmp -s` 相同 | 跳过，不写入 |
| `blocked-existing` | 目标是普通文件、长度非 0，且与来源不同 | 停止，不写入，报告目标路径和手工合并步骤 |
| `blocked-parent` | 目标不存在，且父路径不存在、不是目录或是符号链接 | 停止，不写入，不得 `mkdir` |
| `created` | 目标不存在，父路径是真实目录 | `cp` 后来源与目标必须 `cmp -s` |
| `replaced-empty` | 目标是普通文件且长度为 0 | `cp` 后来源与目标必须 `cmp -s`；这不是覆盖非空文件 |

`created` 的写入命令仅为：

```bash
test -d "$PERNAVO_GLOBAL_AGENTS_PARENT"
test ! -L "$PERNAVO_GLOBAL_AGENTS_PARENT"
test ! -e "$PERNAVO_GLOBAL_AGENTS"
cp "$PERNAVO_AGENTS_SOURCE" "$PERNAVO_GLOBAL_AGENTS"
cmp -s "$PERNAVO_AGENTS_SOURCE" "$PERNAVO_GLOBAL_AGENTS"
```

`replaced-empty` 的写入命令仅为：

```bash
test -d "$PERNAVO_GLOBAL_AGENTS_PARENT"
test ! -L "$PERNAVO_GLOBAL_AGENTS_PARENT"
test -f "$PERNAVO_GLOBAL_AGENTS"
test ! -L "$PERNAVO_GLOBAL_AGENTS"
test ! -s "$PERNAVO_GLOBAL_AGENTS"
cp "$PERNAVO_AGENTS_SOURCE" "$PERNAVO_GLOBAL_AGENTS"
cmp -s "$PERNAVO_AGENTS_SOURCE" "$PERNAVO_GLOBAL_AGENTS"
```

将分发状态、目标路径、来源 checkout 和 full SHA 写入安装报告。`blocked-*` 不回滚已完成的
Skill 登记；Skills 成功而规则未写入时记 `partial`。项目根目录的 `AGENTS.md` 只治理本仓库，
`AGENTS-PERNAVO.md` 才参与分发。

### 合并 API 测试 Stop 门禁

默认安装包含该门禁。由安装代理阅读现有宿主 JSON 后按形状合并，以保证 Mem0、skill-usage
和其它已有 Hook 不被改写。这不是 Shell 脚本，也不是对默认宿主路径运行
`install_api_test_gate.py --apply`。

先从安装后的 `skills ls --global --json` 取出 `test-engineering` 的 `path`，确认下列文件存在
且 SHA-256 与本次 `$PERNAVO_CHECKOUT/skills/test-engineering/scripts/` 中对应文件一致：

```text
scripts/api_test_stop_hook.py
scripts/grade_api_jsonl.py
```

若已落盘的 same-source `test-engineering` 缺少上述脚本或 SHA 不一致，只对该名称从本次
checkout 再执行一次 `--copy`，不触碰其他 same-source 项。命令路径必须使用已落盘副本，
不得指向即将删除的 `$PERNAVO_CHECKOUT`。

宿主与事件：

| 宿主 | 文件 | 事件 |
|---|---|---|
| Claude Code | `$HOME/.claude/settings.json` | `Stop`, `TaskCompleted` |
| Codex | `${CODEX_HOME:-$HOME/.codex}/hooks.json` | `Stop`, `SubagentStop` |
| Cursor | `$HOME/.cursor/hooks.json` | `stop`, `subagentStop`（Cursor camelCase；元素多为扁平 `command`） |
| Grok | `$HOME/.grok/hooks/pernavo.json` | `Stop`, `SubagentStop`（Claude 形分组 JSON；`~/.grok` 已存在时可 `mkdir` `hooks/`） |

Grok 默认还会扫描 `~/.claude/settings.json` 与 `~/.cursor/hooks.json`。Claude 或 Cursor
已含同一 Stop 门禁时，Grok 原生文件会再跑一遍；门禁必须幂等。不要为避免重复而跳过
Grok 原生 `~/.grok/hooks/pernavo.json`。用户若关闭 `[compat.claude] hooks` 或
`[compat.cursor] hooks`，仍依赖该原生文件。

每个文件先读取再分类，只执行匹配分支。写入前把该文件里已有 Hook 的 `command` 全部抄下，
写入后必须逐条仍在。

| 状态 | 判定 | 动作 |
|---|---|---|
| `blocked-symlink` | 目标存在且是符号链接 | 停止，不写入 |
| `blocked-not-file` | 目标存在且不是普通文件 | 停止，不写入 |
| `blocked-invalid` | 不是 JSON 对象，或 `hooks` 存在但不是对象 | 停止，不写入 |
| `blocked-format` | 某所需事件存在但不是数组 | 停止，不猜测、不改写该事件 |
| `blocked-parent` | 目标不存在，且父路径不存在、不是目录或是符号链接 | 跳过该宿主，不得 `mkdir` |
| `skipped-identical` | 所需事件的数组已包含 `api_test_stop_hook.py` | 不写入 |
| `created` | 目标不存在，父路径是真实目录 | 创建仅含本门禁的 JSON；新文件 `chmod 600` |
| `merged` | 目标是普通 JSON 对象 | 按该文件现有数组形状追加一条，保留其它键和已有 Hook |

追加条目必须与该事件数组里已有元素同形。若已有元素是
`{"hooks":[{ "type":"command", "command":"...", "timeout":30 }]}` 这种分组，则追加同形分组；
若已有元素是扁平的 `{"type":"command",...}`，则追加扁平条目。不要改写已有元素的 `matcher`
或其它字段。分组内命令为：

```text
python3 "MATERIALIZED_TEST_ENGINEERING/scripts/api_test_stop_hook.py"
```

`MATERIALIZED_TEST_ENGINEERING` 换成上一步得到的已落盘 path。不得把 checkout 临时目录写进
宿主配置。

合并后对已落盘脚本运行只读核对，禁止对默认宿主路径加 `--apply`：

```bash
python3 "$PERNAVO_TE_ROOT/scripts/install_api_test_gate.py" \
  --check \
  --script "$PERNAVO_TE_ROOT/scripts/api_test_stop_hook.py" \
  --cursor-hooks "$HOME/.cursor/hooks.json" \
  --grok-hooks "$HOME/.grok/hooks/pernavo.json"
```

`--check` 通过只证明 JSON 含有该脚本路径，不证明宿主已触发 Hook。四个宿主的父目录都
`blocked-parent` 时，Skills 与规则文件仍可记成功，Hook 记 `blocked-parent`，总状态
`partial`。任一已检查宿主为 `blocked-symlink`、`blocked-not-file`、`blocked-invalid` 或
`blocked-format` 时停止。

Hook 回滚只删除 `command` 含 `api_test_stop_hook.py` 的那一条；不得删除 `settings.json` 或
`hooks.json`，不得移除其它 Stop 条目。若本次 `created` 了该文件且文件现在只含本门禁，也只
删除本门禁条目，不删除整个文件。

### 合并 ~/.pernavo 运行日志 Hook

默认安装包含该 best-effort 日志，供后续改进 Skills 与完成门禁。它不替代 API 测试 Stop 门禁，
也不安装 `~/.codex/skill-usage` logger。由安装代理复制脚本并阅读现有宿主 JSON 后按形状合并。

来源脚本是固定 checkout 中的 `scripts/pernavo-runtime-hook.py`。先落到用户主目录，这样临时
checkout 删除后命令路径仍然有效：

```text
PERNAVO_HOME="${PERNAVO_HOME:-$HOME/.pernavo}"
```

| 状态 | 判定 | 动作 |
|---|---|---|
| `blocked-home` | `$HOME` 不存在或不是真实目录 | 停止该步，不写入 |
| `blocked-not-dir` | `$PERNAVO_HOME` 已存在且不是目录，或是符号链接 | 停止，不写入、不删除 |
| `copied` / `skipped-identical` | `hooks/runtime-hook.py` 与来源 `cmp -s` | 不同则 `cp` 后 `chmod 600`；相同则跳过 |
| `logs-ready` | `$PERNAVO_HOME/logs` 为真实目录 | 没有则 `mkdir -m 700`；不得把项目树写进该目录 |

允许创建 `$HOME/.pernavo`、`hooks/` 和 `logs/`（`0700`）。这不授权 `mkdir` `$HOME/.claude`、
`$HOME/.cursor`、`$HOME/.grok` 或 `$CODEX_HOME`。`~/.claude` / `~/.cursor` / `~/.grok` 已存在时可以创建
其下的 `rules/` 与 `hooks/`。不要删除已有 `logs/runtime.jsonl`。

命令路径必须是：

```text
PERNAVO_RUNTIME_SOURCE=claude python3 "$HOME/.pernavo/hooks/runtime-hook.py"
PERNAVO_RUNTIME_SOURCE=codex python3 "$HOME/.pernavo/hooks/runtime-hook.py"
PERNAVO_RUNTIME_SOURCE=cursor python3 "$HOME/.pernavo/hooks/runtime-hook.py"
PERNAVO_RUNTIME_SOURCE=grok python3 "$HOME/.pernavo/hooks/runtime-hook.py"
```

分别写入各宿主。Claude 事件：`SessionStart`、`UserPromptSubmit`、`PreToolUse`、
`PostToolUse`、`Stop`、`TaskCompleted`。Codex 与 Grok：`SessionStart`、`UserPromptSubmit`、
`PreToolUse`、`PostToolUse`、`Stop`、`SubagentStop`。Cursor 使用 camelCase：`sessionStart`、
`beforeSubmitPrompt`、`preToolUse`、`postToolUse`、`stop`、`subagentStop`。每条仍按该文件
现有数组形状追加；`skipped-identical` 当该事件已含 `runtime-hook.py`。超时建议 10 秒。

写入前抄下已有 `command`，写入后必须仍在。禁止对默认宿主路径运行任何 `--apply` 安装器。
Hook 必须 `continue: true` 且 exit 0；不得记录原文 prompt、命令、工具输出、凭据或业务 JSONL。

回滚只删除 `command` 含 `runtime-hook.py` 的条目，并仅在 `hooks/runtime-hook.py` 仍与来源
`cmp -s` 相同时删除该脚本。不得删除 `logs/runtime.jsonl` 或整个 `$PERNAVO_HOME`。

存在任何 `same-source` 时，必须把所有原始 `absent` 名称和方案 A 已移除的 `replaceable conflict`
名称逐个写出；下面仅示范命令形状：

```text
npx --yes skills add "$PERNAVO_CHECKOUT" \
  --global \
  --agent '*' \
  --skill ABSENT_OR_REPLACED_NAME_1 ABSENT_OR_REPLACED_NAME_2 \
  --yes \
  --copy
```

上例不可原样执行。如果只有 `same-source`、没有 `absent` 或 `replaceable conflict`，报告已存在且
不做写入。`--agent '*'` 是本手册的默认目标选择；只有用户明确要求缩小目标时才改成具体 CLI
agent ID。任何情况下都不使用 `--all` 作为默认安装方式。

## 4. 安装后 diff 与新会话验证

验证安全临时目录和新文件名后保存安装后快照：

```bash
test -n "$PERNAVO_INSTALL_TMP"
test -d "$PERNAVO_INSTALL_TMP"
test ! -L "$PERNAVO_INSTALL_TMP"
test ! -e "$PERNAVO_INSTALL_TMP/pernavo-after-global.json"
npx --yes skills ls --global --json > "$PERNAVO_INSTALL_TMP/pernavo-after-global.json"
```

对 before/after JSON 做结构化比较并确认：请求的 absent 项各新增一次；方案 A 替换项名称和
目标 Agent 集合不变、来源已从记录的旧来源变为本次官方固定 checkout；scope 为 global；没有写入
未授权 Agent；same-source 项未改变。对每个请求项检查 `path/SKILL.md` 存在，并对固定 checkout
与落盘文件计算 SHA-256；记录共享 path 与不支持 global 的目标。checkout 内不得新增项目级
`.agents/skills/<name>` 副本。非零退出、部分安装或意外 diff 均进入停止/回滚流程。

随后重启目标宿主或开启确定会重新扫描 Skills 的新会话。从
`tests/skill-trigger-corpus.tsv` 选择并记录：

1. 一个正向请求：应加载目标 Skill；
2. 一个负向请求：不应加载目标 Skill；
3. 一个相邻责任碰撞请求：所有 expected owners 都应加载，所有 forbidden owners 均不应加载。

这 3 个案例只是代表性 smoke，只验证所选 Skill 的用例合同，不能证明其余 21 项或完整系统
routing。要验证全部系统 routing，必须在独立新上下文中运行全部 24 个 corpus cases，并逐项
核对完成事件、全部 expected owners 和全部 forbidden owners。完整运行成本较高，可以由用户
选择跳过；未运行时必须将其余 runtime activation 标为 unverified，不能声称 8 项均已验证。

记录宿主/version、会话、安装 SHA、请求、expected/forbidden/实际加载集合、正文加载事件位置，
以及真实子 Agent/工具是否执行。只有所有 expected owners 齐全且没有 forbidden owner，才达到
该用例的 `target-observed`。对授权外部环境的独立实际观测另记为 `environment-observed`，不能
与路由层混淆。宿主不暴露事件时，明确保留 `loaded`、`executed`、`target-observed` 和
`environment-observed` 未验证边界。

## 5. 更新：默认失败关闭

CLI 1.5.21 的 `update` 没有 Agent scope。用户只授权单个 agent、来源是本地 checkout、要求固定
revision，或无法枚举所有受影响的全局登记时，停止并报告：

```text
blocked: skills update has no agent scope
```

只有全部同名全局登记均来自官方来源，且用户明确授权所有受影响登记一起更新时，才可按字面
名称更新。例如用户授权完整 8 项时：

```bash
npx --yes skills update --global --yes \
  change-review codebase-slimming data-work engineering-workflow performance-work \
  repository-governance report-writer test-engineering
```

授权子集时只能保留该子集。更新前后重复来源检查、`--list` 和 JSON 快照。不得使用无名称的
`skills update -g` 作为本包默认更新命令。

## 6. 定向回滚

回滚必须把“新增登记”和“替换登记”分开处理。新增集合只能是
`after global registrations - before global registrations`；多 agent 安装时按 `name + agent`
登记对计算差集，把实际新增名称逐个写成字面量：

```text
npx --yes skills remove NEW_NAME_1 NEW_NAME_2 --global --agent '*' --yes
```

上例不可原样执行。不得移除安装前已存在的 same-source 项，不得使用 `--skill '*'` 或
`remove --all`；`--agent '*'` 仅表示本手册默认的全部支持目标。
多 Agent 安装要按 JSON 中每个 `name + agent` 的快照差集分别确认，随后重新读取 JSON，证明只删除
本次新增登记；共享 path 只能在所有本次新增 agent 登记均已移除后再判断是否仍被其他 agent 使用。

方案 A 替换的旧登记不是“新增登记”，名称集合差集无法识别它。回滚每个替换项时必须先按名称和
Agent 定向移除本次官方登记，再从安装前记录的旧 repository 和固定 full commit SHA 恢复相同
Agent 与 scope，并用 JSON 与 before 快照比较。缺少恢复来源、revision、影响范围或精确恢复命令
时，在替换前就必须报告 `rollback blocked` 并停止，不得假称可回滚或用旧来源最新分支代替旧
revision。

本次若将 `AGENTS.md` 标为 `created`，回滚只能在目标仍与来源 `cmp -s` 相同时删除该文件：

```bash
cmp -s "$PERNAVO_AGENTS_SOURCE" "$PERNAVO_GLOBAL_AGENTS" && rm -- "$PERNAVO_GLOBAL_AGENTS"
```

本次若将 `AGENTS.md` 标为 `replaced-empty`，回滚只能在目标仍与来源 `cmp -s` 时恢复为空文件，
不得删除该路径：

```bash
cmp -s "$PERNAVO_AGENTS_SOURCE" "$PERNAVO_GLOBAL_AGENTS" && : > "$PERNAVO_GLOBAL_AGENTS"
```

`cmp` 失败说明用户已改过该文件：报告 `rollback blocked`，不得删除。`skipped-identical` 与
所有 `blocked-*` 状态没有文件回滚动作。

## 7. 本机 agent harness（默认）

默认安装必须覆盖当前 CLI 支持 global 写入的全部 agent harness，使用 `--agent '*'`，不要只装
Codex、Cursor 或当前会话宿主。Eve 和 PromptScript 若被 CLI 拒绝 global，记
`unsupported-global`，不要重试或手工绕过。安装后按共享 `path` 检查 `SKILL.md` 已落盘，并记录
共享登记，不要把同一 path 计成多份独立副本。

Skills CLI 不会把 `scripts/agentctl.py` 或 `harness/` 安装进宿主，也不会安装 MCP、权限或
skill-usage logger。默认安装仍须在固定 checkout 根目录做只读 harness 检查：

```bash
python3 scripts/agentctl.py doctor --config harness/examples/agentctl.json --json
python3 scripts/agentctl.py explain --config harness/examples/agentctl.json \
  --event harness/examples/event.json --json
python3 scripts/agentctl.py memory search --config harness/examples/agentctl.json \
  --query canonical --json
```

这些命令只证明 checkout 内静态配置、精确字段路由和 JSONL 读取；不能证明宿主 Hook、MCP、模型、
认证、子 Agent 或工具已启用。失败则记 `partial`，不回滚已完成的 Skill 登记。

## 8. 停止条件

以下任一情况立即停止，不猜测、不覆盖、不扩大权限：

- 授权、来源身份、目标、范围或 revision 不清楚；
- 当前 CLI 帮助与命令不兼容，或必需工具缺失；
- 远程/本地 `--list` 不是精确 8 项；
- conflict 无法标为 `replaceable`，或 same-source/absent 无法可靠区分；
- 方案 A 缺少旧 repository、固定 revision、影响 Agent/scope、精确恢复命令或移除后 JSON 证明；
- 默认官方 checkout 校验失败；已有本地开发 checkout 仅在可信验证器缺失时可降级为 `partial`；
- 安装失败、部分成功、after diff 异常或无法计算精确新增集合；
- 继续操作需要覆盖、广泛删除、修改权限或系统依赖；
- 全局 `$CODEX_HOME/AGENTS.md` 为符号链接、非普通文件、父目录不可用，或已存在、非空且与
  `AGENTS-PERNAVO.md` 不同；
- Claude `settings.json`、Codex `hooks.json`、Cursor `hooks.json` 或 Grok
  `hooks/pernavo.json` 为符号链接、非普通文件、无效 JSON，或所需事件存在但不是可追加的数组；
- 用户要求保证运行时触发，但宿主没有可观察证据。

部分安装失败时，对 before/after 差集中的新增名称定向移除；对已经替换的名称按替换台账恢复旧
来源。任一恢复前提缺失时停止并报告实际状态，不得继续扩大删除范围。

## 9. 安装报告模板

```text
Authorized user / target agents / scope / mode:
CLI agent selector and version:
CLI-enumerated supported agents:
CLI-rejected or unsupported global agents:
Discovery remote URL and --list result:
Fixed checkout path:
Verified full commit SHA:
Installed content hash/revision evidence:
Source working-tree state:
Secure temporary directory and permission check:
skills CLI version and help checked:
Requested 8 names or authorized subset:
Remote/local --list exact-set result:
Before global JSON snapshot path (no `ls --agent '*'`):
Per-name classification: absent | same-source | conflict
Conflict disposition: replaceable | blocked
Replacement ledger: name, agent, scope, old repository, old full SHA, restore command
Directed removal command and post-removal JSON result:
Install/update command and exit status:
AGENTS.md path and distribution: created | replaced-empty | skipped-identical | blocked-existing | blocked-symlink | blocked-not-file | blocked-parent | blocked-source-missing
Claude rules/pernavo.md: created | replaced-empty | skipped-identical | blocked-*
Cursor rules/pernavo.mdc: created | replaced-empty | skipped-identical | blocked-*
Grok rules/pernavo.md: created | replaced-empty | skipped-identical | blocked-*
Exact rollback for created AGENTS.md:
Exact rollback for replaced-empty AGENTS.md:
API test Stop hook script path (materialized, not checkout):
Claude settings.json: created | merged | skipped-identical | blocked-parent | blocked-symlink | blocked-not-file | blocked-invalid | blocked-format
Codex hooks.json: created | merged | skipped-identical | blocked-parent | blocked-symlink | blocked-not-file | blocked-invalid | blocked-format
Cursor hooks.json: created | merged | skipped-identical | blocked-parent | blocked-symlink | blocked-not-file | blocked-invalid | blocked-format
Grok hooks/pernavo.json: created | merged | skipped-identical | blocked-parent | blocked-symlink | blocked-not-file | blocked-invalid | blocked-format
Before/after Hook command lists proving pre-existing entries remain:
Exact rollback for this Stop hook entry only:
`--check` result:
`~/.pernavo/hooks/runtime-hook.py`: copied | skipped-identical | blocked-home | blocked-not-dir
Runtime log path:
Runtime hook events merged (claude/codex/cursor/grok): created | merged | skipped-identical | blocked-*
Exact rollback for runtime-hook.py entries only (keep logs):
After global JSON snapshot path:
Structured before/after diff and newly created registrations:
Installed names, paths, scopes, sources, target agents, materialized SHA-256:
Agent status: registered | materialized | shared-registration | unsupported-global | blocked-source
Default `--agent '*'` harness coverage and unsupported-global list:
Readonly agentctl doctor/explain/memory result:
New-session/restart status:
Representative 3-case smoke: cases, expected/forbidden/actual owners, result
Full 24-case corpus: result | not run; remaining activation unverified
Observed child-agent/tool execution:
Per-case target-observed evidence:
External environment-observed evidence, or not observed:
Harness checks (default readonly agentctl):
Exact rollback command for only newly created name+agent registrations:
Exact rollback sequence for replaced registrations:
Unverified layers and remaining decisions:
Final evidence level: source-valid | installed | loaded | executed | target-observed | environment-observed
Final status: complete | partial | blocked
```

只有获授权的 absent 项完成安装、方案 A 的 replaceable conflict 已正确换源、after diff 已核对、
`AGENTS.md` 为 `created`、`replaced-empty` 或 `skipped-identical`、各可用宿主的 Stop 门禁与运行日志 Hook 为
`created`、`merged` 或 `skipped-identical`、只读 `agentctl` 已跑、回滚步骤可执行、失败项已处理且未验证边界明确
列出时，安装代理才可结束任务。
