---
description: Create a new React component with strict TDD and styling rules
---

1.  **Analyze Component Requirements**:
    - Ask user for component name and purpose.
    - Determine location:
        - `components/ui/` (Generic, reusable atoms like buttons).
        - `components/dashboard/` (Admin panel specific).
        - `components/public/` (Customer facing).
        - `components/kitchen/` (Kitchen view).

2.  **Create Test Skeleton (RED)**:
    - Create `<ComponentName>.test.tsx` in the same folder (or `tests/unit/components/`).
    - Write a basic test: `it('renders correctly', () => { ... })`.
    - Run test to confirm failure (if component doesn't exist).

3.  **Implement Component (GREEN)**:
    - Create `<ComponentName>.tsx`.
    - Define `interface Props`.
    - Implement basic structure using Tailwind CSS.
    - **Rules**:
        - Use `export function ComponentName` (Named export).
        - Ensure it is responsive (mobile-first).
        - Add `aria-label` or semantic HTML for accessibility.

4.  **Verify & Refactor**:
    - Run the test again.
    - Check if code style matches project conventions.
    - Ensure no hardcoded strings (prepare for i18n if needed later, though not strict req yet).
