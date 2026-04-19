## execution enforcement

**CRITICAL testing rules during implementation:**

1. **after completing code changes in a task**:
   - STOP before moving to next task
   - add tests for all new functionality
   - update tests for modified functionality
   - run project test command
   - mark completed items with `[x]` in plan file

2. **if tests fail**:
   - fix the failures before proceeding
   - do NOT move to next task with failing tests
   - do NOT skip test writing

3. **only proceed to next task when**:
   - all task items completed and marked `[x]`
   - tests written/updated
   - all tests passing

4. **plan tracking during implementation**:
   - update checkboxes immediately when tasks complete
   - add ➕ prefix for newly discovered tasks
   - add ⚠️ prefix for blockers
   - modify plan if scope changes significantly

5. **on completion**:
   - verify all checkboxes marked
   - run final test suite
   - move plan to `docs/plans/completed/`
   - create directory if needed: `mkdir -p docs/plans/completed`

6. **partial implementation exception**:
   - if a task provides partial implementation where tests cannot pass until a later task:
     - still write the tests as part of this task (required)
     - add TODO comment in test code explaining the dependency
     - mark the test checkbox as completed with note: `[x] write tests ... (fails until Task X)`
     - do NOT skip test writing or defer until later
   - when the dependent task completes, remove the TODO comment and verify tests pass

this ensures each task is solid before building on top of it.

## key principles

- **one question at a time** - do not overwhelm user with multiple questions in a single message
- **multiple choice preferred** - easier to answer than open-ended when possible
- **DRY, YAGNI ruthlessly** - avoid unnecessary duplication and features, keep scope minimal (but prefer duplication over premature abstraction when it reduces coupling)
- **lead with recommendation** - have an opinion, explain why, but let user decide
- **explore alternatives** - always propose 2-3 approaches before settling (unless obvious)
- **duplication vs abstraction** - when code repeats, ask user: prefer duplication (simpler, no coupling) or abstraction (DRY but adds complexity)? explain trade-offs before deciding
