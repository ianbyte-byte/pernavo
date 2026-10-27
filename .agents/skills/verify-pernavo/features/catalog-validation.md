# Catalog validation

## Sub-features

- Frontmatter and skill-directory validation for each skills/*/SKILL.md
- Relative links inside skills/**/*.md
- README entries for all 11 catalog skills
- Trigger corpus: one positive, one negative, and one collision case per skill
- Local Skills CLI lists every catalog skill

## How to get to it (user POV)

From the repository root, run the validator. There is no UI.

## Driving it with the shell

```bash
cd /Users/chung/Developer/Code/loongclaude
./scripts/validate-skills.sh
```

Capture stdout and the exit code in `${TMPDIR:-/tmp}/pernavo-verify/catalog-validation.txt`.

## Gotchas

- Exit 0 without the PASS line for 11 skills and 33 cases is a failure.
- npx needs network access to list skills. A failure there is a failed drive, not a reason to skip the CLI check.
- Do not create .agents/skills/<catalog-name>/SKILL.md. The validator rejects a checkout copy that competes with skills/<name>/.
- A negative check points PERNAVO_SKILL_VALIDATOR at a missing file. It must fail. Do not leave that variable set.
