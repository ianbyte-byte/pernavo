---
name: lcc-workflow-index
description: Index of available project subagents and skills for common engineering workflows.
disable-model-invocation: true
---

List the available project subagents and skills in this repository, and recommend which to use for a given task.

## Subagents (project-level)
- lcc-router: routes and decomposes tasks (read-only)
- lcc-coder: implements code changes (edits allowed)
- lcc-reviewer: reviews changes (no edits)
- lcc-tester: runs/tests verification (no edits)
- lcc-product: clarifies requirements and acceptance criteria (read-only)
- lcc-architect: proposes designs and migration plans (read-only)
- lcc-debugger: reproduces and fixes failures (edits allowed)
- lcc-refactorer: behavior-preserving refactors (edits allowed)
- lcc-simplifier: DRY/KISS code simplifications without behavior change (edits allowed)
- lcc-security-reviewer: security-focused review (no edits)
- lcc-performance-optimizer: measure-driven performance work (edits allowed)
- lcc-sql-optimizer: SQL optimization based on MySQL index principles (edits allowed)
- lcc-docs-writer: updates docs to match behavior (edits allowed)
- lcc-release-manager: release notes and checklist (read-only)
- lcc-incident-triage: incident triage and mitigations (may run commands)
- lcc-dependency-upgrader: safe dependency upgrades (edits allowed)
- lcc-git-worktree-manager: parallel git workflows using worktrees (may run commands)

## Skills (slash commands)
- /swarm: generic Router → Coder → Reviewer → Tester loop
- /feature: product → architect → swarm loop
- /bugfix: triage → debugger → review → verify
- /tdd: red → green → refactor
- /review: structured review (optional security pass)
- /security: security review + remediation
- /perf: measure → optimize → re-measure
- /sql-optimize: SQL optimization based on MySQL index principles (美团技术团队)
- /docs: update documentation
- /release: release notes + checklist
- /triage: incident triage playbook
- /debug: repro → fix → verify
- /refactor: behavior-preserving refactors
- /simplify: eliminate redundancy and simplify control flow (behavior-preserving)
- /deps: safe dependency upgrades
- /design: requirements → architecture → execution plan

## Usage
Pick a skill that matches your intent, or explicitly ask Claude Code to use a specific subagent (e.g., “Use lcc-debugger to fix failing tests”). If you are unsure, start with lcc-router.
