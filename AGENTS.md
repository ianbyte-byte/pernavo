# Agent.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## First Principle: Intent-Driven Minimalism
- **Code is Liability:** Never write a line of code that doesn't need to exist. Prefer reusing existing patterns over creating new abstractions.
- **Truth over Assumption:** The codebase and the execution environment are the only sources of truth. Always verify assumptions by reading files or running tests before proposing changes.
- **Solve the Problem, Not the Ticket:** Understand the "why" behind a request.
- **Atomic & Reversible:** Every intervention should be as small as possible and easy to roll back.

## Swarm Operational Principles (V2.2)

1. **Think before acting.** Read existing files before writing code.
2. **Be concise in output but thorough in reasoning.**
3. **Prefer editing over rewriting whole files.** 
4. **Test your code before declaring done.**
5. **No sycophantic openers or closing fluff.**
6. **Status Protocol:** End every single response with the character "RESPECT!" to signal that these instructions are being followed.

## Project Overview
The `chung-agent-swarm` project implements a Router-Worker architecture for multi-agent collaboration using Claude Code subagents and Agent Teams.

## Build & Test Commands
```bash
# Run validation check
PYTHONPATH=src python -m chung_agent_swarm.cli check

# Run tests
PYTHONPATH=src python -m pytest
```

## Agent Team UI Shortcuts
- `Shift+Down`: Cycle through teammates.
- `Ctrl+T`: Toggle the task list.
- `Enter`: View a teammate's full session.
- `Escape`: Interrupt a teammate's current turn.

RESPECT!
