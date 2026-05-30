#!/bin/bash
# .claude/hooks/lcc-quality-gate.sh

# Read JSON input from stdin
INPUT=$(cat)
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name')
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path')

# Utility for error reporting
report_error() {
  echo "Quality Gate: $1" >&2
  exit 2
}

if [[ "$EVENT" == "TaskCreated" ]]; then
  TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

  # Reject subjects that are too short
  if [[ ${#TASK_SUBJECT} -lt 10 ]]; then
     report_error "Task subject is too short ($TASK_SUBJECT). Please provide at least 10 characters."
  fi

  # Reject subjects with TODO
  if [[ "$TASK_SUBJECT" == *"TODO"* ]]; then
     report_error "Task subject contains TODO. Please provide a concrete subject."
  fi
fi

if [[ "$EVENT" == "TaskCompleted" ]]; then
  TASK_ID=$(echo "$INPUT" | jq -r '.task_id')
  TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

  # If it's a task, ensure it doesn't say "TODO"
  if [[ "$TASK_SUBJECT" == *"TODO"* ]]; then
     report_error "Task subject contains TODO. Please provide a concrete subject before completing."
  fi

  # Basic verification: Ensure there is a handoff or a report in the transcript
  if [[ -f "$TRANSCRIPT_PATH" ]]; then
    if ! grep -qiE "handoff|summary|report|LGTM|verified" "$TRANSCRIPT_PATH"; then
       report_error "Task completion requires a summary or handoff report in the transcript."
    fi
  fi
fi

if [[ "$EVENT" == "TeammateIdle" ]]; then
  TEAMMATE=$(echo "$INPUT" | jq -r '.teammate_name')

  # Ensure teammates don't go idle with unaddressed issues
  if [[ -f "$TRANSCRIPT_PATH" ]]; then
    if grep -qi "error" "$TRANSCRIPT_PATH" && ! grep -qiE "fixed|resolved|workaround|mitigated" "$TRANSCRIPT_PATH"; then
       report_error "Teammate $TEAMMATE is going idle with potential unaddressed errors in the transcript. Please provide a resolution or workaround."
    fi
  fi
fi

exit 0
