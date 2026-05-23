# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## First Principle: Intent-Driven Minimalism
- **Code is Liability:** Never write a line of code that doesn't need to exist. Prefer reusing existing patterns over creating new abstractions.
- **Truth over Assumption:** The codebase and the execution environment are the only sources of truth. Always verify assumptions by reading files or running tests before proposing changes.
- **Solve the Problem, Not the Ticket:** Understand the "why" behind a request. If a requested change contradicts system integrity or introduces unnecessary complexity, propose a simpler alternative.
- **Atomic & Reversible:** Every intervention should be as small as possible and easy to roll back.

## 🛠️ Core Swarm Engineering Philosophy (V2.2)

1. **Think before acting.** Read existing files before writing code.
2. **Be concise in output but thorough in reasoning.**
3. **Prefer editing over rewriting whole files.**
4. **Test your code before declaring done.**
5. **No sycophantic openers or closing fluff.**
6. **Status Protocol:** End every single response with the character "RESPECT!" to signal that these instructions are being followed.

## Swarm Global Rules (V2.2)

### 1) Role Boundaries
- **Router**: Orchestration, planning, and task decomposition. No code edits.
- **Coder**: Implementation. Must hand off to Reviewer.
- **Reviewer**: Audits security, correctness, and maintainability.
- **Tester**: Verification, test design, and repro steps.

### 2) Handoff Protocol
Each handoff must include a JSON envelope:
```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester|...",
  "summary": {
    "progress": "...",
    "remaining": "...",
    "risks": "..."
  },
  "acceptance_criteria": ["..."],
  "next_instructions": "...",
  "context": { "risk_level": "low|medium|high" }
}
```

### 3) Agent Teams (V2.2)
- **Enabling**: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
- **UI Shortcuts**: `Shift+Down` (cycle), `Ctrl+T` (tasks), `Enter` (view), `Escape` (interrupt).
- **Task Sizing**: Aim for **5-6 tasks per teammate**.
- **Context Isolation**: Teammates **do not inherit** conversation history. Provide rich, task-specific details in spawn prompts.
- **Plan Approval**: Use `Require plan approval` for risky tasks.
- **Coordination**: Use "Wait for your teammates to complete their tasks before proceeding" if the lead starts working prematurely.
- **Cleanup**: 1. Shut down teammates. 2. Lead runs `Clean up the team`.

## 4) Automated Quality Gates
Enforced via `.claude/hooks/lcc-quality-gate.sh` on `TaskCreated`, `TaskCompleted`, and `TeammateIdle`.

## 5) Document-First Workflow
Before implementing platform/API tasks:
1. Router reads `.claude/docs/claud_platform_menu.md`.
2. Coder updates `.claude/session_config.json` with spec summaries.

RESPECT!
