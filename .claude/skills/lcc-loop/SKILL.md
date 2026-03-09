---
name: lcc-loop
description: Schedule a recurring prompt or task using the underlying Cron tools. This is a custom alternative to the built-in /loop command.
---

Schedule a recurring prompt to run at a specified interval or cron schedule.

## Usage

/lcc-loop [interval] [prompt]

- **interval**: (Optional) A duration like `5m`, `1h`, `2d`, or a standard 5-field cron expression (e.g., `0 9 * * 1-5`). If omitted, defaults to `10m`.
- **prompt**: The natural language prompt or command (e.g., `/review-pr 1234`) to run.

## Instructions for Claude

1. **Parse the Interval**:
   - If a duration (e.g., `30s`, `5m`, `2h`) is provided, convert it to an appropriate cron expression. Note that cron has 1-minute granularity, so seconds are rounded up.
   - If a 5-field cron expression is provided, use it directly.
   - If no interval is provided, use `*/10 * * * *` (every 10 minutes).

2. **Schedule the Task**:
   - Use the native `CronCreate` tool to register the task.
   - **CRITICAL**: `CronCreate` is a tool, not a shell command. DO NOT attempt to run `claude-cron` or any other shell command to create the task.
   - Set `recurring: true` for intervals/loops.
   - Provide the `prompt` and the calculated `cron` expression.

3. **Confirm**:
   - Inform the user that the task has been scheduled, providing the task ID and the effective schedule.

## Example

- `/lcc-loop 5m check if the build finished`
- `/lcc-loop 0 12 * * * remind me to eat lunch`
- `/lcc-loop /review-pr 5678` (defaults to every 10 minutes)

## Underlying Tools

- **CronCreate**: Create a new scheduled task.
- **CronList**: List all scheduled tasks (useful if the user asks "what tasks are running?").
- **CronDelete**: Delete a task by ID (useful if the user asks "cancel the loop").
