#!/bin/bash
# .claude/hooks/lcc-quality-gate.sh

# Read JSON input from stdin
INPUT=$(cat)
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name')
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path')

if [[ "$EVENT" == "TaskCreated" ]]; then
  TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

  # Ensure task subject is descriptive enough
  if [[ ${#TASK_SUBJECT} -lt 10 ]]; then
     echo "Task subject is too short. Please provide a more descriptive subject (min 10 characters)." >&2
     exit 2
  fi

  # Ensure it doesn't say "TODO"
  if [[ "$TASK_SUBJECT" == *"TODO"* ]]; then
     echo "Task subject contains TODO. Please provide a concrete subject." >&2
     exit 2
  fi
fi

if [[ "$EVENT" == "TaskCompleted" ]]; then
  TASK_ID=$(echo "$INPUT" | jq -r '.task_id')
  TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

  # Double check: ensure it doesn't say "TODO" even at completion
  if [[ "$TASK_SUBJECT" == *"TODO"* ]]; then
     echo "Task subject contains TODO. Please provide a concrete subject before completing." >&2
     exit 2
  fi

  # Basic verification: Ensure there is a handoff or a report in the transcript
  if [[ -f "$TRANSCRIPT_PATH" ]]; then
    if ! grep -qiE "handoff|summary|report|LGTM|verified|completed|finished" "$TRANSCRIPT_PATH"; then
       echo "Task completion requires a summary or handoff report in the transcript." >&2
       exit 2
    fi
  fi
fi

if [[ "$EVENT" == "TeammateIdle" ]]; then
  TEAMMATE=$(echo "$INPUT" | jq -r '.teammate_name')

  # Ensure teammates don't go idle with unaddressed issues
  if [[ -f "$TRANSCRIPT_PATH" ]]; then
    if grep -qi "error" "$TRANSCRIPT_PATH" && ! grep -qiE "fixed|resolved|workaround" "$TRANSCRIPT_PATH"; then
       echo "Teammate $TEAMMATE is going idle with potential unaddressed errors in the transcript." >&2
       exit 2
    fi
  fi
fi

exit 0
