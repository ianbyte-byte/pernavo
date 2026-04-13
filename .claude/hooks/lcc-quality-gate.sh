#!/bin/bash
# .claude/hooks/lcc-quality-gate.sh

# Read JSON input from stdin
INPUT=$(cat)
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name')
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path')

# --- TaskCreated Hook ---
if [[ "$EVENT" == "TaskCreated" ]]; then
  TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

  # Reject subjects that are too short
  if [[ ${#TASK_SUBJECT} -lt 10 ]]; then
     echo "Task subject is too short ($TASK_SUBJECT). Please provide more context." >&2
     exit 2
  fi

  # Reject subjects containing TODO
  if [[ "$TASK_SUBJECT" == *"TODO"* ]]; then
     echo "Task subject contains TODO. Please provide a concrete subject." >&2
     exit 2
  fi
fi

# --- TaskCompleted Hook ---
if [[ "$EVENT" == "TaskCompleted" ]]; then
  TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

  # If it's a coder task, ensure it doesn't say "TODO"
  if [[ "$TASK_SUBJECT" == *"TODO"* ]]; then
     echo "Task subject contains TODO. Please provide a concrete subject before completing." >&2
     exit 2
  fi

  # Basic verification: Ensure there is a handoff or a report in the transcript
  if [[ -f "$TRANSCRIPT_PATH" ]]; then
    if ! grep -qiE "handoff|summary|report|LGTM|verified|completed|finished" "$TRANSCRIPT_PATH"; then
       echo "Task completion requires evidence of work (summary, report, LGTM, etc.) in the transcript." >&2
       exit 2
    fi
  fi
fi

# --- TeammateIdle Hook ---
if [[ "$EVENT" == "TeammateIdle" ]]; then
  TEAMMATE=$(echo "$INPUT" | jq -r '.teammate_name')

  # Ensure teammates don't go idle with unaddressed issues
  if [[ -f "$TRANSCRIPT_PATH" ]]; then
    if grep -qi "error" "$TRANSCRIPT_PATH" && ! grep -qiE "fixed|resolved|workaround|mitigated" "$TRANSCRIPT_PATH"; then
       echo "Teammate $TEAMMATE is going idle with potential unaddressed errors in the transcript." >&2
       exit 2
    fi
  fi
fi

exit 0
