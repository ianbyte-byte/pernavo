#!/bin/bash
# .claude/hooks/lcc-quality-gate.sh

# Read JSON input from stdin
INPUT=$(cat)
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name')
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path')

if [[ "$EVENT" == "TaskCreated" ]]; then
  TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

  # Reject subjects that are too short
  if [[ ${#TASK_SUBJECT} -lt 10 ]]; then
     echo "Quality Gate: Task subject is too short ($TASK_SUBJECT). Please provide at least 10 characters." >&2
     exit 2
  fi

  # Reject subjects with TODO
  if [[ "$TASK_SUBJECT" == *"TODO"* ]]; then
     echo "Quality Gate: Task subject contains TODO. Please provide a concrete subject." >&2
     exit 2
  fi
fi

if [[ "$EVENT" == "TaskCompleted" ]]; then
  TASK_ID=$(echo "$INPUT" | jq -r '.task_id')
  TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

  # If it's a task, ensure it doesn't say "TODO" in the subject
  if [[ "$TASK_SUBJECT" == *"TODO"* ]]; then
     echo "Quality Gate: Task subject contains TODO ($TASK_SUBJECT). Please provide a concrete subject before completing." >&2
     exit 2
  fi

  # Basic verification: Ensure there is a handoff or a report in the transcript
  if [[ -n "$TRANSCRIPT_PATH" && -f "$TRANSCRIPT_PATH" ]]; then
    if ! grep -qiE "handoff|summary|report|LGTM|verification|verified" "$TRANSCRIPT_PATH"; then
       echo "Quality Gate: Task completion requires a summary, handoff report, or LGTM in the transcript." >&2
       exit 2
    fi
  fi
fi

if [[ "$EVENT" == "TeammateIdle" ]]; then
  TEAMMATE=$(echo "$INPUT" | jq -r '.teammate_name')

  # Ensure teammates don't go idle with unaddressed issues
  if [[ -n "$TRANSCRIPT_PATH" && -f "$TRANSCRIPT_PATH" ]]; then
    if grep -qi "error" "$TRANSCRIPT_PATH" && ! grep -qiE "fixed|resolved|workaround|mitigated" "$TRANSCRIPT_PATH"; then
       echo "Quality Gate: Teammate $TEAMMATE is going idle with potential unaddressed errors in the transcript." >&2
       exit 2
    fi
  fi
fi

exit 0
