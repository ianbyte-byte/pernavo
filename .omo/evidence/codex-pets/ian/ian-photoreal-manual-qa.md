# Ian photoreal Codex Pets — manual QA

Read-only final visual QA of the three new photoreal runs. Images were opened at original resolution with `view_image`; JSON artifacts were parsed read-only. The two independent visual-QA oracle passes both returned `REVISE` for all three pets.

## manualQa

### surfaceEvidence

| scenario id | criterion reference | surface | exact invocation | verdict | artifactRefs |
|---|---|---|---|---|---|
| azure-contact | C1 identity/style/transparency | Azure Navigator contact sheet | `view_image(path=".../ian-azure-navigator-photoreal/qa/contact-sheet-extended.png", detail="original")` | REVISE | azure-contact, azure-canonical, shared-face-01, shared-face-02 |
| azure-look | C2 exact directions/look continuity | Azure Navigator look sheet | `view_image(path=".../ian-azure-navigator-photoreal/qa/look-directions.png", detail="original")` | REVISE | azure-look, azure-blind, azure-continuity, azure-direction |
| azure-struct | C3 atlas/alpha/despill | Azure final/validation artifacts | `python3 -c 'json.load(open(".../final/validation-extended.json")); json.load(open(".../qa/chroma-despill-extended.json"))'` | PASS | azure-validation, azure-despill |
| heartline-contact | C1 identity/style/transparency | Heartline Noir contact sheet | `view_image(path=".../ian-heartline-noir-photoreal/qa/contact-sheet-extended.png", detail="original")` | REVISE | heartline-contact, heartline-canonical, shared-face-01, shared-face-02 |
| heartline-look | C2 exact directions/look continuity | Heartline Noir look sheet | `view_image(path=".../ian-heartline-noir-photoreal/qa/look-directions.png", detail="original")` | REVISE | heartline-look, heartline-blind, heartline-continuity, heartline-direction |
| heartline-struct | C3 atlas/alpha/despill | Heartline final/validation artifacts | `python3 -c 'json.load(open(".../final/validation-extended.json")); json.load(open(".../qa/chroma-despill-extended.json"))'` | PASS | heartline-validation, heartline-despill |
| lemon-contact | C1 identity/style/transparency | Lemon Cadet contact sheet | `view_image(path=".../ian-lemon-cadet-photoreal/qa/contact-sheet-extended.png", detail="original")` | REVISE | lemon-contact, lemon-canonical, shared-face-01, shared-face-02 |
| lemon-look | C2 exact directions/look continuity | Lemon Cadet look sheet | `view_image(path=".../ian-lemon-cadet-photoreal/qa/look-directions.png", detail="original")` | REVISE | lemon-look, lemon-blind, lemon-continuity, lemon-direction |
| lemon-struct | C3 atlas/alpha/despill | Lemon final/validation artifacts | `python3 -c 'json.load(open(".../final/validation-extended.json")); json.load(open(".../qa/chroma-despill-extended.json"))'` | PASS | lemon-validation, lemon-despill |

### adversarialCases

| scenario id | criterion reference | adversarial class | expected behavior | verdict | artifactRefs |
|---|---|---|---|---|---|
| azure-identity | C1 | identity drift | Same recognizable Ian face as both shared video anchors within 192x208 limits | FAIL | azure-contact, azure-look, azure-canonical, shared-face-01, shared-face-02 |
| azure-style | C1 | style substitution | Fully clothed real human; no cartoon/anime/toy/animal anatomy/text/logo | PASS | azure-contact, azure-validation |
| azure-rows | C2 | row/state coverage | 11 rows with expected used-cell counts and readable action semantics | PASS-with-warning | azure-contact, azure-validation |
| azure-directions | C2 | direction reversal/ambiguity | Exactly 16 clockwise look directions | REVISE | azure-look, azure-blind, azure-direction |
| azure-alpha | C3 | chroma/fringe/foreground damage | Final despill preserves alpha and leaves no visible fringe or holes | PASS | azure-contact, azure-validation, azure-despill |
| heartline-identity | C1 | identity drift | Same recognizable Ian face as both shared video anchors within 192x208 limits | FAIL | heartline-contact, heartline-look, heartline-canonical, shared-face-01, shared-face-02 |
| heartline-style | C1 | style substitution | Fully clothed real human; no cartoon/anime/toy/animal anatomy/text/logo | PASS | heartline-contact, heartline-validation |
| heartline-rows | C2 | row/state coverage | 11 rows with expected used-cell counts and readable action semantics | PASS-with-warning | heartline-contact, heartline-validation |
| heartline-directions | C2 | direction reversal/ambiguity | Exactly 16 clockwise look directions | REVISE | heartline-look, heartline-blind, heartline-direction |
| heartline-alpha | C3 | chroma/fringe/foreground damage | Final despill preserves alpha and leaves no visible fringe or holes | PASS | heartline-contact, heartline-validation, heartline-despill |
| lemon-identity | C1 | identity drift | Same recognizable Ian face as both shared video anchors within 192x208 limits | FAIL | lemon-contact, lemon-look, lemon-canonical, shared-face-01, shared-face-02 |
| lemon-style | C1 | style substitution | Fully clothed real human; no cartoon/anime/toy/animal anatomy/text/logo | PASS | lemon-contact, lemon-validation |
| lemon-rows | C2 | row/state coverage | 11 rows with expected used-cell counts and readable action semantics | PASS-with-warning | lemon-contact, lemon-validation |
| lemon-directions | C2 | direction reversal/ambiguity | Exactly 16 clockwise look directions | FAIL | lemon-look, lemon-blind, lemon-direction |
| lemon-alpha | C3 | chroma/fringe/foreground damage | Final despill preserves alpha and leaves no visible fringe or holes | PASS | lemon-contact, lemon-validation, lemon-despill |

### artifactRefs

| id | kind | description | path |
|---|---|---|---|
| azure-contact | screenshot | Azure final checkerboard 11-row contact sheet | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-azure-navigator-photoreal/qa/contact-sheet-extended.png` |
| azure-look | screenshot | Azure final 16-direction/look sheet | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-azure-navigator-photoreal/qa/look-directions.png` |
| azure-canonical | reference | Azure canonical base | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-azure-navigator-photoreal/references/canonical-base.png` |
| azure-validation | json | Azure final RGBA/atlas validation | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-azure-navigator-photoreal/final/validation-extended.json` |
| azure-despill | json | Azure final chroma despill report | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-azure-navigator-photoreal/qa/chroma-despill-extended.json` |
| azure-blind | json | Azure pre-despill blind direction validation | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-azure-navigator-photoreal/qa/direction-blind-validation.pre-despill.json` |
| azure-continuity | json | Azure look continuity report | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-azure-navigator-photoreal/qa/look-continuity.json` |
| azure-direction | json | Azure direct visual direction QA | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-azure-navigator-photoreal/qa/direction-visual-qa.json` |
| heartline-contact | screenshot | Heartline final checkerboard 11-row contact sheet | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-heartline-noir-photoreal/qa/contact-sheet-extended.png` |
| heartline-look | screenshot | Heartline final 16-direction/look sheet | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-heartline-noir-photoreal/qa/look-directions.png` |
| heartline-canonical | reference | Heartline canonical base | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-heartline-noir-photoreal/references/canonical-base.png` |
| heartline-validation | json | Heartline final RGBA/atlas validation | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-heartline-noir-photoreal/final/validation-extended.json` |
| heartline-despill | json | Heartline final chroma despill report | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-heartline-noir-photoreal/qa/chroma-despill-extended.json` |
| heartline-blind | json | Heartline pre-despill blind direction validation | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-heartline-noir-photoreal/qa/direction-blind-validation.pre-despill.json` |
| heartline-continuity | json | Heartline look continuity report | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-heartline-noir-photoreal/qa/look-continuity.json` |
| heartline-direction | json | Heartline direct visual direction QA | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-heartline-noir-photoreal/qa/direction-visual-qa.json` |
| lemon-contact | screenshot | Lemon final checkerboard 11-row contact sheet | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-lemon-cadet-photoreal/qa/contact-sheet-extended.png` |
| lemon-look | screenshot | Lemon final 16-direction/look sheet | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-lemon-cadet-photoreal/qa/look-directions.png` |
| lemon-canonical | reference | Lemon canonical base | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-lemon-cadet-photoreal/references/canonical-base.png` |
| lemon-validation | json | Lemon final RGBA/atlas validation | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-lemon-cadet-photoreal/final/validation-extended.json` |
| lemon-despill | json | Lemon final chroma despill report | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-lemon-cadet-photoreal/qa/chroma-despill-extended.json` |
| lemon-blind | json | Lemon pre-despill blind direction validation | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-lemon-cadet-photoreal/qa/direction-blind-validation.pre-despill.json` |
| lemon-continuity | json | Lemon look continuity report | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-lemon-cadet-photoreal/qa/look-continuity.json` |
| lemon-direction | json | Lemon direct visual direction QA | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/runs/ian-lemon-cadet-photoreal/qa/direction-visual-qa.json` |
| shared-face-01 | reference | Shared Ian primary face anchor | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/references/video-frames/ian-video-02-t01.25.jpg` |
| shared-face-02 | reference | Shared Ian supporting face anchor | `/Users/chung/Developer/Code/loongclaude/projects/codex-pets/ian/references/video-frames/ian-video-01-t00.80.jpg` |

## Overall verdict

All three pets are `REVISE`. The atlas/row/occupancy/transparency engineering is largely clean, but the identity requirement is not met: each sprite set preserves its own auburn-haired synthetic face rather than a recognizably consistent Ian face from the shared video anchors. Lemon additionally has a direct blind-direction conflict at 157.5/202.5 and vertical ambiguities; Azure and Heartline retain vertical ambiguities. Jumping/failed rows are visually usable but weak and are recorded as warnings.
