# Pernavo AI 安装执行手册

## AI 读取入口

公开仓库网页：[https://github.com/tuloong/pernavo](https://github.com/tuloong/pernavo)

完整指南 Raw URL：
[https://raw.githubusercontent.com/tuloong/pernavo/refs/heads/main/AI_INSTALL.md](https://raw.githubusercontent.com/tuloong/pernavo/refs/heads/main/AI_INSTALL.md)

### For Humans

把下面整段提示词复制给 Codex、Claude Code、Cursor 或其他编码 Agent：

```text
Install and configure Pernavo by following the complete instructions here:
https://raw.githubusercontent.com/tuloong/pernavo/refs/heads/main/AI_INSTALL.md

Read the entire guide before acting. If the URL is unavailable or the repository does not expose
the 14 Skills declared by the guide, stop and report that the requested version is not published.
Do not fall back to older README installation commands.
```

### For LLM Agents

获取完整指南，然后逐步执行：

```bash
curl -fsSL https://raw.githubusercontent.com/tuloong/pernavo/refs/heads/main/AI_INSTALL.md
```

这条命令只输出 Markdown，不得把它通过管道交给 Shell。`curl` 非零退出、空响应或返回内容
不是本文件时必须停止。

也可以先读取仓库页面，再定位本文件：

> 请先读取公开仓库 `https://github.com/tuloong/pernavo`，在仓库中打开
> `AI_INSTALL.md`，然后严格按照文档的权限门、冲突预检、安装后验证和定向回滚流程执行。
> 如果远程仓库中不存在 `AI_INSTALL.md`，或者 `--list` 结果不是文档声明的 14 个 Skill，
> 立即停止并报告版本尚未发布，不要退回旧 README 的安装命令。

本文件供自动化 AI 安装代理使用。它描述如何安装本仓库的 Skills、如何检查只读
Harness，以及如何证明安装到了哪一层。不要把本文当成可以直接执行的 Shell 脚本；
安装代理必须逐步检查前置条件、权限和每条命令的输出。

本文在 2026-07-31 使用 `skills` CLI 1.5.21 核对。CLI 行为可能变化，执行前必须重新
运行 `npx --yes skills --help`，并以当前帮助输出为准。

## 1. 安装代理契约

安装代理必须遵守以下规则：

1. 先确认用户授权的目标 Agent、安装范围和来源，再执行写操作。
2. 默认只安装到当前用户的 Codex；不得自行扩大到所有 Agent、项目或系统用户。
3. 保留用户已有 Skills、配置、记忆和未提交工作。不得用通配删除、递归删除或
   `skills remove --all` 清理环境。
4. 如果同名 Skill 已来自其他来源，停止并报告冲突。只有用户明确同意且旧来源可恢复时
   才能替换。
5. 在本仓库自己的 checkout 中不得做项目级自安装；它会产生 `.agents/skills` 副本，
   与 `skills/` 源文件竞争。
6. 安装 Skills 不等于安装 Harness、Hook、MCP、工具权限或记忆写入器。
7. 不得把“命令成功”“已列出 Skill”或模型自述升级为“运行时已触发”。
8. 遇到本文的停止条件时立即停止，不要猜测、覆盖或自动修复用户环境。

## 2. 证明层级

安装报告必须区分以下层级：

| 层级 | 可接受证据 | 不能证明 |
|------|------------|----------|
| `source-valid` | 仓库校验通过，或远程来源列出了预期 Skills | 已写入目标 Agent |
| `installed` | `skills ls --global --agent <agent> --json` 显示名称、范围和来源 | 当前会话已重新加载 |
| `loaded` | 目标宿主记录了对应 `SKILL.md` 正文读取或等价加载事件 | Skill 内工具实际可用 |
| `executed` | 目标工具、Hook、MCP 或 Harness 命令真实执行并有结果 | 未观察环境或生产状态 |

最终结论只能到达实际观察到的最高层级。

## 3. 预期 Skill 集合

当前本地源应包含以下 14 个 Skill：

```text
audit-agent-harness
aviation-grade-engineering
codebase-slimming
coding-task-controller
develop-production-code
engineering-work-system
exa-search
gpt55-fusion
graph-engineering
plan-code-change
pplx-cli
review-mr
unknowns-field-guide
verify-change-evidence
```

远程仓库可能落后于本地未提交改动。远程来源没有列出完整集合时，不得声称安装的是本版本。

## 4. 收集安装输入

开始前记录：

- 用户授权的目标 Agent，例如 `codex`；
- 用户授权的范围：默认 `global`，即当前用户级；
- 来源：本地 checkout 的绝对路径，或
  `https://github.com/tuloong/pernavo`；
- 安装全部 14 个 Skill，还是用户点名的子集；
- 是否允许网络访问和当前用户目录写入；
- 是否要求同时检查只读 Harness。

如果用户只说“安装到本机”，默认目标是当前使用的 Agent，不是 `--agent '*'`。

## 5. 只读预检

运行并记录版本：

```bash
git --version
node --version
npx --yes skills --version
python3 --version
npx --yes skills --help
```

要求：

- 安装 Skills 需要 Node.js 和 `npx`；
- 本地 Harness 需要 Python 3.9 或更高版本；
- 完整仓库校验还需要 Git、Ruby，以及 Codex `skill-creator` 提供的
  `quick_validate.py`，或显式设置的可信 `PERNAVO_SKILL_VALIDATOR`。

任何必需命令缺失时停止。不得静默安装系统软件或修改 Shell 启动文件。

### 5.1 本地来源

把占位符替换为用户确认的绝对路径：

```bash
PERNAVO_SOURCE="/absolute/path/to/pernavo"
git -C "$PERNAVO_SOURCE" rev-parse --show-toplevel
git -C "$PERNAVO_SOURCE" rev-parse HEAD
git -C "$PERNAVO_SOURCE" status --short
npx --yes skills add "$PERNAVO_SOURCE" --list
```

如果路径不是预期仓库，立即停止。若工作树非干净状态，先报告将要安装的是“包含本地未提交
内容的工作树”；只有用户明确授权安装该工作树时才继续。

在本地开发源中还要运行：

```bash
cd "$PERNAVO_SOURCE"
./scripts/validate-skills.sh
```

预期当前输出包括：

```text
14 frontmatters, links, README entries, and trigger triplets valid
PASS: 14 skills validated and listed; corpus has 42 cases.
```

如果唯一失败是找不到 `quick_validate.py`，可将
`PERNAVO_SKILL_VALIDATOR` 指向用户已经信任的验证器绝对路径后重试。不得为了通过校验
自动下载或覆盖系统 Skill；无法取得可信验证器时，将本地完整校验标记为 `partial`。

### 5.2 GitHub 来源

```bash
PERNAVO_SOURCE="https://github.com/tuloong/pernavo"
npx --yes skills add "$PERNAVO_SOURCE" --list
```

远程安装前必须检查列出的名称。缺少预期 Skill、出现额外未知 Skill 或来源解析失败时停止。
若用户要求可复现安装，应先取得用户确认的 commit/tag，并从该固定 revision 的 checkout
执行本地来源流程；不要把可变 `main` 描述为固定版本。

## 6. 冲突预检

先读取全部全局登记，再读取默认 Codex 目标：

```bash
npx --yes skills ls --global --json
npx --yes skills ls --global --agent codex --json
```

只检查“预期 Skill 集合”中的同名条目，并记录每项的 `name`、`path`、`scope`、`source`、
`sourceUrl` 和全部目标 Agent。为本次目标 Agent 建立安装前快照，把请求名称逐项标记为：

- `absent`：目标 Agent 安装前没有该名称；
- `present-same-source`：目标 Agent 已有该名称且来源相同；
- `conflict`：任一全局登记的同名项来自其他来源，或来源无法判断。

安装后新增登记集合等于“安装后目标 Agent 名称集合减去安装前目标 Agent 名称集合”。后续自动
回滚只能移除这个差集，不能按请求清单或当前包清单推断。

- 请求名称全部为 `absent`：可以执行首次安装。
- 同名项来自 canonical `tuloong/pernavo`：若用户要求更新，走“更新”流程；否则报告已安装并停止。
- 迁移兼容：若既有登记仍显示旧 URL `tuloong/loongclaude`，只有通过 GitHub redirect 或
  `gh repo view` 证明它与 canonical `tuloong/pernavo` 是同一 repository，才能按
  `present-same-source` 处理；否则为 `conflict`。
- 同时存在 `absent` 和 `present-same-source`：只允许安装明确列出的 `absent` 子集；已有项保持
  不动。若还要更新已有项，必须作为单独操作经过“更新”权限门。
- 同名项来自其他来源，或来源字段无法判断：停止并请求用户决定。

不得通过删除同名目录、修改 symlink 或运行 `remove --all` 解决冲突。

## 7. 安装

以下命令会写入当前用户的 Agent Skill 目录。只有完成授权和冲突预检后才能执行。

### 7.1 默认：安装全部 Skill 到 Codex

只有安装前快照证明 14 个请求名称对 Codex 全部为 `absent` 时，才允许执行本段的
`--skill '*'` 命令。只要存在 `present-same-source`，本段即禁止执行，必须改用 7.2，并只写
`absent` 名称。

```bash
npx --yes skills add "$PERNAVO_SOURCE" \
  --global \
  --agent codex \
  --skill '*' \
  --yes \
  --copy
```

`--copy` 避免目标 Agent 依赖开发 checkout 的活动 symlink。不得省略 `--global` 后在本仓库
根目录运行，否则可能创建项目级自安装副本。

### 7.2 只安装用户点名的 Skill

下面只是语法示例；将名称替换为用户明确选择、且安装前快照标记为 `absent` 的集合：

```bash
npx --yes skills add "$PERNAVO_SOURCE" \
  --global \
  --agent codex \
  --skill plan-code-change verify-change-evidence \
  --yes \
  --copy
```

### 7.3 安装到多个 Agent

把 `codex` 替换为 CLI 当前帮助中支持、且用户明确授权的 Agent 名称。只有用户明确要求
“所有支持的 Agent”时才允许使用 `--agent '*'`。不要默认使用 `--all`，因为它同时选择全部
Skills、全部 Agents 并跳过确认，影响范围过宽。

## 8. 安装后验证

再次读取安装状态：

```bash
npx --yes skills ls --global --agent codex --json
```

验证并记录：

1. 用户选择的每个名称恰好出现；
2. `scope` 是 `global`；
3. 来源与授权来源一致；
4. 没有意外写入未授权 Agent；
5. 仓库 checkout 内没有新增 `.agents/skills/<name>/SKILL.md` 自安装副本。

随后让用户重启目标 Agent，或开启一个确定会重新扫描 Skills 的新会话。不要声称当前旧会话
自动获得了新 Skill。

### 8.1 运行时触发验证

安装清单只能证明 `installed`。要证明 `loaded`：

1. 在新会话中选择 `tests/skill-trigger-corpus.tsv` 的一个正向、一个负向和一个相邻碰撞请求；
2. 使用目标宿主提供的日志、trace 或工具事件，观察对应 `SKILL.md` 正文是否真实加载；
3. 正向用例应加载目标 Skill，负向用例不应加载它，碰撞用例只加载请求所需的责任所有者；
4. 记录宿主、版本、会话、请求、实际加载集合和原始事件位置。

如果宿主不暴露正文加载事件，状态必须写成
`installed; runtime activation unverified`。模型回复“我已使用某 Skill”不是加载证据。

## 9. Harness 与记忆检查

`skills` CLI 不安装 `scripts/agentctl.py`、`harness/`、Hook、MCP 或工具权限。需要检查
Harness 时必须保留一个本地 checkout，并从仓库根目录运行：

```bash
python3 scripts/agentctl.py doctor \
  --config harness/examples/agentctl.json \
  --json

python3 scripts/agentctl.py explain \
  --config harness/examples/agentctl.json \
  --event harness/examples/event.json \
  --json

python3 scripts/agentctl.py memory search \
  --config harness/examples/agentctl.json \
  --query canonical \
  --json
```

Phase 1 的 `agentctl` 只读取本地配置和 JSONL：它不写文件、不运行 Hook、不启动进程、
不连接网络，也不调用 Agent 工具。`harness/examples/memory.jsonl` 是示例权威输入；
`MEMORY.md` 目前不是输入或自动投影目标。

上述三条命令成功只能证明静态配置、精确字段路由和 JSONL 读取有效，不能证明宿主已启用
Hook、认证、MCP、模型或工具。

## 10. 更新（默认失败关闭）

`skills` CLI 1.5.21 的 `update` 没有 `--agent` 参数，也不接收本地路径或指定 revision。
它按已记录来源更新全局同名 Skill，因此不能保证只影响 Codex，也不能把本地 dirty checkout
应用成一次可证明的更新。

默认处理如下：

- 用户只授权 Codex：停止自动更新，报告
  `blocked: skills update has no agent scope`。
- 来源是本地 checkout 或用户要求固定 revision：停止自动更新；不得把 `skills update` 当成
  本地来源刷新。只有用户另行批准可恢复的卸载/重装方案后才能继续。
- 只有当全部全局同名登记都来自 canonical `tuloong/pernavo`，且用户明确授权这些登记中列出的
  每一个 Agent 一起更新时，才允许使用下面的按名称命令。

在满足最后一种条件时，先重新执行来源检查、`--list`、全局快照和仓库校验，再运行：

```bash
npx --yes skills update --global --yes \
  audit-agent-harness \
  aviation-grade-engineering \
  codebase-slimming \
  coding-task-controller \
  develop-production-code \
  engineering-work-system \
  exa-search \
  gpt55-fusion \
  graph-engineering \
  plan-code-change \
  pplx-cli \
  review-mr \
  unknowns-field-guide \
  verify-change-evidence
```

上例只适用于用户授权更新完整 14 项的情况；若授权的是子集，命令中只能保留该子集的字面量
名称。不得把“当前仓库包含 14 项”推断成“用户授权更新 14 项”。

该命令跟随已记录的远程来源，不能证明使用了当前本地内容或用户指定 revision。更新后重新
执行全局快照、各授权 Agent 的安装状态和运行时触发验证。`skills update -g` 不带名称可能
更新用户其他全局 Skills，因此禁止作为本包的默认更新命令。

## 11. 定向回滚

首次安装前若发现同名旧版本，必须先记录其可恢复来源和 revision；否则不得替换，也就没有
可靠的自动回滚。

回滚时使用安装前、安装后快照计算出的“新增目标 Agent 登记集合”，并把集合中的名称逐个
写成字面量。下面只展示命令形状，不可原样执行：

```text
npx --yes skills remove NEW_NAME_1 NEW_NAME_2 --global --agent codex --yes
```

只有安装前快照证明 `NEW_NAME_1`、`NEW_NAME_2` 在 Codex 中不存在时，才能替换为真实名称并
执行。请求清单中的其他名称如果安装前已经存在，禁止放入移除命令。

如果只安装了子集，回滚时只能使用该子集中的新增登记。如果安装到了多个 Agent，分别按
每个 Agent 的快照差集定向移除；不要使用 `--all`。移除后再次运行
`skills ls --global --agent codex --json`，确认安装前已有登记仍在，只删除了本次新增登记。

更新或获准替换的旧版本不属于“新增登记”，不能通过删除来回滚。必须按照预先记录的旧来源
和固定 revision 恢复，再验证名称、来源和目标 Agent。没有旧 revision、恢复来源或 Agent
级影响范围时，状态必须是 `rollback blocked`，不得声称回滚完成。

## 12. 失败处理与停止条件

遇到以下任一情况立即停止：

- 来源路径、仓库身份或 revision 无法确认；
- `--list` 没有得到预期 Skill 集合；
- 本地完整校验失败，且失败不是已经明确记录的验证器缺失；
- 存在未经授权的同名来源冲突；
- 安装命令非零退出，或只安装了部分名称；
- 安装后名称、范围、来源或目标 Agent 不符合授权；
- 无法区分安装前已有登记与本次新增登记；
- 需要覆盖、删除、修改权限或安装系统依赖才能继续；
- 实际宿主没有可观察的加载事件，却被要求保证自动触发。

部分安装失败时，把安装后目标 Agent 登记与安装前快照比较，只对差集中新增的精确名称执行
定向回滚。不得通过请求清单猜测新增项，也不得通过清空整个 Skill 目录恢复。

## 13. 安装报告模板

安装代理最终必须返回：

```text
Source URL/path and revision:
Source working-tree state:
skills CLI version:
Authorized target agents and scope:
Requested skill names:
Pre-existing same-name entries and decision:
Pre-install target-agent registration snapshot:
Source validation commands and results:
Install command and exit status:
Installed names, paths, scopes, and sources:
New target-agent registrations computed from the before/after diff:
Host restart/new-session status:
Runtime body-load evidence, or exact reason unavailable:
Harness checks executed and results:
Memory format and path actually inspected:
Rollback command for only the newly created target-agent registrations:
Updated/replaced entries and their recorded restore source/revision:
Unverified layers and remaining human decisions:
Final status: source-valid | installed | loaded | executed | partial | blocked
```

只有用户授权的 Skill 已安装、安装状态已复查、失败项已处理且未验证层明确列出时，安装任务
才可以结束。
