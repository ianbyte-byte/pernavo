# Swarm Global Rules (V2.2)

## First Principle: Intent-Driven Minimalism
- **Code is Liability:** Never write a line of code that doesn't need to exist. Prefer reusing existing patterns over creating new abstractions.
- **Truth over Assumption:** The codebase and the execution environment are the only sources of truth. Always verify assumptions by reading files or running tests before proposing changes.
- **Solve the Problem, Not the Ticket:** Understand the "why" behind a request. If a requested change contradicts system integrity or introduces unnecessary complexity, propose a simpler alternative.
- **Atomic & Reversible:** Every intervention should be as small as possible and easy to roll back.

## 1) Goals

- Organize multi-agent collaboration using a Router–Worker architecture with **Agent Teams**.
- Ensure continuity via a traceable handoff protocol and direct inter-agent messaging.

## 2) Role boundaries (mandatory)

- Router: Lead orchestrator. Planning, decomposition, and synthesis only. No code edits.
- Coder: Implementation. Must request review and notify teammates when ready.
- Reviewer: Audit. Focuses on security/correctness/maintainability. Supports parallel domains.
- Tester: Verification. Runs tests and shares logs/repro steps.

## 3) Agent Teams (V2.2)

Agent teams allow parallel execution and decentralized coordination.

- **Team lead**: Main agent session. Responsible for spawning, monitoring, plan approval, and final synthesis.
- **Teammates**: Independent agents with their own context windows.
- **Mailbox (Coordination)**:
  - `message <teammate>`: Direct peer-to-peer communication (e.g., Coder to Reviewer).
  - `broadcast <message>`: Send to all teammates for critical status updates.
- **Shared Task List**: decentralized task tracking. Aim for 5-6 tasks per teammate.
- **Plan Approval**: Mandatory for complex/risky implementation. Lead reviews teammate plans autonomously.
- **Wait Directive**: If the lead starts working instead of delegating, use: "Wait for your teammates to complete their tasks before proceeding".
- **Cleanup**: Shutdown all teammates first, then run `Clean up the team`.

## 4) Orchestration Patterns

- **Scientific Debate**: 5+ teammates investigate competing hypotheses and disprove each other's theories.
- **Parallel Review**: Specialized reviewers for Security, Performance, and Test Coverage.
- **Cross-layer Coordination**: Separate teammates for frontend, backend, and testing.

## 5) Hooks and Quality Gates

Automated checks are enforced via `.claude/hooks/lcc-quality-gate.sh`.

- **TaskCreated**: Rejects subjects < 10 characters or containing "TODO".
- **TaskCompleted**: Verifies summary/handoff exists in transcript. Rejects "TODO".
- **TeammateIdle**: Ensures no unaddressed errors are left in the transcript.

## 6) Handoff Protocol (Legacy/Fallback)

Each single-agent handoff must include a JSON object:

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester",
  "summary": "Progress summary (done/todo/risks)",
  "next_instructions": "Actionable task list"
}
```

## 7) Document-first workflow (mandatory)

Before code changes for platform/API/config tasks:
- Router ensures specs are reviewed.
- Coder updates `.claude/session_config.json` with JSON schema and context optimization notes.
- Primary menu: `.claude/docs/claud_platform_menu.md`.
