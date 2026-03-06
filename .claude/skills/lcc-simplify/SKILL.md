---
name: lcc-simplify
description: Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. Focuses on recently modified code unless instructed otherwise.
disable-model-invocation: true
---

Run a behavior-preserving code simplification workflow.

## Steps

### 1) Identify Scope (Router or User)
- Determine which code sections to simplify (recently modified by default)
- Define what must remain equivalent (behavior, interfaces, invariants)

### 2) Simplify (lcc-simplifier)
- Delegate to `lcc-simplifier`
- The agent will apply refinements following these principles:

#### Preserve Functionality
- Never change what the code does - only how it does it
- All original features, outputs, and behaviors must remain intact

#### Apply Project Standards
- Follow CLAUDE.md coding standards
- Use ES modules with proper import sorting
- Prefer function keyword over arrow functions
- Use explicit return type annotations
- Follow proper error handling patterns

#### Enhance Clarity
- Reduce unnecessary complexity and nesting
- Eliminate redundant code and abstractions
- Improve variable and function names
- Consolidate related logic
- Remove unnecessary comments
- **Avoid nested ternary operators** - prefer switch/if-else chains
- Choose clarity over brevity

#### Maintain Balance
- Avoid over-simplification that reduces clarity
- Don't create overly clever solutions
- Don't combine too many concerns
- Don't remove helpful abstractions
- Don't prioritize "fewer lines" over readability

### 3) Review + Verify (lcc-reviewer → lcc-tester)
- Reviewer focuses on behavioral equivalence, readability, and any performance tradeoffs
- Tester runs the relevant suite and/or targeted repro steps

## Usage Examples

```
# Simplify recently modified code
Please simplify the code I just wrote

# Simplify specific files
Simplify the src/utils/helpers.ts file

# Simplify with focus on specific patterns
Simplify this component and focus on reducing nesting
```

## Handoff Protocol

Upon completion, the simplifier provides:

```json
{
  "type": "handoff",
  "next_role": "Reviewer|Tester",
  "summary": "What was simplified, key equivalence checks, and any perf wins",
  "next_instructions": "Review focus areas and verification steps"
}
```
