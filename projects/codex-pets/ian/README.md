# Ian Codex Pets

基于 Hearts2Hearts 成员 IAN（이안）的公开资料与用户提供媒体，开发三套仅人物角色的 Codex Pets。当前主契约已切换为真人写实重制：视频帧负责锁定脸部与可见上半身几何，舞台照片负责服装、发型色彩和可见全身轮廓。所有参考图、原始视频副本、选帧、YAML 提示词、生成记录、QA 证据与最终 v2 图集均保存在本目录。

旧版卡通设计保存在 `archive/ian-pets-cartoon-v1.yaml` 和原有 `runs/<pet-id>/` 中。真人重制使用独立的 `runs/<pet-id>-photoreal-v2/`；三套均在结构校验、方向盲测与三路最终视觉 QA 通过后才覆盖本机安装版本。

## 交付状态

| Pet | 风格 | 仓库图集 | SHA-256 | Codex 安装目录 |
| --- | --- | --- | --- | --- |
| `ian-azure-navigator` | 真人写实 · 蓝色航海 | `runs/ian-azure-navigator-photoreal-v2/final/spritesheet-extended.webp` | `6e801634eacbcc234bb5d5ee0ae12862939030d4693d8fe6269a68e5b4f43f92` | `~/.codex/pets/ian-azure-navigator` |
| `ian-heartline-noir` | 真人写实 · 黑白心线 | `runs/ian-heartline-noir-photoreal-v2/final/spritesheet-extended.webp` | `683e9053856eb58e3496c5e3183aa70d57f0121ba9b9eed885b1ec4405579f30` | `~/.codex/pets/ian-heartline-noir` |
| `ian-lemon-cadet` | 真人写实 · 柠檬双马尾 | `runs/ian-lemon-cadet-photoreal-v2/final/spritesheet-extended.webp` | `a9abfa5e7a5eb426dde85adb15928ce3235de00c03e70ca3081122336db4dcb2` | `~/.codex/pets/ian-lemon-cadet` |

三套均为 Codex Pet v2：`8 × 11` 图集、`1536 × 2288`、`192 × 208` 单元格、九组标准动画、十六个观察方向，`kind` 固定为 `person`。

## 资料与图片绑定

1. `ian-pets.yaml` 是三套真人人物提示词、身份约束、参考媒体绑定、最终图集和安装位置的主契约。
2. `research.md` 保存联网调研、来源链接和事实边界。
3. `references/` 原样保存七张用户图片，并保存两段用户视频的仓库副本；`references/SHA256SUMS` 用于完整性核对。
4. `references/video-reference-manifest.yaml` 记录视频哈希、媒体参数、选帧时间戳、证据用途和证据边界。
5. YAML 中每套 Pet 分别用 `identity_references`、`outfit_references` 与最多五项的 `generation_references` 绑定真人身份和服装输入。
6. `delivery-verification.json` 汇总三套仓库图集、安装图集、盲测与最终 QA 的验收结果。

视频中的暖色白平衡与美颜平滑不被当作真实皮肤纹理；两段视频也没有严格侧面或站立全身证据。参考图片仅用于人物外观、发型、服装配色、可见身材轮廓和动作线索。生成物不得复制照片背景、水印、可读标识、品牌角色或动物配件。`ian_03` 中的动物耳与爪套被明确列入排除项；三套最终角色均为完整真人比例的人类人物，不使用卡通、动漫、Q 版、玩具、贴纸或纯抽象风格。

## 开发产物

每个 `runs/<pet-id>-photoreal-v2/` 包含：

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

三套 `validation-extended.json` 均为 `ok: true`、错误 0、警告 0、透明 RGB 残留 0；多数票方向硬门槛和最终视觉门禁也全部通过。少数极斜角存在非阻塞的缩略图判读分歧，但正上、正右、正下、正左四个硬门槛均通过，带标签的 16 方位环保持连续。

Lemon Cadet 的第一次最终门禁曾在 `running-right` 的 `r1c1`、`r1c2`、`r1c6` 发现脱离人体的碎片，因此该版本被归档且从未安装。随后完整重生整行，而不是逐格修补；修订版 8 帧均只有一个主要人物连通组件，三名终检者全部给出 PASS。失败证据保存在 `runs/ian-lemon-cadet-photoreal-v2/qa/final-visual-round-1-failed/`。

## 本机安装

每个 Pet 已复制到 `~/.codex/pets/<pet-id>/`，目录内包含：

- `pet.json`
- `spritesheet.webp`

安装图集与仓库最终图集的 SHA-256 完全一致，并已在安装目录重新通过 v2 atlas 严格校验。若 Codex Pets 选择器已打开，可刷新或重启 Codex 让真人版本重新载入。

## 事实边界

公开来源支持 IAN 的艺名、韩文名、组合、所属公司、生日、出道日期与出道作品。所查一手艺人资料未确认“정이안 / 郑以安”为法定姓名，也未确认官方成员色、官方 emoji、MBTI 或固定官方队内位置；这些字段不会被写成确定事实。三套配色均来自用户提供的照片，而不是官方成员色。
