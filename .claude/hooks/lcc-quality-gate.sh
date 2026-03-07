#!/bin/bash
# .claude/hooks/lcc-quality-gate.sh

# Read JSON input from stdin
INPUT=$(cat)
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name')

if [[ "$EVENT" == "TaskCompleted" ]]; then
  TASK_ID=$(echo "$INPUT" | jq -r '.task_id')
  TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')
  TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path')

  # If it's a coder task, ensure it doesn't say "TODO"
  if [[ "$TASK_SUBJECT" == *"TODO"* ]]; then
     echo "Task subject contains TODO. Please provide a concrete subject before completing." >&2
     exit 2
  fi

  # Basic verification by inspecting the transcript
  if [[ -f "$TRANSCRIPT_PATH" ]]; then
    # Ensure there is some evidence of tool usage or results
    if ! grep -qE "tool_use|result" "$TRANSCRIPT_PATH"; then
       echo "Task completed without any tool usage recorded in transcript. Please ensure work was actually performed." >&2
       exit 2
    fi
  fi
fi

if [[ "$EVENT" == "TeammateIdle" ]]; then
  TEAMMATE=$(echo "$INPUT" | jq -r '.teammate_name')

  # Enforce that teammates don't go idle without a final report
  # This is just a placeholder logic
  # echo "Teammate $TEAMMATE is going idle. Ensuring quality..." >&2
fi

exit 0
