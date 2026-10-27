import os
from pathlib import Path

explicit = os.environ.get("PERNAVO_SKILL_VALIDATOR") or os.environ.get("LOONGCLAUDE_SKILL_VALIDATOR")
path = Path(explicit) if explicit else Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
if not path.is_file():
    raise SystemExit("missing validator: %s" % path)
