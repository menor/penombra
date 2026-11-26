# Research: Hono, Fastify and Express 5 compared

Ticket: #39. Map: #34. Checked 26 November 2026.

Question: which Node framework fits the Penombra API? It must serve REST and `/mcp` from one process on Node LTS. Sessions follow ADR 0006: a random ID in an `HttpOnly` cookie, a server-side row, and CSRF protection.

This file lays out facts and trade-offs. It does not pick. The pick goes into an ADR or a `CONTEXT.md` row through #45.

## Summary

| Area | Hono 4 | Fastify 5 | Express 5 |
|---|---|---|---|
| Latest version | 4.13.22 (25 Nov 2026) | 5.12.8 (2 Nov 2026) | 5.3.0 (9 Oct 2026) |
| Stable releases, last 12 months | 71 | 26 | 7 (4.x and 5.x) |
| Next major | 5.0.0-rc.1 (10 Oct 2026) | 6.0.0-alpha.6 (2 Nov 2026) | none published |
| Validation and typed routes | `@hono/zod-validator` or `@hono/standard-validator`. Types flow into handlers and an RPC client | JSON Schema on each route, built in. Type providers for Zod, TypeBox, json-schema-to-ts | None built in. Hand-written Zod calls or middleware |
| OpenAPI | `@hono/zod-openapi` (first-party middleware repo) or `hono-openapi` | `@fastify/swagger` reads route schemas | None first-party. For example `@asteasolutions/zod-to-openapi` |
| Server-side session (ADR 0006) | None. `@hono/session` stores data in an encrypted cookie, not an ID plus a row. Hand-write it with `hono/cookie` | `@fastify/session` with a store. Store needs `compareAndSet` | `express-session` with a store, for example `connect-pg-simple` |
| CSRF | Built-in `hono/csrf`: checks `Origin` and `Sec-Fetch-Site` | `@fastify/csrf-protection`: token in cookie or session | `csurf` archived. Third-party, for example `csrf-csrf` |
| Rate limit | Third-party `hono-rate-limiter` | First-party `@fastify/rate-limit` | Third-party `express-rate-limit` |
| Sentry | `@sentry/hono`, `sentry(app)` middleware | `fastifyIntegration` in `@sentry/node`, v5 via diagnostics channels | `expressIntegration` and `setupExpressErrorHandler` in `@sentry/node` |
| Tests without a socket | `app.request()` and `testClient()` | `app.inject()` | No. `supertest` binds an ephemeral local port |
| MCP Streamable HTTP | `@modelcontextprotocol/hono`. Web-standard transport, no Node adapter | `@modelcontextprotocol/fastify` plus `@modelcontextprotocol/node` | `@modelcontextprotocol/express` plus `@modelcontextprotocol/node`. Only adapter with bearer-auth middleware |
| Hello-world requests/s (Fastify-run benchmark) | 74,163 | 78,697 | 53,785 |

## Versions and maintenance

Node LTS lines on 26 November 2026: 26 (Lithium, 26.13.1), 24 (Krypton), 22 (Jod), 20 (Iron). Source: https://nodejs.org/dist/index.json, checked 26 Nov 2026.

All counts below come from the npm registry (`https://registry.npmjs.org/<package>`), checked 26 Nov 2026. "Stable releases" counts versions without a prerelease tag published since 26 Nov 2025.

| Package | Latest | Released | Stable releases, 12 months | Downloads, 18 to 24 Nov 2026 | Engines |
|---|---|---|---|---|---|
| `hono` | 4.13.22 | 2026-11-25 | 71 | 112.4M | node >=16.9.0 |
| `fastify` | 5.12.8 | 2026-11-02 | 26 | 23.8M | none set |
| `express` | 5.3.0 | 2026-10-09 | 7 | 209.9M | node >= 18 |

Download counts: https://api.npmjs.org/downloads/point/last-week/<package>, checked 26 Nov 2026. Downloads include transitive installs, so they measure reach, not choice.

GitHub, checked 26 Nov 2026 (open count mixes issues and pull requests):

| Repo | Stars | Open issues and PRs | Last push |
|---|---|---|---|
| https://github.com/honojs/hono | 33,086 | 375 | 2026-11-26 |
| https://github.com/fastify/fastify | 37,462 | 212 | 2026-11-26 |
| https://github.com/expressjs/express | 69,753 | 267 | 2026-11-19 |

### Coming majors

- **Hono 5.** `5.0.0-rc.0` on 8 Oct 2026, `5.0.0-rc.1` on 10 Oct 2026 (npm `next` tag). Breaking changes: ESM only, runtime adapters in separate packages, `c.req.json()` returns `unknown`, `c.req.query()` may return `undefined`. Source: https://github.com/honojs/website/blob/5d49625/docs/guides/migrating-to-v5.md, checked 26 Nov 2026.
- **Fastify 6.** 7 alphas from 11 Aug to 2 Nov 2026. Fastify's LTS table lists v6 for Node 24 and 26, release date "TDB". v5 supports Node 20, 22, 24 and 26, end of LTS "TBD". Source: https://github.com/fastify/fastify/blob/f5757f1/docs/Reference/LTS.md, checked 26 Nov 2026.
- **Express.** No 6.x on npm. The support page lists 5.x (from September 2024) and 4.x as "ongoing". Only the latest release of each major line is supported. Source: https://expressjs.com/en/support/, checked 26 Nov 2026.

Consequence: Hono and Fastify each face a major upgrade within the build. Express does not.

## Request validation and typed routes

- **Hono.** Built-in `validator()` plus `@hono/zod-validator` (0.9.1, 31 Aug 2026) and `@hono/standard-validator` (0.4.1, 26 Oct 2026). Standard Schema covers Zod, Valibot and ArkType. Source: https://github.com/honojs/website/blob/5d49625/docs/guides/validation.md. Validated types reach the handler and the RPC client. The typed `testClient()` needs routes chained on the `Hono` instance. Source: https://github.com/honojs/website/blob/5d49625/docs/helpers/testing.md.
- **Fastify.** Each route takes a JSON Schema for body, query, params and response. Type providers turn schemas into handler types: `@fastify/type-provider-zod` (1.0.3, 25 Oct 2026), `@fastify/type-provider-typebox` (6.3.0), `@fastify/type-provider-json-schema-to-ts`. Source: https://github.com/fastify/fastify/blob/f5757f1/docs/Reference/Type-Providers.md.
- **Express 5.** No validation or typed routes in core. Types come from `@types/express`. Express 5 forwards rejected promises from async handlers to the error handler, so `.catch(next)` is gone. Source: https://expressjs.com/en/guide/migrating-5.html, checked 26 Nov 2026.

## OpenAPI generation

- **Hono.** `@hono/zod-openapi` 1.6.3 (4 Sep 2026) lives in the first-party `honojs/middleware` repo. `hono-openapi` 1.6.0 (14 Nov 2026) is third-party. Both appear in Hono's third-party middleware list. Source: https://github.com/honojs/website/blob/5d49625/docs/middleware/third-party.md.
- **Fastify.** `@fastify/swagger` 9.9.5 (16 Nov 2026) builds the document from route schemas. `@fastify/swagger-ui` 6.1.5 serves it. The same schema validates, types and documents a route.
- **Express.** No first-party tool. One option: `@asteasolutions/zod-to-openapi` 9.1.0 (19 Jul 2026). Routes and the document stay in step by hand.

## Cookie sessions and CSRF (ADR 0006)

ADR 0006 needs a random session ID in the cookie and the session in a PostgreSQL row.

- **Hono.**
  - `@hono/session` 0.2.2 uses "encrypted JSON Web Tokens" in the cookie. That is the client-side pattern, not ADR 0006. Source: https://github.com/honojs/middleware/blob/060c5cd/packages/session/README.md.
  - So the session layer is hand-written: `getCookie`, `setCookie` (with `httpOnly`, `secure`, `sameSite`) from `hono/cookie`, plus a table lookup. Source: https://github.com/honojs/website/blob/5d49625/docs/helpers/cookie.md.
  - `hono/csrf` checks the `Origin` and `Sec-Fetch-Site` headers. It checks only unsafe methods with form content types: `application/x-www-form-urlencoded`, `multipart/form-data`, `text/plain`. A JSON body is out of its scope; cross-site JSON needs a CORS preflight instead. It needs `Origin` to survive proxies. Source: https://github.com/honojs/website/blob/5d49625/docs/middleware/builtin/csrf.md.
- **Fastify.**
  - `@fastify/session` 11.2.1 (20 Nov 2026) stores session data server-side through a store. The store must implement `set`, `get`, `destroy` and `compareAndSet`. "Stores written for express-session need an adapter that implements `compareAndSet`." So a PostgreSQL store is likely hand-written. Source: https://github.com/fastify/session/blob/2f0eb34/README.md.
  - `@fastify/csrf-protection` 8.0.2 (9 Oct 2026) keeps the CSRF secret in a cookie (`@fastify/cookie`) or in the session. Source: https://github.com/fastify/csrf-protection (README), checked 26 Nov 2026.
- **Express.**
  - `express-session` 1.19.0 (22 Jan 2026) with a store. `connect-pg-simple` 10.0.0 (13 Sep 2024) stores sessions in PostgreSQL. The default `MemoryStore` "is purposely not designed for a production environment". Source: https://github.com/expressjs/session (README), checked 26 Nov 2026.
  - `csurf` 1.11.0 is deprecated on npm: "archived and no longer maintained". A third-party package such as `csrf-csrf` 4.1.0 (1 Nov 2026) replaces it.

In all three, the session row and the expired-guest job are Penombra code. Only the cookie and middleware glue differ.

## Rate limiting

ADR 0006 needs a limit on guest-account creation. S12 needs one on sign-in.

| Framework | Package | Owner | Latest | Stars |
|---|---|---|---|---|
| Hono | `hono-rate-limiter` | rhinobase (third-party) | 0.5.4, 6 Sep 2026 | 656 |
| Fastify | `@fastify/rate-limit` | fastify (first-party) | 11.3.0, 20 Nov 2026 | 606 |
| Express | `express-rate-limit` | express-rate-limit (third-party) | 8.7.5, 18 Nov 2026 | 3,319 |

Sources: npm registry and GitHub repos, checked 26 Nov 2026.

## Sentry

Checked against https://docs.sentry.io and the SDK source at https://github.com/getsentry/sentry-javascript (commit a159856), 26 Nov 2026. `@sentry/node` is 11.18.0 (25 Nov 2026). It requires Node `>=20.19.0 <22`, `>=22.12.0 <23` or `>=23.2.0`.

All three load Sentry before the app with `node --import ./instrument.mjs`.

- **Hono.** Install `@sentry/hono` and `@sentry/node`. Import from `@sentry/hono/node`, then `app.use(sentry(app))`. Supports Hono 4.0.0 and later. Source: https://docs.sentry.io/platforms/javascript/guides/hono/manual-setup/. The older `@hono/sentry` middleware now points to the official SDK. Source: https://github.com/honojs/middleware/blob/060c5cd/packages/sentry/README.md.
- **Fastify.** "Fastify doesn't need its own Sentry SDK." `fastifyIntegration` captures errors from routes and hooks. 3xx and 4xx errors are skipped by default. Source: https://docs.sentry.io/platforms/javascript/guides/fastify/. On Fastify 5 the SDK subscribes to Fastify's diagnostics channels (`packages/server-utils/src/integrations/fastify/errors.ts`). `setupFastifyErrorHandler` is exported from `@sentry/node`.
- **Express.** "Express doesn't need its own Sentry SDK." `expressIntegration` captures route and middleware errors, and `setupExpressErrorHandler` is exported from `@sentry/node`. Source: https://docs.sentry.io/platforms/javascript/guides/express/. The SDK instruments `express` 4.x and `router` 2.x, which Express 5 uses (`packages/server-utils/src/orchestrion/config/express.ts`).

No gap separates them here. Hono needs one extra package.

## Testing without a network

- **Hono.** `app.request(path, init)` passes a `Request` to the app and returns a `Response`. No socket opens. `testClient(app)` adds typed calls. Sources: https://github.com/honojs/website/blob/5d49625/docs/guides/testing.md and `docs/helpers/testing.md`.
- **Fastify.** `app.inject()` fakes the HTTP request through `light-my-request`. No socket opens. Source: https://github.com/fastify/fastify/blob/f5757f1/docs/Guides/Testing.md.
- **Express.** No built-in injection. `supertest` 7.3.2 binds the app "to an ephemeral port" when it is not listening. That is a local socket, not an outside network. Source: https://github.com/forwardemail/supertest (README), checked 26 Nov 2026.

All three run under Vitest.

## Mounting the MCP Streamable HTTP transport

Source for this section: https://github.com/modelcontextprotocol/typescript-sdk at commit 5ee54ee, checked 26 Nov 2026. Files: `README.md`, `packages/middleware/*/README.md`, `docs/serving/{hono,fastify,express,authorization}.md`.

SDK state:
- v2 is the stable line: `@modelcontextprotocol/server` 2.4.0 (23 Oct 2026). It implements the 2026-07-28 MCP spec.
- v1 (`@modelcontextprotocol/sdk` 1.32.2, 23 Oct 2026) gets fixes "for at least six months after the v2 release (2026-07-27)". That is until about 27 Jan 2027.
- v2 ships one thin adapter per framework: `@modelcontextprotocol/express` 2.0.2, `@modelcontextprotocol/hono` 2.0.2, `@modelcontextprotocol/fastify` 2.0.1, and `@modelcontextprotocol/node` 2.1.2.

How each mounts `/mcp`:

- **Hono.** `createMcpHandler(factory).fetch(c.req.raw, { parsedBody, authInfo })`. The transport is web-standard, so no Node adapter is needed. `createMcpHonoApp()` adds JSON parsing and `Host`/`Origin` checks. The bearer-token gate is `requireBearerAuth` from `@modelcontextprotocol/server`, the web-standard variant. A second option, `@hono/mcp` 0.3.5, wraps the v1 SDK.
- **Fastify.** `toNodeHandler(createMcpHandler(factory))(request.raw, reply.raw, request.body)`. The handler runs on Node's raw request, outside Fastify's reply. Auth is set as `auth` on `request.raw`. The Fastify adapter exports no auth helpers.
- **Express.** `toNodeHandler(...)(req, res, req.body)`. `@modelcontextprotocol/express` alone exports `requireBearerAuth` and `mcpAuthMetadataRouter`, which serve the RFC 9728 metadata. The docs warn that `@modelcontextprotocol/express` 2.0.1 drops `expectedResource`, so upgrade it with the server package.

All three adapters bind `127.0.0.1` by default. A public deploy must pass `host: '0.0.0.0'` and `allowedHosts`. All three serve REST and `/mcp` from one process, as #34 requires.

The SDK states that the Express and web-standard auth gates "are both adapters over one core". The status codes and challenges match. So OAuth (Phase 6) works on Hono and Express with first-party code. On Fastify it needs the web-standard gate called by hand, or a hand-written hook.

## Performance

One source only: https://github.com/fastify/benchmarks (commit 368b407), run 14 Nov 2026. Machine: Linux x64, 4 vCPUs, 15.6 GB. Node 24.22.3. The Fastify team maintains this benchmark.

| Framework | Version | GET hello world, requests/s | GET latency, ms | POST, requests/s | POST latency, ms |
|---|---|---|---|---|---|
| node:http (baseline) | 24.22.3 | 81,011 | 11.98 | 55,477 | 17.53 |
| Fastify | 5.12.8 | 78,696 | 12.18 | 47,248 | 20.64 |
| Hono (on `@hono/node-server`) | 4.13.17 | 74,163 | 12.99 | 39,976 | 24.50 |
| Express | 5.3.0 | 53,785 | 18.13 | 27,924 | 35.30 |

Read with care:
- These are hello-world routes. The latency column is measured under 100 concurrent connections. It is not the cost of one request.
- Penombra's S3 target is p95 under 200 ms for search. A PostgreSQL query will likely dominate framework overhead.
- No benchmark run on Penombra's own routes exists yet. Phase 3 measures S3.

## Trade-offs

These are the axes that separate the three for Penombra. The human picks.

1. **One schema for validation, types and OpenAPI.** Fastify does it in core. Hono does it with `@hono/zod-openapi`. Express needs it assembled by hand.
2. **ADR 0006 sessions.** Express has the most ready-made path (`express-session` plus `connect-pg-simple`), but `connect-pg-simple` has not shipped since Sep 2024. Fastify needs a store with `compareAndSet`. Hono needs the session layer written by hand. The hand-written layer is small: a cookie and a row lookup.
3. **CSRF.** Hono's built-in check relies on `Origin` and `Sec-Fetch-Site`, with no token. Fastify ships a first-party token plugin. Express's own `csurf` is archived.
4. **MCP and OAuth.** Hono gets the web-standard transport with no adapter. Express gets the only framework-specific auth middleware. Fastify writes MCP responses to `reply.raw`, bypassing its own reply and serialisation.
5. **Upgrade risk during the build.** Hono 5 is at release candidate. Fastify 6 is at alpha. Express has no new major in sight.
6. **Tests.** Hono and Fastify test with no socket. Express tests through a local port.
7. **Raw throughput.** Fastify leads Express by 46% on hello-world GET in its own benchmark. Hono sits 6% below Fastify. The database will likely dominate.

## Not verified

- Release counts include patch releases. They measure cadence, not stability.
- Whether `hono/csrf` alone meets S12 for JSON endpoints. That depends on the CORS policy, which is not decided.
- Whether `connect-pg-simple` 10.0.0 works with `express-session` 1.19.0 on Node 24 or 26. Not tested.
- Hono's own benchmark claims. Not checked; only the Fastify-run benchmark is cited.
- The behaviour of `@modelcontextprotocol/fastify` with Fastify 6 alphas.
