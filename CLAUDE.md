# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## First Principle: Intent-Driven Minimalism
- **Code is Liability:** Never write a line of code that doesn't need to exist. Prefer reusing existing patterns over creating new abstractions.
- **Truth over Assumption:** The codebase and the execution environment are the only sources of truth. Always verify assumptions by reading files or running tests before proposing changes.
- **Solve the Problem, Not the Ticket:** Understand the "why" behind a request. If a requested change contradicts system integrity or introduces unnecessary complexity, propose a simpler alternative.
- **Atomic & Reversible:** Every intervention should be as small as possible and easy to roll back.

## 🛠️ Core Engineering Philosophy & Constraints

> "There are two ways of constructing a software design: One way is to make it so simple that there are **obviously no deficiencies**, and the other way is to make it so complicated that there are no obvious deficiencies."
> — **Tony Hoare** (1980 Turing Award)

> "Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, **not smart enough to debug it**."
> — **Brian Kernighan** (Unix Pioneer)

> "The power of abstract data types derives from the fact that they separate the **use of data from the details of its implementation**."
> — **Barbara Liskov** (2008 Turing Award)

> "The purpose of abstraction is not to be vague, but to create a **new semantic level** in which one can be absolutely precise."
> — **Edsger W. Dijkstra** (1972 Turing Award)

---

## Core Operational Principles

1. **Think before acting.** Read existing files before writing code.
2. **Be concise in output but thorough in reasoning.
3. **Prefer editing over rewriting whole files.** 
4. **Do not re-read files you have already read.** 
5. **Test your code before declaring done.**
6. **No sycophantic openers or closing fluff.**
7. **Keep solutions simple and direct.**
8. **User instructions always override this file.**

### 📋 Operational Rules for Claude

1.  **Hoare’s Law of Simplicity:** Prioritize the "obviously no deficiencies" approach. If a solution feels "clever," refactor it for readability.
2.  **Liskov’s Principle of Abstraction:** Ensure data implementation is strictly separated from its use to maintain modularity.
3.  **Dijkstra’s Precision:** Abstraction must provide clarity and precision at a higher level, never ambiguity.
4.  **Knuth’s Optimization Warning:** Focus on architectural correctness and clean structure first; avoid premature optimization until bottlenecks are proven.
5.  **Perlis’s Rule of Thought:** Provide solutions that improve the mental model of the codebase rather than just patching symptoms.

## Project Overview

ZKSoft 2025 is a large-scale enterprise management solution built on .NET 8.0 with a modular architecture. It consists of multiple business modules (ZKSoft.*) and industry-specific applications (CZL, BK2024, TX, Hjg, etc.).

## Debugging Workflow

When fixing bugs, first identify the exact root cause before implementing fixes. Avoid speculative multi-fix approaches. User will clarify if multiple issues exist.

## Simplicity Principles

Always prefer simple solutions over adding new fields/entities. Reuse existing database fields when possible (e.g., cLicenseType for quota tracking). Ask before adding new JSON columns or tables.

## Code Placement

When placing logic (validation, cleaning, transformation), confirm the exact line/file location with user before implementing. Avoid assumptions about method boundaries or class responsibilities.

## Build Commands

```bash
# Build the main solution
dotnet build ZKSoft.sln

# Build in Release configuration
dotnet build ZKSoft.sln -c Release

# Run the main web application
dotnet run --project ZKSoft/ZKSoft2025.csproj

# Run tests
dotnet test tests/YtStock.HighConcurrency.Tests/

# Publish NuGet packages (requires version and API key)
./publish-nuget.ps1 -NewVersion "26.2.5" -NuGetApiKey "your-key" -NuGetSource "http://nuget.zksoft.cc/v3/index.json"
```

## Project Creation Specification

When creating new projects in this repository, follow these strict dotnet CLI conventions:

### Creating a New Web API Project

```bash
# 1. Create project directory and navigate to it
mkdir -p {ParentDir}/{ProjectName}
cd {ParentDir}/{ProjectName}

# 2. Create Web API project (use --no-https to avoid HTTPS setup)
dotnet new webapi -n {ProjectName} --no-https

# 3. If nested folder was created, flatten structure
mv {ProjectName}/* .
rm -rf {ProjectName}

# 4. Create solution file (strict dotnet sln command)
dotnet new sln -n {ProjectName}

# 5. Add project to solution
dotnet sln add {ProjectName}.csproj

# 6. Add project references (from project root, use relative paths)
dotnet add reference ../../ZKSoft.Common/ZKSoft.Common.csproj
# ... add other required references
```

### Project Reference Rules

- Always use **relative paths** from the project directory to reference other projects
- Common shared projects to reference:
  - `ZKSoft.Common` - Required for AutoDI, utilities
  - `ZKSoft.AA` - For authentication/authorization
  - `ZKSoft.Voucher` - For document management
  - `ZKSoft.Flow` - For workflow integration
  - `ZKSoft.AI` - For AI service integration
  - `ZKSoft.Report` - For reporting capabilities
  - `ZKSoft.AS` - For archive management

### Example: Creating Hjg.Pmi Project

```bash
mkdir -p Hjg/Hjg.Pmi
cd Hjg/Hjg.Pmi
dotnet new webapi -n Hjg.Pmi --no-https
mv Hjg.Pmi/* . && rm -rf Hjg.Pmi
dotnet new sln -n Hjg.Pmi
dotnet sln add Hjg.Pmi.csproj
dotnet add reference ../../ZKSoft.AA/ZKSoft.AA.csproj \
                     ../../ZKSoft.AS/ZKSoft.AS.csproj \
                     ../../ZKSoft.Voucher/ZKSoft.Voucher.csproj \
                     ../../ZKSoft.AI/ZKSoft.AI.csproj \
                     ../../ZKSoft.Flow/ZKSoft.Flow.csproj \
                     ../../ZKSoft.Common/ZKSoft.Common.csproj \
                     ../../ZKSoft.Report/ZKSoft.Report.csproj
```

## Architecture

### Project Structure

- **ZKSoft/**: Main ASP.NET Core web application (entry point)
- **ZKSoft.AA**: Authentication and authorization module (permission management, user auth)
- **ZKSoft.Common**: Shared components and utilities (AutoDI, helpers)
- **ZKSoft.Flow**: Workflow engine
- **ZKSoft.Voucher**: Document/voucher management framework
- **ZKSoft.Budget**: Budget management system
- **ZKSoft.Bgma**: Budget preparation and approval
- **ZKSoft.MES**: Manufacturing execution system
- **ZKSoft.WMS**: Warehouse management system
- **ZKSoft.AI**: AI service integration (OpenAI, Volcengine)
- **ZKSoft.AS**: Basic archive management
- **ZKSoft.GDZC**: Fixed asset management
- **ZKSoft.OA**: Office automation
- **ZKSoft.Report**: Reporting system
- **ZKSoft.Sk**: Tax control and invoice recognition
- **ZKSoft.DingDing**: DingTalk integration
- **ZKSoft.QYWeiXin**: WeChat Work integration

### Service Pattern

Each module follows a consistent 3-file pattern within `{Feature}All/` directories:

1. **Interface** (`I{Feature}.cs`): Defines service contract, inherits from `ITransientDependency` (or `IScopeDependency`/`ISingletonDependency`)
2. **Implementation** (`Im{Feature}.cs`): Inherits from `RetVal` and implements the interface
3. **Controller** (`{Feature}Controller.cs`): ASP.NET Core API controller with `[Route("api/{module}/[controller]/[action]")]`

Example structure in `ZKSoft.AA/AACalendarAll/`:
- `IAACalendar.cs` - Interface with methods returning `RetValModel<T>`
- `ImAACalendar.cs` - Implementation extending `RetVal`
- `AACalendarController.cs` - API controller

### Dependency Injection System

Uses a custom AutoDI system in `ZKSoft.Common/AutoDI/`:

- **Marker Interfaces**:
  - `ITransientDependency`: Transient lifetime (default for services)
  - `IScopeDependency`: Scoped lifetime (per-request)
  - `ISingletonDependency`: Singleton lifetime

- **Registration**: `AutoDIProc.AddDataService()` scans all assemblies and auto-registers services based on these markers. Convention: implementation `ImXxx` maps to interface `IXxx`.

### Base Classes and Return Types

**`RetVal`** (`ZKSoft.AA/RetValAll/RetVal.cs`): Base class for all service implementations providing:
- `_db`: `SqlSugarClientProxy` for database access
- `_login`: `IPersonScope` for current user context
- Helper methods: `Suc()`, `Err()`, `Confirm()`, `ErrCode()` - return `RetValModel<T>`
- `GetMaxID()`, `GetMaxCode()`: Auto-increment ID/code generation
- `RecordChanges()`: Change tracking for audit logging

**`RetValModel<T>`**: Standard API response wrapper:
- `result`: 1 (success), -1 (error), 1001 (confirm), -3 (token expired)
- `resultdetail`: Message string
- `data`: Typed payload
- `logID`: Audit log ID

### Database Access

Uses **SqlSugarCore** ORM:
- `_db` (from `RetVal` base) provides `SqlSugarClientProxy`
- Use `_db.UseTran()` for transactions: `using (var tran = _db.UseTran()) { tran.CommitTran(); }`
- Lambda-based queries: `_db.Queryable<Entity>().Where(s => s.ID == id).First()`

**Important:** Never reuse `IQueryable` objects between count and data queries - always create fresh queries to avoid mutation bugs. Use `.Clone()` or rebuild the expression.

### SQL Generation Standards

For database quote styles: use single quotes (') for string literals. Confirm user's SQL dialect before generating scripts - they use single-quote style, not double quotes.

### Performance Optimization

**WARNING:** Never suggest `Parallel.ForEach` or naive parallel processing for database operations. Always use async queue-based architectures with bounded concurrency (e.g., `Channel<T>` with limited parallelism) to prevent database pressure.

### API Conventions

- Controllers use `[Route("api/{module}/[controller]/[action]")]` pattern
- Module prefix: `aa` (AA), `budget` (Budget), `mes` (MES), etc.
- All POST methods accept `[FromBody]` DTOs
- GET methods use `[FromQuery]` parameters
- All endpoints return `RetValModel<T>`

**Important:** For API endpoints accepting complex configuration objects, always use `[FromBody]` binding, not query parameters. Confirm binding approach before implementing controllers.

### Key Configuration

- **NuGet**: Uses internal feed `http://nuget.zksoft.cc/v3/index.json` (see `nuget.config`)
- **EditorConfig**: 4-space indentation for C#, CRLF line endings, UTF-8
- **Nullable**: Enabled project-wide with specific warning suppressions (CS8618, CS8602, etc.)

### Important Implementation Notes

1. **Transaction Management**: Always wrap database operations in `using (var tran = _db.UseTran())` and call `tran.CommitTran()` on success.

2. **Service Constructor Pattern**: Implementation classes receive `IServiceProvider` and pass to `RetVal` base:
   ```csharp
   public ImXxxService(IServiceProvider provider) : base(provider) { }
   ```

3. **ID Generation**: Use `GetMaxID(tableName, columnName, count)` instead of database identity columns for primary keys.

4. **Versioned Services**: Services can be versioned with `V####` suffix (e.g., `ImServiceV2024`), and `AutoDIProc` will handle registration by stripping the version suffix.

5. **Validation Pattern**: Services typically have `CheckMain()` methods that return error strings, accumulated and returned via `Err()` if non-empty.

### Testing

Test projects use **xUnit** with **FluentAssertions** and **Moq**:
- Located in `tests/` directory
- Run with `dotnet test {project}`

### Documentation

- `README.md`: Project overview and high-level documentation
- `knowledge.md`: Architecture and development guidelines
- `docs/`: Module-specific documentation (e.g., `docs/AI-Query-Module-Design.md`)
# Swarm Global Rules

## First Principle: Intent-Driven Minimalism
- **Code is Liability:** Never write a line of code that doesn't need to exist. Prefer reusing existing patterns over creating new abstractions.
- **Truth over Assumption:** The codebase and the execution environment are the only sources of truth. Always verify assumptions by reading files or running tests before proposing changes.
- **Solve the Problem, Not the Ticket:** Understand the "why" behind a request. If a requested change contradicts system integrity or introduces unnecessary complexity, propose a simpler alternative.
- **Atomic & Reversible:** Every intervention should be as small as possible and easy to roll back.

## 1) Goals

- Organize multi-agent collaboration using a Router–Worker architecture
- Ensure continuity via a traceable handoff protocol

## 2) Role boundaries (mandatory)

- Router: routing, decomposition, acceptance criteria only. No code edits, no test runs.
- Coder: implements changes. Must hand off to Reviewer when done.
- Reviewer: reviews security/correctness/maintainability. Does not edit files.
- Tester: runs/designs tests and produces repro steps. No large refactors.

## 3) Handoff protocol (mandatory)

Each handoff must include a JSON object in the output:

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester",
  "summary": "Progress summary (done/todo/risks)",
  "next_instructions": "Actionable task list for the next agent"
}
```

## 4) Handoff content requirements

- Must include: progress summary, next steps, and required context (files/commands/failure reasons)
- Must not include: secrets, tokens, or sensitive information

## 5) Agent teams (Experimental)

Agent teams allow parallel execution and decentralized coordination.

- **Team lead**: The main agent session. Responsible for spawning the team, approving plans, and final synthesis.
- **Teammates**: Independent agents with their own context windows.
- **Shared task list**: Use it to assign and track work. Teammates can self-claim tasks. Aim for 5-6 tasks per teammate to maximize productivity.
- **UI Shortcuts**: Use `Shift+Down` to cycle through teammates, `Ctrl+T` to toggle the task list, `Enter` to view a teammate's session, and `Escape` to interrupt.
- **Plan Approval**: For complex or risky tasks (e.g., refactors), the lead should spawn teammates with `Require plan approval before they make any changes`. The lead reviews and approves/rejects plans autonomously.
- **Communication**:
  - `message <teammate>`: Send a direct message to a specific teammate (e.g., Coder to Reviewer).
  - `broadcast <message>`: Send to all teammates (use sparingly).
- **Cleanup**: Once the task is complete, the lead must shut down all teammates and then run `Clean up the team` to remove shared resources.
- **Parallel patterns**:
  - **Scientific Debate**: Spawn 5+ teammates to investigate competing hypotheses and actively disprove each other.
  - **Parallel Review**: Assign reviewers with distinct lenses (Security, Performance, Test Coverage).
  - **Cross-layer coordination**: Separate teammates for frontend, backend, and testing.

## 6) Hooks and quality gates

Automated checks are enforced via `.claude/settings.json` and `.claude/hooks/`.

- **TaskCreated**: Fires when a task is being created. Rejects subjects < 10 characters or containing "TODO".
- **TaskCompleted**: Fires when a task is closed. Verifies that a summary or handoff report exists in the transcript and rejects "TODO" in subjects.
- **TeammateIdle**: Fires before a teammate stops. Ensures no work is left with unaddressed errors.

## 7) Failure handling

- If blocked, the summary must include: failure reason, repro steps, and a recommended fix path

## 8) Document-first workflow (mandatory for platform/API/prompt/limits + Claude Code configuration)

Before any code changes for tasks involving platform APIs, prompt optimization, model selection, token budgets, context windows, rate limits, structured outputs, or Claude Code configuration (subagents/skills/hooks/permissions):

- The Router must ensure relevant specs are reviewed first (local docs preferred).
- The Coder must not start implementation until the session config is updated (see below).

### Document index (project)

- Primary: `.claude/docs/claud_platform_menu.md`

### Instruction to (re)generate the menu doc

In Claude (chat) or Claude Code, run:

> Please visit `https://platform.claude.com/docs/en/home` and its core sub-pages (such as Prompt Engineering, Models, API Reference), extract all the core topics, and generate a Markdown format link menu document for me. The document should be categorized as 'Basic Concepts', 'Development Guidelines', and 'Performance Optimization', and retain the original URLs.

### “Read the book first, then do the work” starter instruction

When starting a development task, use:

> Based on the best practices outlined in the relevant specifications linked in `.claude/docs/claud_platform_menu.md`, please perform the following tasks: [your requirements].

### Session pre-flight (required)

Before `lcc-coder` writes code, it must summarize requirements from the relevant specs regarding:

- JSON schema definition (structured outputs / tool input schemas)
- Context window optimization (token budgets, long context, caching/compaction strategies)

and write them into:

- `.claude/session_config.json`
