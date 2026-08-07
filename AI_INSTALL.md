# Pernavo AI 安装执行手册

## 复制给安装 AI 的提示词

```text
请为我安装 Pernavo 的完整 Skills 系统。完整执行手册：
https://raw.githubusercontent.com/ianbyte-byte/pernavo/refs/heads/main/AI_INSTALL.md

默认参数：来源使用官方 GitHub 仓库 https://github.com/ianbyte-byte/pernavo；安装给当前用户的
Codex；范围为 global；目标为手册列出的全部 16 个 Skills；安装方式为固定 SHA checkout
中的 copy。远程 URL 只用于发现和 clone，不直接作为安装源。

开始前必须读取完整手册，重新检查 skills CLI 的 version/help，确认写入授权，精确核对远程
--list 的 16 项，并用 JSON 快照检查同名冲突。不要直接盲跑安装命令，不要使用 --all，
不要使用 remove --all。若远程 --list 不是精确 16 项，停止并说明该版本尚未发布。
安装后按手册完成 JSON diff、新会话触发验证、报告和可定向回滚记录。
```

本手册供 AI 安装代理逐步执行，不是 Shell 脚本。上述默认值只补全用户未指定的参数，不能
替代授权、全文阅读、冲突检查或逐步验证。若本 Raw URL 不可用、为空或不是本文件，立即停止；
不得退回 README 中的旧命令，也不得宣称当前本地未提交内容已经发布到远程。

本文曾用 `skills` CLI 1.5.21 验证。CLI 会变化，每次安装仍必须重新读取当前
`npx --yes skills --help` 以及相关子命令帮助，并以当次输出为准。

## 默认成功路径

| 顺序 | 操作 | 通过条件 |
|---|---|---|
| 1 | 确认写入授权 | 当前用户、Codex、global、官方来源、16 项、copy 均获授权 |
| 2 | 检查 CLI | version 和 help 可用，参数与本手册兼容 |
| 3 | 远程 `--list` | 名称集合精确等于下方 16 项；远程 URL 仅用于发现 |
| 4 | 固定来源 | 安全临时目录中 clone，记录 full HEAD SHA，detach、校验 16 项 |
| 5 | 保存全局及 Codex JSON 快照 | 安装前状态可恢复、可比较 |
| 6 | 分类同名项 | 每项是 `absent`、`same-source` 或 `conflict` |
| 7 | 只从固定 checkout 安装 `absent` | `same-source` 不触碰；任何 `conflict` 都停止 |
| 8 | 安装后 JSON diff | 只新增获授权的 absent 项，无意外 Agent 或范围 |
| 9 | 新会话验证 | 3 个代表性 smoke，或完整 48-case corpus |
| 10 | 报告与回滚 | 区分证据层级，只为本次新增登记给出定向回滚 |

## 安全契约与系统边界

安装代理必须遵守：

1. 写入前确认用户授权的来源、当前系统用户、目标 Agent、范围、名称集合和 copy/symlink
   方式。默认只写当前用户的 Codex global Skills。
2. 保留既有 Skills、配置、记忆、目录和未提交工作。不得通配删除、递归清理、修改 Shell
   启动文件、静默安装系统依赖或运行 `skills remove --all`。
3. 不在 Pernavo 自己的 checkout 中做项目级自安装；那会创建 `.agents/skills` 副本并与
   `skills/` 源竞争。
4. 只安装 `absent`；`same-source` 保持不变；`conflict` 必须停止并请用户决定。
5. 安装 16 个 Skills 会提供成本感知的自动工作流政策，包括 controller、work-system 和
   graph 路由规则。它不会安装或证明宿主的子 Agent 目录、模型路由、Hook、MCP、权限、
   Harness 或记忆写入器。
6. 真正的子 Agent 派生，以及 Skill 是否 `loaded`/`executed`，只能在安装后的宿主新会话中
   观察；命令成功、目录存在或模型自述均不是运行时证明。

### 证据层级

| 层级 | 可接受证据 | 不能证明 |
|---|---|---|
| `source-valid` | 固定 checkout 校验通过，或远程 `--list` 精确列出预期集合 | 已写入目标 Agent |
| `installed` | 安装后 global/Codex JSON 快照显示正确名称、范围和来源 | 新会话已加载正文 |
| `loaded` | 宿主 trace、日志或等价事件显示对应 `SKILL.md` 正文被加载 | Skill 内工具实际执行 |
| `executed` | 目标工具、子 Agent、Hook、MCP 或 Harness 确有执行结果 | 外部目标状态已改变 |
| `target-observed` | 用例要求的 expected owners 全部加载，且 forbidden owners 均未加载 | 交付、部署或外部环境行为正确 |
| `environment-observed` | 对授权的外部目标环境做独立观测，结果与预期一致 | 其他未观测环境也一致 |

结论只能到达实际证据支持的最高层级；无法观察正文加载时应报告
`installed; runtime activation unverified`。

## 唯一预期的 16 个 Skills

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
project-capability-engineering
repository-knowledge-gardening
review-mr
unknowns-field-guide
verify-change-evidence
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

输出必须精确对应上述 16 个名称。如果不是，停止并说明：远程版本尚未发布或与本手册不一致。
该 URL 指向可变远程，只能证明发现时的列表，不能作为 installed revision 证据，也不能把当前
本地 dirty 内容当成远程内容。

### 固定默认安装来源

创建仅当前用户可访问的新临时目录，验证路径确为本次新目录，然后 clone 官方仓库。不得使用
已有路径，不得覆盖内容：

```bash
umask 077
PERNAVO_INSTALL_TMP="$(mktemp -d "${TMPDIR:-/tmp}/pernavo-install.XXXXXX")"
test -n "$PERNAVO_INSTALL_TMP"
test -d "$PERNAVO_INSTALL_TMP"
test ! -L "$PERNAVO_INSTALL_TMP"
chmod 700 "$PERNAVO_INSTALL_TMP"
PERNAVO_CHECKOUT="$PERNAVO_INSTALL_TMP/checkout"
test ! -e "$PERNAVO_CHECKOUT"
git clone "$PERNAVO_REMOTE" "$PERNAVO_CHECKOUT"
git -C "$PERNAVO_CHECKOUT" fetch --all --tags
PERNAVO_COMMIT_SHA="$(git -C "$PERNAVO_CHECKOUT" rev-parse --verify 'HEAD^{commit}')"
git -C "$PERNAVO_CHECKOUT" checkout --detach "$PERNAVO_COMMIT_SHA"
git -C "$PERNAVO_CHECKOUT" rev-parse --verify 'HEAD^{commit}'
npx --yes skills add "$PERNAVO_CHECKOUT" --list
"$PERNAVO_CHECKOUT/scripts/validate-skills.sh"
```

再次确认 checkout 的列表精确为 16 项、校验通过，并在报告中记录完整 SHA。若用户要求指定
revision，先确认该 full commit SHA 存在，再 detach 到该 SHA 后执行相同校验。不得把 branch、
tag 或远程 `main` 名称当成安装 revision。

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
test ! -e "$PERNAVO_INSTALL_TMP/pernavo-before-codex.json"
npx --yes skills ls --global --json > "$PERNAVO_INSTALL_TMP/pernavo-before-global.json"
npx --yes skills ls --global --agent codex --json > "$PERNAVO_INSTALL_TMP/pernavo-before-codex.json"
```

对 16 个请求名称逐项读取 `name`、`path`、`scope`、`source`、`sourceUrl` 和 Agent 登记，并分类：

- `absent`：Codex 中无同名登记，且其他全局登记没有不明同名来源；可安装。
- `same-source`：已来自同一个官方仓库；本次不触碰、不重装、不隐式更新。
- `conflict`：来自其他来源，或来源无法可靠判断；停止并报告。

如果旧来源显示 `tuloong/loongclaude`，只有能证明它与官方仓库是同一 repository 时才可视为
`same-source`，否则是 `conflict`。混合状态下只把 `absent` 名称放进安装命令。

安装前必须同时保存：16 项分类、原始 JSON、已授权目标，以及“安装后 Codex 名称集合减安装前
Codex 名称集合”的回滚计算规则。不得根据请求列表猜测新增项。

## 3. 安装

只有 16 项全部是 `absent` 时，才可使用星号选择全部 Skills。安装源必须是已经 detach、记录
full SHA 并校验通过的 `$PERNAVO_CHECKOUT`，不能是 `$PERNAVO_REMOTE`：

```bash
npx --yes skills add "$PERNAVO_CHECKOUT" \
  --global \
  --agent codex \
  --skill '*' \
  --yes \
  --copy
```

存在任何 `same-source` 时，必须把所有 `absent` 名称逐个写出；下面仅示范命令形状：

```text
npx --yes skills add "$PERNAVO_CHECKOUT" \
  --global \
  --agent codex \
  --skill ABSENT_NAME_1 ABSENT_NAME_2 \
  --yes \
  --copy
```

若没有 `absent`，报告已存在且不做写入。只有用户明确授权所有支持的 Agent 时才可使用
`--agent '*'`。任何情况下都不使用 `--all` 作为默认安装方式。

## 4. 安装后 diff 与新会话验证

验证安全临时目录和新文件名后保存安装后快照：

```bash
test -n "$PERNAVO_INSTALL_TMP"
test -d "$PERNAVO_INSTALL_TMP"
test ! -L "$PERNAVO_INSTALL_TMP"
test ! -e "$PERNAVO_INSTALL_TMP/pernavo-after-global.json"
test ! -e "$PERNAVO_INSTALL_TMP/pernavo-after-codex.json"
npx --yes skills ls --global --json > "$PERNAVO_INSTALL_TMP/pernavo-after-global.json"
npx --yes skills ls --global --agent codex --json > "$PERNAVO_INSTALL_TMP/pernavo-after-codex.json"
```

对 before/after JSON 做结构化比较并确认：请求的 absent 项各出现一次、scope 为 global、来源
一致、没有写入未授权 Agent、same-source 项未改变。checkout 内不得新增项目级
`.agents/skills/<name>` 副本。非零退出、部分安装或意外 diff 均进入停止/回滚流程。

随后重启目标宿主或开启确定会重新扫描 Skills 的新会话。从
`tests/skill-trigger-corpus.tsv` 选择并记录：

1. 一个正向请求：应加载目标 Skill；
2. 一个负向请求：不应加载目标 Skill；
3. 一个相邻责任碰撞请求：所有 expected owners 都应加载，所有 forbidden owners 均不应加载。

这 3 个案例只是代表性 smoke，只验证所选 Skill 的用例合同，不能证明其余 15 项或完整系统
routing。要验证全部系统 routing，必须在独立新上下文中运行全部 48 个 corpus cases，并逐项
核对完成事件、全部 expected owners 和全部 forbidden owners。完整运行成本较高，可以由用户
选择跳过；未运行时必须将其余 runtime activation 标为 unverified，不能声称 16 项均已验证。

记录宿主/version、会话、安装 SHA、请求、expected/forbidden/实际加载集合、正文加载事件位置，
以及真实子 Agent/工具是否执行。只有所有 expected owners 齐全且没有 forbidden owner，才达到
该用例的 `target-observed`。对授权外部环境的独立实际观测另记为 `environment-observed`，不能
与路由层混淆。宿主不暴露事件时，明确保留 `loaded`、`executed`、`target-observed` 和
`environment-observed` 未验证边界。

## 5. 更新：默认失败关闭

CLI 1.5.21 的 `update` 没有 Agent scope。用户只授权 Codex、来源是本地 checkout、要求固定
revision，或无法枚举所有受影响的全局登记时，停止并报告：

```text
blocked: skills update has no agent scope
```

只有全部同名全局登记均来自官方来源，且用户明确授权所有受影响登记一起更新时，才可按字面
名称更新。例如用户授权完整 16 项时：

```bash
npx --yes skills update --global --yes \
  audit-agent-harness aviation-grade-engineering codebase-slimming \
  coding-task-controller develop-production-code engineering-work-system \
  exa-search gpt55-fusion graph-engineering plan-code-change pplx-cli \
  project-capability-engineering repository-knowledge-gardening review-mr \
  unknowns-field-guide verify-change-evidence
```

授权子集时只能保留该子集。更新前后重复来源检查、`--list` 和 JSON 快照。不得使用无名称的
`skills update -g` 作为本包默认更新命令。

## 6. 定向回滚

回滚集合只能是 `after Codex registrations - before Codex registrations`。把实际新增名称逐个写成
字面量：

```text
npx --yes skills remove NEW_NAME_1 NEW_NAME_2 --global --agent codex --yes
```

上例不可原样执行。不得移除安装前已存在的 same-source 项，不得使用通配符或
`remove --all`。多 Agent 安装要按每个 Agent 的快照差集分别移除，随后重新读取 JSON，证明只
删除本次新增登记。

更新或获准替换的旧版本不是“新增登记”；只有预先记录旧来源和固定 revision，才能按该来源
恢复。缺少恢复来源、revision 或影响范围时报告 `rollback blocked`，不得假称已回滚。

## 7. Harness 检查（可选、独立授权）

Skills 安装不会安装 `scripts/agentctl.py`、`harness/`、Hook、MCP、权限或宿主路由。用户要求
检查只读 Harness 时，保留 checkout 并从仓库根目录运行：

```bash
python3 scripts/agentctl.py doctor --config harness/examples/agentctl.json --json
python3 scripts/agentctl.py explain --config harness/examples/agentctl.json \
  --event harness/examples/event.json --json
python3 scripts/agentctl.py memory search --config harness/examples/agentctl.json \
  --query canonical --json
```

这些命令只证明本地静态配置、精确字段路由和 JSONL 读取；不能证明宿主 Hook、MCP、模型、
认证、子 Agent 或工具已启用。

## 8. 停止条件

以下任一情况立即停止，不猜测、不覆盖、不扩大权限：

- 授权、来源身份、目标、范围或 revision 不清楚；
- 当前 CLI 帮助与命令不兼容，或必需工具缺失；
- 远程/本地 `--list` 不是精确 16 项；
- 存在 conflict，或 same-source/absent 无法可靠区分；
- 默认官方 checkout 校验失败；已有本地开发 checkout 仅在可信验证器缺失时可降级为 `partial`；
- 安装失败、部分成功、after diff 异常或无法计算精确新增集合；
- 继续操作需要覆盖、广泛删除、修改权限或系统依赖；
- 用户要求保证运行时触发，但宿主没有可观察证据。

部分安装失败时，只对 before/after 差集中的字面名称定向回滚。

## 9. 安装报告模板

```text
Authorized user / agent / scope / mode:
Discovery remote URL and --list result:
Fixed checkout path:
Verified full commit SHA:
Installed content hash/revision evidence:
Source working-tree state:
Secure temporary directory and permission check:
skills CLI version and help checked:
Requested 16 names or authorized subset:
Remote/local --list exact-set result:
Before global and Codex JSON snapshot paths:
Per-name classification: absent | same-source | conflict
Install/update command and exit status:
After global and Codex JSON snapshot paths:
Structured before/after diff and newly created registrations:
Installed names, paths, scopes, sources, and target agents:
New-session/restart status:
Representative 3-case smoke: cases, expected/forbidden/actual owners, result
Full 48-case corpus: result | not run; remaining activation unverified
Observed child-agent/tool execution:
Per-case target-observed evidence:
External environment-observed evidence, or not observed:
Harness checks, if separately requested:
Exact rollback command for only newly created registrations:
Unverified layers and remaining decisions:
Final evidence level: source-valid | installed | loaded | executed | target-observed | environment-observed
Final status: complete | partial | blocked
```

只有获授权的 absent 项完成安装、after diff 已核对、失败项已处理且未验证边界明确列出时，安装
代理才可结束任务。
