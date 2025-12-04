---
description: Analyze the codebase and answer questions without modifying code
---

1. **Analyze the Request**: Identify the core question or doubt the user has about the project.

2. **Gather Context**:
   - Use `list_dir` to understand relevant directory structures if needed.
   - Use `codebase_search` or `grep_search` to find relevant code snippets, classes, or functions related to the query.
   - Use `view_file` to read specific files in detail.
   - **Constraint**: Do NOT modify any files. Do NOT run tests unless necessary to demonstrate behavior (and only if safe).
   - **CRITICAL**: Your job is ONLY to explain. You are strictly forbidden from using tools that write to files, run destructive commands, or modify the state of the project.

3. **Synthesize Answer**:
   - Explain the logic, architecture, or flow found in the code.
   - Reference specific files and line numbers.
   - If the user asked "how to do X", explain the approach based on existing patterns in the project.

4. **Final Output**: Present the explanation clearly in Spanish.
