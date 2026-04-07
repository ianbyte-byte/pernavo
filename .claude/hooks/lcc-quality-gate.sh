#!/bin/bash
# .claude/hooks/lcc-quality-gate.sh

# Read JSON input from stdin
INPUT=$(cat)
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name')
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path')

if [[ "$EVENT" == "TaskCreated" ]]; then
  TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

  # 1. Reject subjects < 10 characters
  if [ ${#TASK_SUBJECT} -lt 10 ]; then
     echo "Task subject too short. Must be at least 10 characters." >&2
     exit 2
  fi

  # 2. Reject TODO in subject
  if [[ "$TASK_SUBJECT" == *"TODO"* ]]; then
     echo "Task subject contains TODO. Please provide a concrete subject." >&2
     exit 2
  fi
fi

if [[ "$EVENT" == "TaskCompleted" ]]; then
  TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

  # Ensure it doesn't say "TODO"
  if [[ "$TASK_SUBJECT" == *"TODO"* ]]; then
     echo "Task subject contains TODO. Please provide a concrete subject before completing." >&2
     exit 2
  fi

  # Ensure there is a handoff or a report in the transcript
  if [[ -f "$TRANSCRIPT_PATH" ]]; then
    if ! grep -qiE "handoff|summary|report|LGTM|verified|completed|finished" "$TRANSCRIPT_PATH"; then
       echo "Task completion requires a summary or handoff report in the transcript (keywords: LGTM, verified, completed, finished)." >&2
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
