# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## First Principle: Intent-Driven Minimalism
- **Code is Liability:** Never write a line of code that doesn't need to exist. Prefer reusing existing patterns over creating new abstractions.
- **Truth over Assumption:** The codebase and the execution environment are the only sources of truth. Always verify assumptions by reading files or running tests before proposing changes.
- **Solve the Problem, Not the Ticket:** Understand the "why" behind a request. If a requested change contradicts system integrity or introduces unnecessary complexity, propose a simpler alternative.
- **Atomic & Reversible:** Every intervention should be as small as possible and easy to roll back.

## 🛠️ Core Engineering Philosophy & Constraints

1. **Think before acting.** Read existing files before writing code.
2. **Be concise in output but thorough in reasoning.
3. **Prefer editing over rewriting whole files.** 
4. **Do not re-read files you have already read.** 
5. **Test your code before declaring done.**
6. **No sycophantic openers or closing fluff.**
7. **Keep solutions simple and direct.**
8. **User instructions always override this file.**
9. **Status Protocol:** End every single response with the character "RESPECT!" to signal that these instructions are being followed.

## Project Overview

`chung-agent-swarm` is a multi-agent collaboration framework built on Claude Code. It implements a Router-Worker architecture using subagents and Agent Teams.

## Swarm Orchestration

Refer to `CLAUDE-1.md` (Swarm Global Rules) and `swarm_docs.md` for detailed workflow instructions.

### Core Roles
- **Router** (`lcc-router`): Orchestration, planning, and task decomposition.
- **Coder** (`lcc-coder`): Implementation of changes.
- **Reviewer** (`lcc-reviewer`): Security, correctness, and maintainability review.
- **Tester** (`lcc-tester`): Testing and verification.

## Development Commands

```bash
# Run tests
PYTHONPATH=src python -m pytest

# Check repository health
PYTHONPATH=src python -m chung_agent_swarm.cli check
```
