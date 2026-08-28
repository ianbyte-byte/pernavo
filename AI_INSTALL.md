# Pernavo AI 安装执行手册

## 复制给安装 AI 的提示词

```text
请为我安装 Pernavo 的完整 Skills 系统。完整执行手册：
https://raw.githubusercontent.com/ianbyte-byte/pernavo/refs/heads/main/AI_INSTALL.md

默认参数：来源使用官方 GitHub 仓库 https://github.com/ianbyte-byte/pernavo；安装给当前用户的
**所有支持 global 安装的 agents**；范围为 global；目标为手册列出的全部 8 个 Skills；安装
方式为固定 SHA checkout 中的 copy。CLI 使用 `--agent '*'`，不是只安装 Codex。远程 URL 只用于
发现和 clone，不直接作为安装源。

开始前必须读取完整手册，重新检查 skills CLI 的 version/help，确认写入授权，精确核对远程
--list 的 8 项，并用 JSON 快照检查同名冲突。不要直接盲跑安装命令，不要使用 --all，
不要使用 remove --all。遇到来源不同的同名项时，默认采用方案 A：保存可精确恢复的旧登记后，
仅按名称定向移除冲突项，再从固定 SHA checkout 重装；旧来源、revision 或影响范围无法可靠
恢复时必须停止。若远程 --list 不是精确 8 项，停止并说明该版本尚未发布。
安装后按手册完成 JSON diff、新会话触发验证、报告和可定向回滚记录。
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
| 目标 | 当前用户所有支持 global 安装的 agents |
| CLI 目标选择 | `--agent '*'`；不要把显示名称（如 `Claude Code`）当作 CLI ID |
| 范围 | global |
| 内容 | 下方完整的 8 个 Skills |
| 复制方式 | `--copy` |
| 冲突策略 | 方案 A；来源无法恢复时 `blocked` |

`--agent '*'` 表示当前 CLI 支持的全部 agent 目标，不等于“只安装当前会话使用的 agent”。
不同版本可能枚举不同数量；必须记录当次 CLI 输出中的实际 agent 列表和不支持 global 的目标，
不能把旧版本的数量写死为成功条件。当前 `skills@1.5.22` 的全局登记显示 66 个常规 agent；
Eve 和 PromptScript 的 global 安装不受支持，属于已知能力边界，不能通过重试或手工删除绕过。

## 默认成功路径

| 顺序 | 操作 | 通过条件 |
|---|---|---|
| 1 | 确认写入授权 | 当前用户、所有支持 global 的 agents、官方来源、8 项、copy 均获授权 |
| 2 | 检查 CLI | version 和 help 可用，参数与本手册兼容 |
| 3 | 远程 `--list` | 名称集合精确等于下方 8 项；远程 URL 仅用于发现 |
| 4 | 固定来源 | 安全临时目录中 clone，记录 full HEAD SHA，detach、校验 8 项 |
| 5 | 保存全局 JSON 快照 | 快照包含每个登记的 agents、scope、path 和 source，可恢复、可比较 |
| 6 | 分类同名项 | 每项是 `absent`、`same-source` 或 `conflict` |
| 7 | 处理并安装 | `same-source` 不触碰；安装 `absent`；`conflict` 默认按方案 A 定向替换 |
| 8 | 安装后 JSON diff | absent 正确新增、conflict 正确换源，无意外 Agent 或范围 |
| 9 | 新会话验证 | 3 个代表性 smoke，或完整 24-case corpus |
| 10 | 报告与回滚 | 区分新增与替换，分别给出定向删除和旧来源恢复步骤 |

## 安全契约与系统边界

安装代理必须遵守：

1. 写入前确认用户授权的来源、当前系统用户、目标 Agent、范围、名称集合和 copy/symlink
   方式。默认写入当前用户所有支持 global 安装的 agents；用 `--agent '*'` 交给当前 CLI
   枚举目标，不要只写 Codex。
2. 保留既有 Skills、配置、记忆、目录和未提交工作。不得通配删除、递归清理、修改 Shell
   启动文件、静默安装系统依赖或运行 `skills remove --all`。
3. 不在 Pernavo 自己的 checkout 中做项目级自安装；那会创建 `.agents/skills` 副本并与
   `skills/` 源竞争。
4. `absent` 直接安装，`same-source` 保持不变；`conflict` 默认采用方案 A，在旧来源、固定
   revision、影响 Agent 和恢复命令均已记录后定向替换。任一恢复条件不完整时停止，不得覆盖。
5. 安装 8 个入口 Skills 会提供成本感知的自动工作流政策，包括生命周期、数据、性能、测试和
审查路由规则。它不会安装或证明宿主的子 Agent 目录、模型路由、Hook、MCP、权限、
   Harness 或记忆写入器。
6. 真正的子 Agent 派生，以及 Skill 是否 `loaded`/`executed`，只能在安装后的宿主新会话中
   观察；命令成功、目录存在或模型自述均不是运行时证明。

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

再次确认 checkout 的列表精确为 8 项、校验通过，并在报告中记录完整 SHA。若用户要求指定
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
test ! -e "$PERNAVO_INSTALL_TMP/pernavo-before-agents.json"
npx --yes skills ls --global --json > "$PERNAVO_INSTALL_TMP/pernavo-before-global.json"
npx --yes skills ls --global --agent '*' --json > "$PERNAVO_INSTALL_TMP/pernavo-before-agents.json"
```

对 8 个请求名称逐项读取 `name`、`path`、`scope`、`source`、`sourceUrl` 和所有 Agent 登记，并分类：

- `absent`：全局 JSON 中无同名登记，且没有不明同名来源；可安装。
- `same-source`：已来自同一个官方仓库；本次不触碰、不重装、不隐式更新。
- `conflict`：来自其他来源，或来源无法可靠判断；进入下方方案 A 的替换安全门，不能直接覆盖。

如果旧来源显示 `tuloong/pernavo`、`tuloong/loongclaude` 或其他 fork/mirror，只有能证明它与
官方仓库是同一 repository 时才可视为 `same-source`，否则是 `conflict`。不得因为仓库名称相似、
内容相同或来源是 fork/mirror，就跳过冲突处理。

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
test ! -e "$PERNAVO_INSTALL_TMP/pernavo-after-agents.json"
npx --yes skills ls --global --json > "$PERNAVO_INSTALL_TMP/pernavo-after-global.json"
npx --yes skills ls --global --agent '*' --json > "$PERNAVO_INSTALL_TMP/pernavo-after-agents.json"
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
- 远程/本地 `--list` 不是精确 8 项；
- conflict 无法标为 `replaceable`，或 same-source/absent 无法可靠区分；
- 方案 A 缺少旧 repository、固定 revision、影响 Agent/scope、精确恢复命令或移除后 JSON 证明；
- 默认官方 checkout 校验失败；已有本地开发 checkout 仅在可信验证器缺失时可降级为 `partial`；
- 安装失败、部分成功、after diff 异常或无法计算精确新增集合；
- 继续操作需要覆盖、广泛删除、修改权限或系统依赖；
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
Before global and all-agent JSON snapshot paths:
Per-name classification: absent | same-source | conflict
Conflict disposition: replaceable | blocked
Replacement ledger: name, agent, scope, old repository, old full SHA, restore command
Directed removal command and post-removal JSON result:
Install/update command and exit status:
After global and all-agent JSON snapshot paths:
Structured before/after diff and newly created registrations:
Installed names, paths, scopes, sources, target agents, materialized SHA-256:
Agent status: registered | materialized | shared-registration | unsupported-global | blocked-source
New-session/restart status:
Representative 3-case smoke: cases, expected/forbidden/actual owners, result
Full 24-case corpus: result | not run; remaining activation unverified
Observed child-agent/tool execution:
Per-case target-observed evidence:
External environment-observed evidence, or not observed:
Harness checks, if separately requested:
Exact rollback command for only newly created name+agent registrations:
Exact rollback sequence for replaced registrations:
Unverified layers and remaining decisions:
Final evidence level: source-valid | installed | loaded | executed | target-observed | environment-observed
Final status: complete | partial | blocked
```

只有获授权的 absent 项完成安装、方案 A 的 replaceable conflict 已正确换源、after diff 已核对、
回滚步骤可执行、失败项已处理且未验证边界明确列出时，安装代理才可结束任务。
