---
description: Safely modify the database schema and apply migrations
---

1.  **Analyze Request & Schema**:
    - Ask the user what changes are needed in the database.
    - Read `prisma/schema.prisma`.
    - **CRITICAL CHECK**: If adding a new table that stores tenant data, ensure it has:
        - `restaurantId String`
        - `restaurant Restaurant @relation(fields: [restaurantId], references: [id])`
        - `@@index([restaurantId])` (Non-clustered index for performance).

2.  **Modify Schema**:
    - Edit `prisma/schema.prisma` with the changes.
    - Ensure relationships are correctly defined.

3.  **Generate Migration**:
    - Run: `npx prisma migrate dev --name <descriptive_name>` (Ask user for name or propose one).
    - Wait for the command to complete.

4.  **Verify**:
    - Check the generated SQL file in `prisma/migrations/` to ensure it looks correct.
    - If the migration failed, read the error, revert changes if necessary, and fix the schema.
    - **Regenerate Client**: Usually happens automatically, but if not, run `npx prisma generate`.
