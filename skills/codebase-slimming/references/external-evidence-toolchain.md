# External Evidence Toolchain

Use external analyzers as evidence providers, not as autonomous deletion authorities. A finding is
a candidate until repository search, runtime behavior, reflection or dependency-injection risk,
tests, and human review establish that removal is safe.

## Agent-facing runner

The Skill includes a Python 3.9, standard-library-only runner:

```bash
python3 scripts/quality_evidence.py inventory --target /absolute/project --json

python3 scripts/quality_evidence.py run \
  --target /absolute/project \
  --evidence-dir /absolute/project/.codebase-slimming/evidence/baseline-001 \
  --tool scc \
  --tool knip \
  --dry-run \
  --json

python3 scripts/quality_evidence.py compare \
  --before /absolute/project/.codebase-slimming/evidence/baseline-001/manifest.json \
  --after /absolute/project/.codebase-slimming/evidence/current-001/manifest.json \
  --json
```

Resolve the script path relative to this installed `SKILL.md`; do not assume the current working
directory is the Skill directory. `inventory` only checks project signals and executable presence.
`run --dry-run` validates applicability, availability, gates, and fixed command arguments without
creating the evidence directory or invoking an analyzer.

The real `run` command:

- executes only adapters named by repeated `--tool` flags;
- uses argument arrays without a shell and never installs dependencies;
- refuses to overwrite a non-empty evidence directory;
- records a bounded `--version` probe, then captures analyzer stdout and stderr with SHA-256 hashes
  and a versioned `manifest.json`;
- normalizes metrics when stable machine-readable output is available;
- returns nonzero when an analyzer returns nonzero, while preserving its evidence and exit code;
- labels the proof boundary instead of claiming that findings prove safe deletion.

## Built-in adapters

| Adapter | Project signal | Default evidence | Special boundary |
|---------|----------------|------------------|------------------|
| `scc` | Any visible source tree | JSON code, line, file, comment, blank, and complexity totals | Counts size; does not prove value or behavior |
| `knip` | JS/TS markers | JSON unused file, export, type, and dependency findings | Dynamic imports, framework conventions, and generated entry points need review |
| `dotnet-packages` | Solution or project file | JSON top-level and transitive package inventory | Uses `--no-restore`; SDK 10 uses noun-first command order |
| `dotnet-analyzers` | Solution or project file | Build-time CA/CS and third-party analyzer diagnostics | Forces analyzers during a Release build; requires `--allow-worktree-writes` for MSBuild outputs |
| `roslyn-analyzers` | Solution or project file | `dotnet format analyzers` JSON report and normalized diagnostic IDs | Uses `--verify-no-changes --no-restore`; requires `--allow-worktree-writes` for Roslyn/MSBuild intermediates |
| `coverlet` | Solution/project plus `coverlet.collector` or `coverlet.MTP` reference | VSTest collector or MTP-native Cobertura coverage | Requires `--allow-worktree-writes`; test/build outputs may touch `bin` and `obj` |
| `sonarqube` | `sonar-project.properties` | SonarScanner stdout, stderr, exit status, and hashes | Requires both `--allow-network` and `--allow-worktree-writes` |
| `dependency-check` | Supported dependency manifest | Local OWASP Dependency-Check JSON report | Runs with `--noupdate`; update the vulnerability database separately under explicit network authority |

Tool absence is reported as `missing`. The runner does not fall back to `npx`, package restore, a
container pull, Homebrew, or another installer because those would add network and supply-chain
side effects to an evidence collection step.

The Coverlet adapter is `not_applicable` until the repository declares one supported integration.
It uses `--collect "XPlat Code Coverage"` for `coverlet.collector`, and the MTP-native `--coverlet`
form for `coverlet.MTP`. If both packages are referenced, the MTP-native path wins, but the project
owner should remove the incompatible duplicate rather than treating that precedence as a repair.

The two .NET analyzer adapters answer different questions:

- `dotnet-analyzers` establishes whether the repository builds while SDK, NuGet, and third-party
  analyzers execute. It enables `RunAnalyzers` and `RunAnalyzersDuringBuild`, requests `AnalysisMode=All`,
  and only forces `EnableNETAnalyzers` when the repository does not reference
  `Microsoft.CodeAnalysis.NetAnalyzers` directly.
- `roslyn-analyzers` asks Roslyn which analyzer fixes would be required, but uses
  `--verify-no-changes`; it emits a JSON report and never authorizes the formatter to rewrite source.
  Exit code and diagnostic IDs remain evidence for a later reviewed change.

Generated reports under the tool-specific evidence directory are recorded with relative paths,
byte sizes, and SHA-256 hashes. This applies to Roslyn, Coverlet, and Dependency-Check artifacts.

## Tools that stay project-owned

NDepend and ArchUnit or NetArchTest are valuable architecture gates, but they are not safe universal
zero-configuration commands:

- NDepend needs its licensed executable, an analyzed solution, and a committed project or ruleset.
  Treat the `.ndproj` and CQLinq rules as retained verification artifacts; export their report into
  the same evidence directory and record the exact CI command and version.
- ArchUnit, ArchUnitNET, and NetArchTest rules execute as repository tests. Keep dependency direction,
  forbidden-cycle, and layering assertions beside the owning test project. Run them through the
  normal test command and store the test result, rather than inventing a generic adapter that cannot
  know the repository's intended architecture.
- OpenTelemetry is runtime evidence. Define the service, environment, observation window, traffic
  coverage, sampling, and query before treating “zero calls” as a deletion signal. Never equate an
  absent span with an unreachable code path without checking instrumentation coverage.

## Evidence ladder for deletion candidates

1. **Candidate:** static analyzer or dependency tool reports an unused or problematic item.
2. **Repository corroboration:** references, generated code, configuration, reflection, DI, plugins,
   serialization, scripts, and external contracts are checked.
3. **Behavior baseline:** build, tests, API or UI scenario, data behavior, and known defects are
   repeatable before editing.
4. **Bounded change:** one small removal or replacement is isolated in a reviewable batch.
5. **Post-change evidence:** the same checks run again, plus relevant failure and recovery paths.
6. **Runtime or human gate:** dynamic usage and business ownership are checked when static evidence
   cannot see the invocation path.

Only levels 4-6 authorize a deletion decision. Levels 1-3 produce evidence and a plan.
