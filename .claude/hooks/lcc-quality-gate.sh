#!/bin/bash
# .claude/hooks/lcc-quality-gate.sh

# Read JSON input from stdin
INPUT=$(cat)
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name')

if [[ "$EVENT" == "TaskCompleted" ]]; then
  TASK_ID=$(echo "$INPUT" | jq -r '.task_id')
  TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

  # For lcc-coder, we might want to check if tests were run or if a handoff exists
  # Since we don't have easy access to the full transcript in this simple bash script
  # (though transcript_path is provided), we'll do a basic validation.

  # Example: Check if the last assistant message (if available in some events)
  # or just enforce a rule that they must mention "handoff" in their summary if it's a team task.

  # For now, let's just log and allow, or implement a dummy check for demonstration.
  # A real implementation might use 'grep' on the 'transcript_path'.

  # If it's a coder task, ensure it doesn't say "TODO"
  if [[ "$TASK_SUBJECT" == *"TODO"* ]]; then
     echo "Task subject contains TODO. Please provide a concrete subject before completing." >&2
     exit 2
  fi
fi

if [[ "$EVENT" == "TeammateIdle" ]]; then
  TEAMMATE=$(echo "$INPUT" | jq -r '.teammate_name')

  # Enforce that teammates don't go idle without a final report
  # This is just a placeholder logic
  # echo "Teammate $TEAMMATE is going idle. Ensuring quality..." >&2
fi

exit 0
