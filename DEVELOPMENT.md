# Development handoff — 2026-09-11

User intent: continue coding autonomously until a material decision or credentials are needed. When stopping, state the stage and exact next user action. Final GitHub push remains with the user.

## Current state
- Node 24 native modules, vanilla Ukrainian UI, SQLite; no external dependencies.
- Server at http://127.0.0.1:4317; start with npm start.
- 7 tests pass. Live HTTP import of Ink Builder Program and network docs succeeded.
- Browser automation fails to initialize (trusted Node process exited); visual QA outstanding.
- Sandbox helper repeatedly fails setup refresh; commands work with approved escalation. Do not assume this is missing project access.
- Local main branch and origin configured; local commits exist, no push.
- SQLite data ignored by Git, contains 2 real research records. Source verification remains manual.
- Monitoring opt-in, every 6h while server is running; unchanged content does not create events.

## Next material decision
User was asked whether AI analysis should use OpenAI API (separate billing/key), local Ollama, or rule-based/manual analysis. Never request secrets in chat. Await the choice before configuring a paid service.

## Next engineering work
1. AI provider adapter, bounded evidence analysis and schema validation; source material must remain untrusted data.
2. Structured eligibility, costs, deadlines and assessments linked to evidence snapshots; no invented reward probabilities.
3. Browser adapter for the JS-only Ink apps catalog; do not label the current static response as successful discovery.
4. Wallet preview/simulation with user signatures, no private-key storage; contract templates later.
5. Real browser verification when the automation environment works.

## Known limitations
- Current discovery imports curated research sources, not a general crawler or confirmed airdrop feed.
- Current score is zero until actual signal assessment is implemented; verifying a source alone does not increase score.
- Source snapshots stored as text with digest and timestamp; no full HTML UI rendering.
- No LLM, autonomous check-ins, wallet execution, multi-user auth, or reward reconciliation yet.
- Onchain task completion is user-reported evidence, not independent transaction confirmation.
