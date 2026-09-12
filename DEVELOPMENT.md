# Development handoff — 2026-09-12

## User intent
Continue coding autonomously. Give regular progress updates (user requested at least once in 15 minutes); explain stage and exact required action when stopping. Final GitHub push remains with the user. No paid LLM provider selected yet; do not ask for keys in chat.

## Current state
- Version 0.3, Node 24, native modules, SQLite, Ukrainian vanilla UI, no runtime npm dependencies.
- Server http://127.0.0.1:4317; start with npm start.
- Store layering: Store -> ResearchStore -> AssessmentStore -> TaskStore -> PlanStore, server uses PlanStore.
- 22 tests pass and isolated headless Edge browser smoke passes.
- Browser smoke covers project creation, source verification, structured assessment, schedules, recurring completion, research plan adoption, reload and mobile overflow; no JS errors.
- Playwright package is bundled at the runtime path discoverable through load_workspace_dependencies. Run with PLAYWRIGHT_MODULE pointing at that package. npm run test:browser.
- CUA and view_image helpers fail with setup refresh / trusted Node errors; headless browser through approved shell works.
- Sandbox helper repeatedly fails; approved escalated commands work. Do not infer missing workspace authorization.
- Local main and origin configured, no push. data directory ignored by Git.
- Live DB has real Ink Builder Program and network-docs research records. Do not mark source verified or user actions complete without user confirmation.

## Completed additions
1. Assessments with evidence and immutable revisions; source changes invalidate revisions in the same transaction.
2. Five manual scoring signals, coverage, separate risk/costs/deadline fields. No reward probabilities.
3. Exact timestamp/calendar validation, schedules, optimistic revisions, idempotent recurring completion; missing periods never invented as completed.
4. Rule-based research cues with exact source offsets, review-before-adoption, deterministic task IDs and stale evidence checks.
5. All new UI flows validated in a separate in-memory test server.

## Next work
- Await provider preference before configuring paid AI services; provider-neutral work can continue.
- Browser adapter for JS-only Ink apps page remains missing.
- Wallet / chain receipt verification and transaction simulation are not implemented.
- API remains local single-user only; no on-chain execution, credential storage or external account access.
- Monitor only runs while server is alive, opt-in every 6h. Its current setting is not automatically changed.
