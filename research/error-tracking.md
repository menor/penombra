# Error tracking: Sentry free plan and OpenTelemetry options

Research for issue #37. Checked 26 November 2026. Prices and quotas change. Recheck before signing up.

Stack in scope: a React single-page app with TanStack Router (ADR 0003) and a separate Node LTS TypeScript API (ADR 0004). Goal: the shortest path to S11 in `plan.md`, one error traced from alert to fix.

## Question

1. What does the Sentry free plan include?
2. Does it cover the app and the API in one project or two?
3. What would an OpenTelemetry setup cost and take to run instead?
4. Which option reaches S11 fastest?

## 1. Sentry Developer plan (free)

Source: https://sentry.io/pricing/ (checked 26 Nov 2026).

| Item | Developer (free) | Team ($29/month, $26 billed yearly) |
|---|---|---|
| Users | 1 | Unlimited |
| Projects | Unlimited | Unlimited |
| Errors | 5,000 per month | 50,000 per month |
| Tracing spans | 5M | 5M |
| Session replays | 50 | 50 |
| Logs | 5 GB | 5 GB |
| Attachments | 1 GB | 1 GB |
| Cron and uptime monitors | 1 each | 1 each |
| Retention (lookback) | 30 days | Up to 90 days |
| Alerts | Email only | Integrations included |
| Third-party integrations, API | Not included | Included |

Consequences for Penombra:
- 1 user is enough for a solo project.
- No third-party integrations on free. A GitHub issue link from a Sentry issue is not available. The alert reaches email. The trace from alert to fix must then go through a manual issue and commit reference.
- 5,000 errors per month is far above a demo's expected load. A noisy bug can burn it in hours. Sampling and filters are the guard.

## 2. One project or two

- Sentry's docs give "separate projects for your API server and frontend client" as the example layout. Source: https://docs.sentry.io/product/projects/ (checked 26 Nov 2026).
- The free plan allows unlimited projects, so two projects cost nothing extra. Quotas are per organisation.
- The page does not say how traces link across projects. Distributed tracing across projects is a Sentry feature, but this research did not confirm it from a primary page. Verify during setup.

Recommendation within Sentry: two projects, `penombra-web` and `penombra-api`.

### SDK fit

- **React app.** `@sentry/react` ships `tanstackRouterBrowserTracingIntegration(router)`. It creates `pageload` and `navigation` transactions from TanStack Router routes. Needs `@tanstack/react-router` 1.64.0 or later. Source: https://docs.sentry.io/platforms/javascript/guides/react/features/tanstack-router/ (checked 26 Nov 2026).
- **Node API.** `@sentry/node` needs Node 20.19.0 or later (22.12+ on Node 22). Setup: an `instrument.mjs` file loaded with `node --import`. Framework guides exist for Express, Fastify and Hono, the 3 candidates in ADR 0004. Source: https://docs.sentry.io/platforms/javascript/guides/node/ (checked 26 Nov 2026).
- **OpenTelemetry.** The Sentry Node SDK "creates and sends spans without an OpenTelemetry pipeline" by default. It can also capture spans from OpenTelemetry APIs or join an existing OpenTelemetry pipeline. Source: https://docs.sentry.io/platforms/javascript/guides/node/opentelemetry/ (checked 26 Nov 2026).
- **Source maps.** Upload through the Sentry Wizard or the bundler plugin. Readable stack traces depend on it. Source: the Node guide above.

## 3. OpenTelemetry alternatives

### OpenTelemetry JavaScript status

Source: https://opentelemetry.io/docs/languages/js/ (checked 26 Nov 2026).
- Traces and metrics: Stable. Logs: Development.
- Browser: "Client instrumentation for the browser is experimental and mostly unspecified."
- Node: supports all active and maintenance LTS versions.

Consequence: OpenTelemetry fits the API well. The browser side needs a vendor SDK (Faro) or experimental packages.

OpenTelemetry has no "issue" concept. It records exceptions as `exception` span events. Grouping, alerting and issue states come from the backend you send to.

### Option B: Grafana Cloud free tier

Source: https://grafana.com/pricing/ (checked 26 Nov 2026).

| Item | Free tier |
|---|---|
| Users | 3 active per month |
| Metrics | 10,000 active series, 14-day retention |
| Logs | 50 GB per month, 14-day retention |
| Traces | 50 GB per month, 14-day retention |
| Frontend Observability | 50,000 sessions per month |
| Application Observability | 2,232 host hours per month |
| Expiry | None stated. "Always free" |

- Browser errors come from the Grafana Faro Web SDK. It collects errors, logs, real-user metrics and client traces. A Faro React package exists. Source: https://grafana.com/docs/grafana-cloud/monitor-applications/frontend-observability/ and .../instrument/ (checked 26 Nov 2026).
- Not confirmed from primary pages: source map upload, TanStack Router support, frontend-to-backend trace links. Verify before choosing.
- The API sends OpenTelemetry traces over OTLP.
- Cost: $0. Setup: more parts than Sentry (Faro, OpenTelemetry SDK, alert rules written by hand).

### Option C: SigNoz

- Self-host with Docker Compose. Parts: ClickHouse, ClickHouse Keeper, PostgreSQL 16, an OpenTelemetry Collector and the SigNoz backend. At least 4 GB of memory for Docker. Source: https://signoz.io/docs/install/docker/ (checked 26 Nov 2026).
- Exceptions view built from `exception` span events. Groups by service, type and message. Alerts on new or rising exception types. Source: https://signoz.io/docs/userguide/exceptions/ (checked 26 Nov 2026).
- SigNoz Cloud Teams plan: from $49 per month, including $49 of usage. Traces and logs $0.30 per GB, 15-day retention. No free cloud tier stated. Source: https://signoz.io/pricing/ (checked 26 Nov 2026).
- Cost: a 4 GB server, or $49 per month. Browser errors still depend on experimental OpenTelemetry browser packages.

### Option D: GlitchTip (Sentry-compatible, not OpenTelemetry)

- Works with Sentry client SDKs. Features: error tracking, performance, uptime, logs. Source: https://glitchtip.com/ (checked 26 Nov 2026).
- Hosted free tier: 1,000 events per month, 30-day retention. Small plan: $15 per month for 100,000 events. Source: https://glitchtip.com/pricing (checked 26 Nov 2026).
- Self-host: PostgreSQL 14+ required, Valkey or Redis optional. 512 MB RAM recommended, 256 MB minimum. Source: https://glitchtip.com/documentation/install (checked 26 Nov 2026).
- Penombra already runs PostgreSQL (ADR 0002). GlitchTip could share the server.
- Not confirmed: source maps and session replay support.

## 4. Comparison for S11

| | A. Sentry free | B. Grafana Cloud free | C. SigNoz self-host | D. GlitchTip |
|---|---|---|---|---|
| Monthly cost | $0 | $0 | Server with 4 GB+ | $0 (1,000 events) or self-host |
| Error budget | 5,000 errors | 50 GB traces, 50,000 sessions | Disk-bound | 1,000 events hosted |
| React SDK | Official, TanStack Router integration | Faro React | Experimental OpenTelemetry | Sentry SDKs |
| Node SDK | Official | OpenTelemetry (stable) | OpenTelemetry (stable) | Sentry SDKs |
| Issue grouping and states | Built in | Build with queries and alerts | Exceptions view | Built in |
| Alert channel on free | Email only | Grafana alerting | SigNoz alerts | Not confirmed |
| Retention | 30 days | 14 days | Self-set | 30 days |
| Parts to run | 0 | 0 | 5 containers | 0 hosted, 2 self-hosted |
| Vendor lock-in | Sentry SDK | Low (OpenTelemetry), Faro on browser | Low | Sentry SDK protocol |

## Trade-offs

- **Shortest path to S11: Sentry free (A).** 2 SDK installs, a source map upload, an email alert. Issue grouping and stack traces work without extra setup. Cost: vendor SDK, email-only alerts, no GitHub integration on free.
- **Most portable: OpenTelemetry on the API with Grafana Cloud (B).** The API code stays vendor-neutral. Cost: more setup, browser side tied to Faro, 14-day retention, error grouping is weaker than an issue tracker.
- **Hybrid.** Sentry for errors on both sides, OpenTelemetry tracing on the API later. Sentry's Node SDK can read OpenTelemetry spans. This keeps S11 short and leaves a path to OpenTelemetry.
- **Self-host (C or D)** adds a service to run and monitor. That conflicts with the one-click demo goal only if the monitor shares the demo's failure modes.

The human decides. Both A and the hybrid match the "Sentry (or OpenTelemetry)" row in `CONTEXT.md`.

## Not verified

- Distributed trace links across 2 Sentry projects on the free plan.
- Faro: source maps, TanStack Router support, trace links to the backend.
- GlitchTip: source maps, replay, alert channels.
- Whether Grafana Cloud free alerting has its own limits.
- SigNoz Cloud free trial terms.
