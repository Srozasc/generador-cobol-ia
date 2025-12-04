---
description: Systematically debug an issue using a scientific approach
---

1.  **Reproduce the Issue**:
    - Ask user for steps to reproduce the bug.
    - If possible, create a **reproduction test case** (e.g., a unit test that fails with the reported error).
    - If not possible to test (e.g., UI glitch), describe the manual reproduction steps clearly.

2.  **Analyze**:
    - Read relevant files.
    - Check logs (server logs, browser console).
    - Use `console.log` or debugger if needed (remember to remove later).

3.  **Hypothesize & Fix**:
    - Formulate a hypothesis: "The bug is caused by X because Y".
    - Apply the fix.

4.  **Verify**:
    - Run the reproduction test case (it should now PASS).
    - If manual, perform the reproduction steps again to confirm the bug is gone.
    - **Regression Check**: Run related tests to ensure no side effects.
