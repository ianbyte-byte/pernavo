# Ian Codex Pets

基于 Hearts2Hearts 成员 IAN（이안）的公开资料与用户提供图片，完成三套仅人物角色的 Codex Pets。所有参考图、YAML 提示词、生成记录、QA 证据与最终 v2 图集均保存在本目录。

## 交付状态

| Pet | 风格 | 仓库图集 | SHA-256 | Codex 安装目录 |
| --- | --- | --- | --- | --- |
| `ian-azure-navigator` | 3D toy | `runs/ian-azure-navigator/final/spritesheet-extended.webp` | `cfaa4e8ca4159b51480a212be4cb231b102af90b360655c7db3c0a7f8cf3a5fb` | `~/.codex/pets/ian-azure-navigator` |
| `ian-heartline-noir` | illustrated sticker | `runs/ian-heartline-noir/final/spritesheet-extended.webp` | `a275782c3aa3e99804516f1020832be7a969d0fc6a3a252fa2d853bf73449022` | `~/.codex/pets/ian-heartline-noir` |
| `ian-lemon-cadet` | painterly anime-game | `runs/ian-lemon-cadet/final/spritesheet-extended.webp` | `24abea89638e27a60de87e2a7fcc7260e22cc8bd8cfcbd5ae1470b384f7cc149` | `~/.codex/pets/ian-lemon-cadet` |

三套均为 Codex Pet v2：`8 × 11` 图集、`1536 × 2288`、`192 × 208` 单元格、九组标准动画、十六个观察方向，`kind` 固定为 `person`。

## 资料与图片绑定

1. `ian-pets.yaml` 是三套人物提示词、人物约束、参考图绑定、最终图集和安装位置的主契约。
2. `research.md` 保存联网调研、来源链接和事实边界。
3. `references/` 原样保存七张用户图片；`references/SHA256SUMS` 用于完整性核对。
4. 每个 YAML `references` 数组引用 `reference_catalog` 中的图片键；每个键同时记录相对路径、SHA-256、允许提取的造型线索和明确禁用项。
5. `delivery-verification.json` 汇总三套仓库图集、安装图集、盲测与最终 QA 的验收结果。

参考图片仅用于人物外观、发型、服装配色和动作线索。生成物不得复制照片背景、水印、可读标识、品牌角色或动物配件。`ian_03` 中的动物耳与爪套被明确列入排除项；三套最终角色均为完整人类人物。

## 开发产物

每个 `runs/<pet-id>/` 包含：

- `pet_request.json`：hatch-pet 请求契约。
- `imagegen-jobs.json`：来源、依赖、生成结果和打包状态。
- `references/`、`prompts/`、`decoded/`：绑定后的输入、提示词和生成中间件。
- `final/spritesheet-extended.webp`：可安装的无损 WebP 图集。
- `final/pet.json`：指向仓库内扩展图集的可复用 Pet 清单。
- `final/spritesheet-extended.json`：v2 布局与 16 方位映射。
- `final/validation-extended.json`：确定性结构、透明度与色键验证。
- `qa/contact-sheet-extended.png`：九组动画与两组方向行总览。
- `qa/look-directions.png`、`qa/look-continuity.json`：方向语义和连续性检查。
- `qa/direction-blind-*`：三名互不共享答案键的方向盲测与多数票结果。
- `qa/final-visual-qa.json`：独立最终视觉门禁。

三套 `validation-extended.json`、多数票方向硬门槛和最终视觉门禁均通过。Azure 与 Lemon 的少数极斜角存在非阻塞诊断警告，但正上、正右、正下、正左四个硬门槛均通过，独立视觉复核未发现可见身份断裂、裁切或色键残边。

## 本机安装

每个 Pet 已复制到 `~/.codex/pets/<pet-id>/`，目录内包含：

- `pet.json`
- `spritesheet.webp`

安装图集与仓库最终图集的 SHA-256 完全一致。若 Codex Pets 选择器已打开，可刷新或重启 Codex 让新条目重新载入。

## 事实边界

公开来源支持 IAN 的艺名、韩文名、组合、所属公司、生日、出道日期与出道作品。所查一手艺人资料未确认“정이안 / 郑以安”为法定姓名，也未确认官方成员色、官方 emoji、MBTI 或固定官方队内位置；这些字段不会被写成确定事实。三套配色均来自用户提供的照片，而不是官方成员色。
