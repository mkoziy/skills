---
name: reviewer-full
description: Comprehensive code review skill. Review code changes for documentation gaps, implementation issues, quality problems, over-engineering, and testing deficiencies. Provide detailed feedback on each aspect. Use when the user says "reviewer-full", "full review", or wants an in-depth code review covering all aspects of the code.
allowed-tools: Read, Bash, Glob, Grep
---

# Documentation

Review code changes and identify missing documentation updates.

## README.md (Human Documentation)

Check if changes require README updates:

Must document:
- New features or capabilities
- New CLI flags or command-line options
- New API endpoints or interfaces
- New configuration options
- Changed behavior that affects users
- New dependencies or system requirements
- Breaking changes

Skip:
- Internal refactoring with no user-visible changes
- Bug fixes that restore documented behavior
- Test additions
- Code style changes

## CLAUDE.md (AI Knowledge Base)

Check if changes require CLAUDE.md updates:

Must document:
- New architectural patterns discovered/established
- New conventions or coding standards
- New build/test commands
- New libraries or tools integrated
- Project structure changes
- Workflow changes
- Non-obvious debugging techniques

Skip:
- Standard code additions following existing patterns
- Simple bug fixes
- Test additions using existing patterns

## Plan Files

If changes relate to an existing plan:
- Mark completed items as done
- Update plan status if needed
- Note which plan items this change addresses

## What to Report

For each gap:
- Missing: what needs to be documented
- Section: where in the documentation it should go
- Suggested content: draft text or outline

Report problems only - no positive observations.

# Implementation

Review whether the implementation achieves the stated goal/requirement.

## Core Review Responsibilities

1. Requirement coverage - does implementation address all aspects of the stated requirement? Are there edge cases or scenarios not handled?

2. Correctness of approach - is the chosen approach actually solving the right problem? Could it fail to achieve the goal in certain conditions?

3. Wiring and integration - is everything connected properly? Are new components registered, routes added, handlers wired, configs updated?

4. Completeness - are there missing pieces that would prevent the feature from working? Missing imports, unimplemented interfaces, incomplete migrations?

5. Logic flow - does data flow correctly from input to output? Are transformations correct? Is state managed properly?

6. Edge cases - are boundary conditions handled? Empty inputs, null values, concurrent access, error paths?

## What to Report

For each issue found:
- Issue: clear description of what's wrong
- Impact: how this prevents achieving the goal
- Location: file and line reference
- Fix: what needs to be added or changed

Focus on correctness of approach, not code style.
Report problems only - no positive observations.

# Quality

Review code for bugs, security issues, and quality problems.

## Correctness Review

1. Logic errors - off-by-one errors, incorrect conditionals, wrong operators
2. Edge cases - empty inputs, nil/null values, boundary conditions, concurrent access
3. Error handling - all errors checked, appropriate error wrapping, no silent failures
4. Resource management - proper cleanup, no leaks, correct resource release
5. Concurrency issues - race conditions, deadlocks, thread/coroutine leaks
6. Data integrity - validation, sanitization, consistent state management

## Security Analysis

1. Input validation - all user inputs validated and sanitized
2. Authentication/authorization - proper checks in place
3. Injection vulnerabilities - SQL, command, path traversal
4. Secret exposure - no hardcoded credentials or keys
5. Information disclosure - error messages, logs, debug info

## Simplicity Assessment

1. Direct solutions first - if simple approach works, don't use complex pattern
2. No enterprise patterns for simple problems - avoid factories, builders for straightforward code
3. Question every abstraction - each interface/abstraction must solve real problem
4. No scope creep - changes solve only the stated problem
5. No premature optimization - unless addressing proven bottlenecks

## What to Report

For each issue:
- Location: exact file path and line number
- Issue: clear description
- Impact: how this affects the code
- Fix: specific suggestion

Focus on defects that would cause runtime failures, security vulnerabilities, or maintainability problems.
Report problems only - no positive observations.

# Simplification

Detect over-engineered and overcomplicated code - code that works but is more complex than necessary.

## Excessive Abstraction Layers

- Wrapper adds nothing - method just calls another method with same signature
- Factory for single implementation - factory pattern when only one concrete type exists
- Interface on producer side - interface defined where implemented, not where consumed
- Layer cake anti-pattern - handler -> service -> repository when each just passes through
- DTO/Mapper overkill - multiple types representing same data with conversion functions

## Premature Generalization

- Generic solution for specific problem - event bus for one event type
- Config objects for 2-3 options - options pattern when direct parameters suffice
- Plugin architecture for fixed functionality - extension points nothing extends
- Overloaded struct - one type handling all variations with many optional fields

## Unnecessary Indirection

- Pass-through wrappers - methods that only delegate to dependencies
- Excessive method chaining - builder pattern for simple constructions
- Interface wrapping primitives - custom types for standard library types
- Middleware stacking - multiple middlewares that could be one

## Future-Proofing Excess

- Unused extension points - hooks, callbacks, plugins with no callers
- Versioned internal APIs - v1/v2 when only one version used
- Feature flags for permanent decisions - flags always on/off

## Unnecessary Fallbacks

- Fallback that never triggers - default path conditions never met
- Legacy mode kept just in case - old code path always disabled
- Dual implementations - old + new logic when old has no callers
- Silent fallbacks hiding problems - catching errors and falling back instead of failing fast

## Premature Optimization

- Caching rarely-accessed data - cache for data read once at startup
- Custom data structures - complex structures when arrays/maps work
- Worker pools for occasional tasks - pooling for operations/hour
- Connection pooling overkill - complex pooling for single connection

## What to Report

For each finding:
- Location: file and line reference
- Pattern: which over-engineering pattern detected
- Problem: why this adds unnecessary complexity
- Simplification: what simpler code would look like
- Effort: trivial/small/medium/large

Report problems only - no positive observations.

# Testing

Review test coverage and quality.

## Test Existence and Coverage

1. Missing tests - new code paths without corresponding tests
2. Untested error paths - error conditions not verified
3. Coverage gaps - functions or branches without test coverage
4. Integration test needs - system boundaries requiring integration tests

## Test Quality

1. Tests verify behavior, not implementation details
2. Each test is independent, can run in any order
3. Descriptive test names that explain what is being tested
4. Both success and error paths tested
5. Edge cases and boundary conditions covered

## Fake Test Detection

Watch for tests that don't actually verify code:
- Tests that always pass regardless of code changes
- Tests checking hardcoded values instead of actual output
- Tests verifying mock behavior instead of code using the mock
- Ignored errors with _ or empty error checks
- Conditional assertions that always pass
- Commented out failing test cases

## Test Independence

1. No shared mutable state between tests
2. Proper setup and teardown
3. No order dependencies between tests
4. Resources properly cleaned up

## Edge Case Coverage

1. Empty inputs and collections
2. Null/nil values
3. Boundary values (zero, max, min)
4. Concurrent access scenarios
5. Timeout and cancellation handling

## What to Report

For each finding:
- Location: test file and function
- Issue: what's wrong with the test
- Impact: what bugs could slip through
- Fix: how to improve the test

Report problems only - no positive observations.