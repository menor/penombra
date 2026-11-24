# Penombra

A visual catalogue of synthwave and darkwave, built on MusicBrainz data. Penombra is Catalan for half-light.

Fans will browse releases by tag, year, country and label, and keep public or private lists. Claude will query the catalogue and a user's lists through an MCP server. My goal: anyone can try it in 1 click, with no account.

## Status

**Phase 0 of 8: decisions. There is no app yet.** The phases, their exit checks and the success criteria are in [`plan.md`](plan.md). I update this section at the end of each phase.

## What to look at today

- **The data check.** Before choosing the scope, I sampled the MusicBrainz API with 5 scripts. Results: 26 of 26 sampled releases had a date, 1 of 26 had a producer or mixer credit, and 78% of 69 artists had a Bandcamp link. The credit result made me cut a planned feature. Scripts, raw output and limits: [`data-check/`](data-check/README.md).
- **Decisions.** I write an architecture decision record (ADR) with its trade-off for each hard-to-reverse decision: [`docs/adr/`](docs/adr/). 1 so far. The product context and the options I rejected are in [`CONTEXT.md`](CONTEXT.md).
- **How I work.**
  - 1 GitHub issue, 1 branch, 1 squash-merged pull request into `main` ([ADR 0001](docs/adr/0001-github-flow-squash-merge.md)).
  - Every pull request lists its evidence, its merge risk and what it left out.
  - Commit messages and pull request titles follow Conventional Commits, checked by commitlint in a git hook and in CI.
  - I build it with AI agents. Their instructions live in [`.agents/skills/`](.agents/skills/): planning, committing and opening pull requests.

## Planned stack

Planned, not built. My reasons are in [`CONTEXT.md`](CONTEXT.md).

- React, TanStack Router, TanStack Query, Tailwind and TypeScript, as a single-page app.
- A separate TypeScript REST API, with PostgreSQL full-text and trigram search.
- A Model Context Protocol (MCP) server with tools scoped to the signed-in user.
- Vitest, Playwright, GitHub Actions and Sentry.

## Licence

Code: [MIT](LICENSE).
