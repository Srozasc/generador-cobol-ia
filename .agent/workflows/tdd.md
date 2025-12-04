---
description: Implement a new feature using TDD (Test Driven Development)
---

1.  **Analyze the Requirement**:
    - Ask the user for the specific feature or component to implement.
    - Review `documentacion/inicial/especificacion de caracteristicas.md` if relevant.
    - Identify the target file path (e.g., `app/api/orders/route.ts`) and the test file path (e.g., `tests/integration/orders.test.ts`).

2.  **Create the Test (RED)**:
    - Create the test file if it doesn't exist.
    - Write a test case that asserts the expected behavior (e.g., "should return 201 when creating a valid order").
    - Ensure the test fails (because the implementation doesn't exist or is empty).
    - Run the test to confirm failure: `npm test -- <test_file_path>` (Ask for confirmation before running).

3.  **Implement the Feature (GREEN)**:
    - Create or modify the implementation file.
    - Write the *minimum* code necessary to pass the test.
    - **Documentation (MANDATORY)**:
        - Add detailed JSDoc comments to all exported components, interfaces, and functions.
        - Explicitly describe props, return values, and complex logic in Spanish.
        - Explain security checks and multi-tenancy handling inline.
    - Remember strict rules:
        - Use `restaurantId` in all DB queries.
        - Use `lib/db.ts` for Prisma.
        - Validate inputs with Zod.

4.  **Verify (REFACTOR)**:
    - Run the test again: `npm test -- <test_file_path>` (Ask for confirmation).
    - If it passes, check if refactoring is needed (clean code, optimizations).
    - Verify that the code is well-documented and comments are clear.
    - If it fails, debug and repeat step 3.