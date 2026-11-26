# Research: MCP TypeScript SDK capabilities

Ticket: #38. Map: #34. Checked 26 November 2026. Every source below was read on that date.

## Question

What is the state of the official MCP TypeScript SDK? Cover the version, the Streamable HTTP transport, OAuth (resource server and authorization server), and sessions. Which Node frameworks does it plug into? Which other TypeScript MCP libraries are worth a look?

Context: the MCP server runs inside the API process on an `/mcp` route. Its tools are scoped to the signed-in member (S13). ADR 0004 leaves the framework open: Hono, Express or Fastify.

## Short answer

1. The official SDK is at v2. Use `@modelcontextprotocol/server` 2.4.0. The old `@modelcontextprotocol/sdk` 1.32.2 gets fixes only.
2. v2 implements the 2026-07-28 spec. That spec removed sessions and the `initialize` handshake. The server is stateless by default: one fresh server instance per HTTP request.
3. The SDK ships adapters for Express, Fastify, Hono and plain Node `http`. All 4 are official, in the same repo.
4. The SDK covers only the resource-server half of OAuth: token check, 401 challenge, metadata document. It no longer ships an authorization server. Penombra must bring one.
5. Claude (claude.ai, Desktop, Claude Code) accepts OAuth with a Client ID Metadata Document or Dynamic Client Registration. The Free plan allows 1 custom connector.

## Versions on npm

Source: npm registry (`https://registry.npmjs.org/<package>`) and download API (`https://api.npmjs.org/downloads/point/last-week/<package>`), week 18 to 24 November 2026.

| Package | Latest | Published | Node engine | Weekly downloads |
|---|---|---|---|---|
| `@modelcontextprotocol/server` (v2) | 2.4.0 | 23 Oct 2026 | >=20 | 33.9M |
| `@modelcontextprotocol/client` (v2) | 2.4.0 | 23 Oct 2026 | >=20 | n/a |
| `@modelcontextprotocol/node` | 2.1.2 | 23 Oct 2026 | >=20 | 9.1M |
| `@modelcontextprotocol/express` | 2.0.2 | 2 Oct 2026 | >=20 | 2.7M |
| `@modelcontextprotocol/hono` | 2.0.2 | 2 Oct 2026 | >=20 | 278k |
| `@modelcontextprotocol/fastify` | 2.0.1 | 2 Oct 2026 | >=20 | 79k |
| `@modelcontextprotocol/sdk` (v1) | 1.32.2 | 23 Oct 2026 | >=18 | 92.9M |

- Node: the current LTS is 26.13.1 ("Lithium"), per `https://nodejs.org/dist/index.json`. It meets the `>=20` engine.
- Peer ranges: express adapter needs `express ^4.18 || ^5`. Fastify adapter needs `fastify ^5.2`. Hono adapter needs `hono ^4.11.4`. All 3 need `@modelcontextprotocol/server ^2.3.0`.
- v1 still leads downloads by 2.7 to 1. Many other libraries still depend on v1.

## Support status

Source: SDK README, `https://github.com/modelcontextprotocol/typescript-sdk` (main branch), and `VERSIONING.md` in the same repo.

- `main` is v2, "the stable release line, implementing the 2026-07-28 MCP spec".
- v2 was released on 27 July 2026. v1 lives on the `v1.x` branch. It gets "bug fixes and security updates for at least six months after the v2 release". That is until at least late January 2027.
- `core`, `client`, `server`, `server-legacy` and `codemod` release together under one version. The framework adapters bump on their own.
- The SDK follows SemVer. Dropping a Node LTS or a protocol revision counts as breaking.
- A codemod (`@modelcontextprotocol/codemod`) and a migration guide exist for v1 to v2: `https://ts.sdk.modelcontextprotocol.io/v2/migration/upgrade-to-v2`.
- Licence: Apache-2.0 for new code, MIT for older code.
- Tool schemas use Standard Schema: Zod v4, Valibot, ArkType or another compatible library.

## The 2026-07-28 spec changes the shape of the server

Source: `https://modelcontextprotocol.io/specification/2026-07-28/changelog`.

- Sessions and the `Mcp-Session-Id` header are gone (SEP-2567).
- The `initialize` handshake is gone. Each request carries protocol version and client capabilities in `_meta` (SEP-2575).
- Servers must implement `server/discover` to advertise versions and capabilities.
- The HTTP GET stream is replaced by `subscriptions/listen`, a long-lived POST response.
- SSE resumability (`Last-Event-ID`) is removed. A broken stream loses the in-flight request.
- Server-to-client requests (sampling, elicitation) become "multi round-trip requests". The server returns `input_required` and the client retries.
- Streamable HTTP POSTs must carry `Mcp-Method` and `Mcp-Name` headers (SEP-2243).
- Deprecated: Roots, Sampling, Logging, the old HTTP+SSE transport, and Dynamic Client Registration.

For Penombra: cross-call state must travel as tool arguments or live in PostgreSQL. Nothing lives in process memory between requests.

## Streamable HTTP and sessions in the SDK

Source: `docs/serving/http.md`, `docs/serving/sessions-state-scaling.md`, `docs/serving/legacy-clients.md`, `docs/protocol-versions.md` in the SDK repo.

- Entry point: `createMcpHandler(factory)`. It returns `{ fetch, close, notify, bus }`. `fetch` is a web-standard `(Request) => Promise<Response>`.
- The factory runs once per HTTP request. It receives `era`, `authInfo` and the raw `Request`. So a per-member tool set is built from `authInfo` in the factory.
- The docs advise: create database pools at module scope, keep the factory cheap.
- Since 2.0.2 a server object serves 1 connection. Reusing one `McpServer` across requests fails on the second or overlapping request (express adapter CHANGELOG, PR #2918).
- Response shape: a single JSON body by default. It upgrades to SSE only when a tool emits progress or log messages. `responseMode: 'json'` or `'sse'` pins one.
- Two eras. "Legacy" is 2024-10-07 to 2025-11-25 (with `initialize`). "Modern" is 2026-07-28.
- By default `createMcpHandler` also serves legacy clients, statelessly, per request (`legacy: 'stateless'`). `legacy: 'reject'` makes it modern-only.
- In stateless legacy mode, legacy `GET` and `DELETE` answer `405`. A client that needs a session stream will not work.
- Sessionful legacy serving is still possible. It needs the hand-wired `NodeStreamableHTTPServerTransport` with `sessionIdGenerator`, a session map, and an optional event store.
- Scaling: stateless nodes need no session affinity. Only `subscriptions/listen` crosses nodes. It needs a shared `ServerEventBus`, for example over Redis.
- The handler checks no `Host`, no `Origin` and no token. The framework app factories add `Host` and `Origin` checks by default on localhost. On a public bind, `allowedHosts` must list the hostname.

Unknown: which protocol revision Claude sends today. Claude's connector docs link to the 2025-11-25 spec. The default `legacy: 'stateless'` serves both, so this matters only if Penombra picks `legacy: 'reject'`.

## Framework adapters

Source: `docs/serving/express.md`, `docs/serving/fastify.md`, `docs/serving/hono.md`, and `packages/middleware/` in the SDK repo.

All 3 are official, thin, and add no MCP features. Each gives an app factory with JSON parsing and DNS rebinding protection.

| Framework | Package | Mount | Auth helpers in the package |
|---|---|---|---|
| Express | `@modelcontextprotocol/express` + `@modelcontextprotocol/node` | `toNodeHandler(handler)` on `app.all('/mcp')`, pass `req.body` | `requireBearerAuth`, `mcpAuthMetadataRouter`, `getOAuthProtectedResourceMetadataUrl` |
| Fastify | `@modelcontextprotocol/fastify` + `@modelcontextprotocol/node` | `toNodeHandler` on `request.raw`, `reply.raw`, `request.body` | None. Set `auth` on `request.raw` yourself |
| Hono | `@modelcontextprotocol/hono` | `handler.fetch(c.req.raw, { parsedBody })`. No Node adapter needed | None. Use the web-standard `requireBearerAuth` and `oauthMetadataResponse` from `@modelcontextprotocol/server` |

- The docs say the Express and web-standard `requireBearerAuth` are "adapters over one core". A verifier written for one serves the other.
- Hono and the web-standard path run on Node, Bun, Deno and Cloudflare Workers. Express and Fastify run through the Node adapter.
- Express has the most ready-made auth glue. Hono needs no Node shim. Fastify has the least auth glue and the fewest downloads (79k a week).

## OAuth: resource server half (in the SDK)

Source: `docs/serving/authorization.md` in the SDK repo, and `https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization`.

The spec requires an MCP server to:
- act as an OAuth 2.1 resource server;
- publish Protected Resource Metadata (RFC 9728);
- check that each token was issued for it as audience (RFC 8707);
- answer an invalid or expired token with `401`, and a missing scope with `403 insufficient_scope`.

The SDK covers this:
- `requireBearerAuth({ verifier, requiredScopes, resourceMetadataUrl, expectedResource })` returns `401` or `403` with a `WWW-Authenticate` challenge.
- You write `verifyAccessToken(token)`. It returns an `AuthInfo`: JWT check, RFC 7662 introspection, or an identity-provider call.
- `expectedResource` enforces the audience. It needs `@modelcontextprotocol/express` 2.0.2 or later. 2.0.1 drops it silently.
- `AuthInfo` without `expiresAt` is rejected with `401`.
- Tools read the caller as `ctx.http.authInfo`. The factory also gets it, so it can register a different tool set per caller.
- `scopeChallenge` on a tool, resource or prompt gives per-operation scope step-up.
- `mcpAuthMetadataRouter` (Express) and `oauthMetadataResponse` (web-standard) serve `/.well-known/oauth-protected-resource/mcp`. They also mirror the authorization server metadata at `/.well-known/oauth-authorization-server`.

## OAuth: authorization server half (not in the SDK)

Source: SDK `docs/serving/authorization.md` and `packages/server-legacy/README.md`.

- v2 removed the authorization server helpers (`mcpAuthRouter`, `ProxyOAuthServerProvider`).
- They survive in `@modelcontextprotocol/server-legacy/auth`. That package is "a frozen copy of v1 code", Express-only, and "planned for removal in v3".
- The SDK says: "Use a dedicated identity provider for new servers."

Penombra already plans its own sessions (ADR 0006). Claude needs an OAuth token tied to a member. So someone must issue tokens. Options:

| Option | What it is | Fits "no external service"? | Notes |
|---|---|---|---|
| A. Better Auth `@better-auth/mcp` 1.7.28 + `@better-auth/cimd` | Turns a Better Auth server into an OAuth 2.1 authorization server and protected resource for MCP | Yes. Runs in the API process | Docs show it with SDK v2 `createMcpHandler`. Client ID Metadata Documents recommended. Dynamic Client Registration off unless enabled. Needs its JWT plugin. Needs a `resource` setting so tokens carry the right `aud`. 2.0M weekly downloads. Would also decide the session library for ADR 0006 |
| B. `oidc-provider` 9.15.1 | A certified OpenID Connect provider library for Node | Yes | Client ID Metadata Document support not checked. More wiring to link it to Penombra sessions |
| C. Hosted identity provider (for example Auth0, WorkOS, Stytch) | An external authorization server | No. Adds an external service and maybe cost | Matches the SDK's advice. Conflicts with the one-click, no-external-service rule in `CONTEXT.md` |
| D. `server-legacy/auth` `mcpAuthRouter` | Frozen v1 helpers | Yes | Deprecated. Removed in v3. Express-only. Not a sound base for new code |
| E. Hand-written authorization server | Own `/authorize`, `/token`, metadata | Yes | Most code and most security risk. Shows the most backend work |

Sources: `https://www.better-auth.com/docs/plugins/mcp`; npm registry for versions.

## What Claude needs from the server

Source: `https://claude.com/docs/connectors/building/authentication` and `https://claude.com/docs/connectors/custom/remote-mcp`.

- Supported auth types by default: `oauth_cimd`, `oauth_dcr`, and `none`.
- Claude picks a Client ID Metadata Document only if the authorization server metadata has `"client_id_metadata_document_supported": true` and `"none"` in `token_endpoint_auth_methods_supported`. Otherwise it falls back to Dynamic Client Registration.
- A `401` with `WWW-Authenticate: Bearer resource_metadata="…"` starts sign-in. Claude ignores that header on a `200`.
- The metadata `resource` field must equal the URL the user enters, path included.
- Claude uses only the first entry in `authorization_servers`.
- PKCE with S256 on every request. Metadata should list `"code_challenge_methods_supported": ["S256"]`.
- Redirect URIs: `https://claude.ai/api/mcp/auth_callback` for hosted apps. Claude Code uses a loopback redirect on any port, for `localhost` and `127.0.0.1`.
- The token endpoint must accept `application/x-www-form-urlencoded`.
- Timeouts: 10 s for discovery, registration and token. 30 s for refresh.
- Refresh tokens should rotate for public clients. Claude adds `offline_access` if the authorization server lists it.
- Machine-to-machine `client_credentials` is not supported.
- Traffic comes from `160.79.104.0/21`.
- Custom connectors work on Free, Pro, Max, Ultra, Team and Enterprise. The Free plan allows 1.

## Other TypeScript MCP libraries

Source: npm registry and each project's README on GitHub.

| Library | Latest | Weekly downloads | Built on | Spec | Fit for Penombra |
|---|---|---|---|---|---|
| `fastmcp` | 4.29.1 | 704k | SDK v1, Hono inside | Legacy only. README: "does not support the current specification, 2026-07-28" | Poor. Owns its own HTTP server; would sit beside the API |
| `@hono/mcp` | 0.3.5 | 681k | SDK v1 (`^1.29.0`) | Legacy, sessionful | Poor. Superseded by the official `@modelcontextprotocol/hono` for v2 |
| `@platformatic/mcp` | 2.6.0 | 1.8k | Own implementation, Fastify plugin | Up to 2025-11-25 | Low. Redis sessions; low adoption |
| `mcp-handler` (Vercel) | 2.4.0 | 2.1M | SDK v2 server | Follows v2 | Poor. Peer-depends on Next.js |
| `xmcp` | 1.13.3 | 42k | SDK v2 | Follows v2 | Poor. Own framework and build; needs Node >=22.12 and React 19 |
| `@vitemcp/server` | 1.10.0 | n/a | Unknown | README of `fastmcp` points to it for 2026-07-28 | Too new. Repo created 5 Aug 2026, 27 stars |
| `mcp-framework` | 0.2.22 | n/a | SDK v1 | Legacy | Poor. Last release 16 Apr 2026 |

None adds a capability Penombra needs that the official v2 SDK lacks. The official SDK already mounts on an existing route in all 3 candidate frameworks.

## Options for the MCP SDK pick

| Option | Pros | Cons |
|---|---|---|
| 1. Official v2 `@modelcontextprotocol/server` 2.4.0 + framework adapter | Current spec. Stateless, so it fits one API process and any host. Official adapters for all 3 frameworks. Resource-server auth built in | No authorization server. v2 is 4 months old; fewer third-party examples than v1. Adapter fixes like `expectedResource` landed in October 2026 |
| 2. Official v1 `@modelcontextprotocol/sdk` 1.32.2 | More examples and tutorials. Ships `mcpAuthRouter` | Fixes only, for at least 6 months after 27 July 2026. Legacy spec. A migration would follow soon |
| 3. A third-party framework (`fastmcp` and others above) | Less boilerplate | Most target the legacy spec or bring their own server or framework. Adds a dependency between Penombra and the official SDK |

Coupled decision: the authorization server. Option 1 needs one of A to E above. Option A (Better Auth) also touches ADR 0006 and the Phase 4 sign-up choice. The MCP OAuth ADR is planned for Phase 6 (ADR 0006).

## Not verified

- Which protocol revision Claude sends to a custom connector today.
- Whether `oidc-provider` supports Client ID Metadata Documents.
- Better Auth behaviour beyond its docs page. No code was run.
- Download counts include CI and transitive installs. They show adoption, not quality.
- The SDK docs pages were read from the `main` branch source, not the rendered site. They match release 2.4.0 only as far as `main` has not moved since 23 October 2026.

## Sources

All checked 26 November 2026.

- SDK repo and README: https://github.com/modelcontextprotocol/typescript-sdk
- SDK versioning policy: https://github.com/modelcontextprotocol/typescript-sdk/blob/main/VERSIONING.md
- SDK protocol eras: https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/protocol-versions.md
- SDK serving over HTTP: https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/serving/http.md
- SDK sessions and scaling: https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/serving/sessions-state-scaling.md
- SDK legacy clients: https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/serving/legacy-clients.md
- SDK authorization: https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/serving/authorization.md
- SDK Express, Fastify, Hono recipes: https://github.com/modelcontextprotocol/typescript-sdk/tree/main/docs/serving
- SDK express adapter changelog: https://github.com/modelcontextprotocol/typescript-sdk/blob/main/packages/middleware/express/CHANGELOG.md
- SDK server-legacy README: https://github.com/modelcontextprotocol/typescript-sdk/blob/main/packages/server-legacy/README.md
- SDK releases: https://github.com/modelcontextprotocol/typescript-sdk/releases
- SDK v2 docs site: https://ts.sdk.modelcontextprotocol.io/v2/
- MCP spec 2026-07-28 changelog: https://modelcontextprotocol.io/specification/2026-07-28/changelog
- MCP spec 2026-07-28 authorization: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
- MCP spec 2026-07-28 transports: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports
- Claude connector authentication: https://claude.com/docs/connectors/building/authentication
- Claude custom connectors: https://claude.com/docs/connectors/custom/remote-mcp
- Better Auth MCP plugin: https://www.better-auth.com/docs/plugins/mcp
- npm registry: https://registry.npmjs.org/ (packages named in the tables)
- npm downloads API: https://api.npmjs.org/downloads/point/last-week/
- Node.js release index: https://nodejs.org/dist/index.json
- fastmcp README: https://github.com/punkpeye/fastmcp
- Hono MCP middleware README: https://github.com/honojs/middleware/tree/main/packages/mcp
- Platformatic MCP README: https://github.com/platformatic/mcp
