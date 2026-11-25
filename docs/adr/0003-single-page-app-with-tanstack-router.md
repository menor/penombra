---
status: accepted
date: 2026-11-25
---

# Single-page app with TanStack Router

The frontend is a single-page app: React, TanStack Router, TanStack Query, Tailwind and TypeScript, served as static files. We chose this because server rendering helps only link previews and indexing here, and typed URL search parameters in TanStack Router fit the faceted filters. The cost: shared list pages get no rich link preview unless the API adds one.

## Considered options

- **Next.js.** Rejected: server rendering buys little here, and it adds a server and a rendering model to learn and run.
- **TanStack Start.** Rejected for now. It went stable on 13 October 2026, needs Vite 8 or newer, and adds a Node server to run and secure. Its server functions had an XSS fix in a Vite 7-era release, which shows they are an attack surface. A migration path from Router to Start should exist but is unverified.

## Consequences

- If link previews for shared lists matter, add one small route on the API that returns HTML with meta tags, about 50 lines.
- Revisit if search indexing of catalogue pages becomes a goal.
