# Development handoff — 2026-09-12

## User intent
Continue coding autonomously. Give regular progress updates (user requested at least once in 15 minutes); explain stage and exact required action when stopping. User explicitly authorized publishing current code to GitHub main on 2026-09-12. No paid LLM provider selected yet; do not ask for keys in chat.

## Current state
- Version 0.5, Node 24, native modules, SQLite, Ukrainian vanilla UI, no runtime npm dependencies.
- Server http://127.0.0.1:4317; start with npm start.
- Store layering: Store -> ResearchStore -> AssessmentStore -> TaskStore -> PlanStore, server uses PlanStore.
- 32 tests pass and isolated headless Edge browser smoke passes.
- Browser smoke covers project creation, source verification, structured assessment, schedules, recurring completion, research plan adoption, reload and mobile overflow; no JS errors.
- Playwright package is bundled at the runtime path discoverable through load_workspace_dependencies. Run with PLAYWRIGHT_MODULE pointing at that package. npm run test:browser.
- CUA and view_image helpers fail with setup refresh / trusted Node errors; headless browser through approved shell works.
- Sandbox helper repeatedly fails; approved escalated commands work. Do not infer missing workspace authorization.
- Local main and origin configured; first push to main verified at 4b62671. data directory ignored by Git.
- Live DB has real Ink Builder Program and network-docs research records. Do not mark source verified or user actions complete without user confirmation.

## Completed additions
1. Assessments with evidence and immutable revisions; source changes invalidate revisions in the same transaction.
2. Five manual scoring signals, coverage, separate risk/costs/deadline fields. No reward probabilities.
3. Exact timestamp/calendar validation, schedules, optimistic revisions, idempotent recurring completion; missing periods never invented as completed.
4. Rule-based research cues with exact source offsets, review-before-adoption, deterministic task IDs and stale evidence checks.
5. All new UI flows validated in a separate in-memory test server.

## Next work
- Await provider preference before configuring paid AI services; provider-neutral work can continue.
- Ink apps catalogue now reads public JSON data literals from same-origin Next.js assets without executing downloaded JavaScript. Saves names, descriptions and HTTPS websites in the source snapshot; individual app import remains future work.
- Wallet / chain receipt verification and transaction simulation are not implemented.
- API remains local single-user only; no on-chain execution, credential storage or external account access.
- Monitor only runs while server is alive, opt-in every 6h. Its current setting is not automatically changed.

## Latest addition
Cross-project agenda implemented and browser-tested; /api/agenda refreshes independently from forms. Current push request fulfilled; continued with agenda feature.

## Outcome ledger
OutcomeLedger is composed with the main store by the server. Records manual rewards/expenses, exact asset quantities and cent-valuations, unknown-value handling, idempotent requests and auditable voids. Browser smoke now covers record/void. No actual transactions or price lookups.

## Backups
POST /api/backup streams a session-protected SQLite backup. Temp files cleaned explicitly; portable DELETE journal avoids leftover WAL files. Restore CLI validates integrity/FKs/tables and reserves destination exclusively, refusing existing DB and sidecars. DROP_HUNTER_DB_PATH allows opening restored DB separately. Full round-trip and browser download tested.

## Погоджені джерела та ШІ-аналіз
Див. [RESEARCH_ROADMAP.md](RESEARCH_ROADMAP.md): шість джерел, запропонованих користувачем, вимоги до агентів, доказів, оцінки витрат і ризиків та етапи реалізації. Інтеграції цих джерел ще не реалізовані.
