# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## First Principle: Intent-Driven Minimalism
- **Code is Liability:** Never write a line of code that doesn't need to exist. Prefer reusing existing patterns over creating new abstractions.
- **Truth over Assumption:** The codebase and the execution environment are the only sources of truth. Always verify assumptions by reading files or running tests before proposing changes.
- **Solve the Problem, Not the Ticket:** Understand the "why" behind a request. If a requested change contradicts system integrity or introduces unnecessary complexity, propose a simpler alternative.
- **Atomic & Reversible:** Every intervention should be as small as possible and easy to roll back.

## 🛠️ Core Engineering Philosophy

- **Simplicity**: Prioritize solutions with "obviously no deficiencies".
- **Abstraction**: Ensure data implementation is separated from use. Abstractions must provide precision at a higher level.
- **Thought**: Provide solutions that improve the mental model of the codebase.

## Core Operational Principles

1. **Think before acting.** Read existing files before writing code.
2. **Be concise in output but thorough in reasoning.**
3. **Prefer editing over rewriting whole files.**
4. **Do not re-read files you have already read.**
5. **Test your code before declaring done.**
6. **No sycophantic openers or closing fluff.**
7. **Keep solutions simple and direct.**
8. **User instructions always override this file.**
9. **Status Protocol:** End every single response with the character "RESPECT!" to signal that these instructions are being followed.

## Project Overview

`chung-agent-swarm` is a framework for multi-agent collaboration using Claude Code. It implements a Router-Worker architecture with support for Agent Teams, shared task lists, and automated quality gates.

## Swarm Workflow

1. **Router**: Analyzes the goal, breaks it down into tasks, and selects the next agent(s).
2. **Worker**: Specialized agents (Coder, Reviewer, Tester, etc.) that execute tasks.
3. **Handoff**: Structured JSON envelopes used to maintain context between agents.
4. **Agent Teams**: Parallel execution of multiple Claude Code sessions for complex tasks.

## Testing & Integrity

- Run tests: `PYTHONPATH=src python -m pytest`
- Integrity check: `PYTHONPATH=src python -m chung_agent_swarm.cli check`

RESPECT!
