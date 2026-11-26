---
status: accepted
date: 2026-11-26
---

# Hono for the API

The API runs on Hono 4 (`hono@^4.13`) on Node 26 LTS through `@hono/node-server`. One process serves REST and `/mcp`. Each route has one Zod schema, defined with `@hono/zod-openapi`. It validates the request, types the handler and generates the OpenAPI document. We chose Hono because the MCP SDK v2 transport and its `requireBearerAuth` gate both use web-standard `Request` and `Response`. They mount on Hono with first-party code and no Node adapter. Tests call `app.request()` with no socket. The cost: a third-party rate limiter, a hand-written session layer for ADR 0006, and a Hono 5 upgrade during the build. Options and sources: [research note](https://github.com/menor/penombra/blob/research/node-framework/research/node-framework.md).

Speed and cost carried no weight. All three options are free. Fastify leads Hono by 6% on a hello-world benchmark run by the Fastify team. A PostgreSQL query will dominate the S3 search target. CSRF and sessions carried no weight either. In all three frameworks, the session row and the expired-guest job are Penombra code. Phase 4 picks the CSRF method.

## Considered options

- **Fastify 5.** Rejected: MCP responses go to `reply.raw`, which bypasses Fastify's reply. The Fastify MCP adapter has no auth helper, so Phase 6 would write its own bearer-token hook. Its strengths are first-party schemas, rate limit, CSRF and `inject()` tests. Fastify 6 is at alpha.
- **Express 5.** Rejected: it has no built-in validation, typed routes or OpenAPI, so the one-schema rule would be built by hand. Tests need `supertest` on a local port. `csurf` is archived, and `connect-pg-simple` last shipped in September 2024. Its strengths are stability, with no new major in sight, and the only framework-specific MCP auth middleware.

## Consequences

- Start on Hono 4. `@modelcontextprotocol/hono` declares `hono ^4.11.4` as its peer range, so it rejects Hono 5 (at 5.0.0-rc.1 on 26 November 2026). Upgrade in its own pull request once that range includes `^5`.
- Pin Node 26 in `engines` and `.nvmrc` in Phase 1.
- Rate limiting (ADR 0006, S12) needs `hono-rate-limiter` or our own code. Phase 4 picks one.
- Revisit if `@modelcontextprotocol/hono` falls more than 3 months behind a stable Hono 5, or if Phase 6 bearer auth can't run on the web-standard `requireBearerAuth`. Either one removes the main reason for choosing Hono over Fastify.
