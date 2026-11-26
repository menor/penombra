# Penombra: success criteria and build order

Name: **Penombra**. Catalan for half-light. Chosen 12 November 2026. Drafted 11 November 2026.
Read `CONTEXT.md` first. It holds the why, the decisions, and the working rules.

## One line

A visual catalogue of synthwave and darkwave, built on MusicBrainz. Fans browse by tag, year, country and label. They keep public or private lists. Claude can query the catalogue and their lists through an MCP server.

## Scope

**In**
1. Guest browsing. No sign-up needed.
2. Cover grid and dense table. Filters: tag, year, country, label. Live counts.
3. Release timeline by year, split by core tag.
4. Artist pages: releases, tags, band members and side projects where present, links to Bandcamp, Discogs and Spotify.
5. Lists: public or private. Manual add. Public share pages. Optional link on each entry.
6. List analytics: decade, label, country, tag mix. Compare two lists.
7. MCP server with member-scoped tools.
8. Sign up, sign in, delete account.

**Out**
- Credits explorer. Data check: 1 of 26 sampled releases had a producer or mixer credit.
- Imports from Plex, Jellyfin or Bandcamp. Matching messy libraries costs about a third of the build. It also limits users to those with the services. Lists are manual.
- Wider genre scope. Synthwave, darkwave and coldwave stay the core. A wider catalogue loses its identity.
- Real-time features, comments, follows, recommendations, native apps, audio playback.

## Data facts measured on 11 November 2026

Source: MusicBrainz API samples. Scripts and raw output in `data-check/`. See `data-check/README.md`.

| Fact | Result | Sample |
|---|---|---|
| Core tags, artists | up to about 2,450 | tag search counts, overlap unknown |
| Core tags, release groups | up to about 18,000 | tag search counts |
| Estimated size | under 1M rows, roughly | 18 artists. Order of magnitude only |
| Date present | 26 of 26 releases | 26 |
| Country present | 24 of 26 | 26 |
| Label present | 13 of 26 (synthwave 2 of 10) | 26 |
| Person credit (producer, mixer) | 1 of 26 | 26 |
| Artist-level Bandcamp link | 54 of 69 (78%) | 69 |
| Release-level Bandcamp link | 24 of 69 (35%) | 69 |
| Cover art | 127 of 136 (93%) | 69 artists |
| True tail (5 or fewer release groups) | Not measured. 7 artists only | needs dump |

Known limit: the search API rejects offsets of 500 and above. Exact counts need the data dumps.

## Success criteria

Every target below is a draft. Set the final number after the first measurement.

| # | Area | Target | How to verify |
|---|---|---|---|
| S1 | Demo | Public URL. Guest sees data in 1 click. No sign-up | Open in a private window on a phone |
| S2 | Data | Core-tag subset loaded in PostgreSQL. Row counts per table in README | Count query, committed script |
| S3 | Search | p95 under 200 ms on the real catalogue | Load test script. Record before and after indexing |
| S4 | Bundle | Initial JavaScript under 200 KB gzipped | Build report in CI, fails on regression |
| S5 | Page load | Largest Contentful Paint under 2.5 s on a throttled mobile profile | Lighthouse in CI, 3-run median |
| S6 | Table | Scrolls 60 fps with 100k rows. Stress test with 5M synthetic rows documented | Browser profile. Label synthetic data as synthetic |
| S7 | Accessibility | axe: 0 serious or critical issues on 5 key pages. Keyboard-only path through search, list creation, chart view | axe in Playwright, manual run recorded |
| S8 | Charts | Every chart has a table alternative | Playwright check |
| S9 | CI/CD | Each merge runs typecheck, unit tests, Playwright, accessibility check, deploy | Badge on README |
| S10 | Tests | Playwright covers: guest browse, sign up, create list, share page, MCP call | Test run in CI |
| S11 | Observability | Sentry on frontend and API. One real or staged error traced from alert to fix, written up | Write-up in the repo |
| S12 | Security | Private lists return 404 to anyone but their owner. User text escaped. CSRF protected. Rate limit on sign in | Playwright and API tests |
| S13 | MCP | 4 to 6 tools, scoped to the signed-in member. OAuth. Eval set of 20 questions. Right tool chosen in 90% or more | Eval script in CI |
| S14 | Docs | README with architecture diagram, 90-second video, ADRs | Read by someone outside the project |
| S15 | Cost | Monthly hosting cost recorded | Invoice |

## Build order

Each phase ends with something that runs on the public URL. Do not start the next phase until the exit check passes. Every exit check also includes: the README status shows the phase now starting.

**Phase 0. Decisions (1 to 2 days)**
- ~~Confirm MusicBrainz data licence and Cover Art Archive terms for a public site.~~ Done: ADR 0007.
- Pick: database access library. ~~Node framework.~~ Done: ADR 0009. ~~MCP SDK.~~ Done: `CONTEXT.md` table. ~~Hosting provider.~~ Done: ADR 0008.
- ~~Write the first five ADRs in `docs/adr/`.~~ Done: ADRs 0001 to 0007.
- Exit: decisions written down. Name chosen.

**Phase 1. Walking skeleton (3 to 4 days)**
- Repo, TypeScript API, PostgreSQL, empty TanStack Router app, one page that reads one row.
- GitHub Actions: typecheck, test, deploy. Sentry connected.
- Exit: public URL shows a row from the database. Green badge.

**Phase 2. Data (4 to 5 days)**
- Import script: dumps in, genre subset out. Repeatable.
- Schema: artists, release groups, releases, labels, tags, links, cover art ids.
- Record true row counts. Replace the estimates in this file.
- Exit: counts match the script output. Import reruns cleanly.

**Phase 3. Catalogue UI (5 to 6 days)**
- Cover grid, dense table, filters, live counts, artist page.
- Full-text search with trigram index. Measure before and after.
- Baseline measurements for S3 to S6.
- Exit: S3 recorded. Guest can browse.

**Phase 4. Accounts and lists (4 to 5 days)**
- Sessions, sign up, sign in, delete account.
- Lists: create, add, remove, reorder, public or private, share page, optional link.
- Security tests for S12.
- Exit: S12 passes.

**Phase 5. Timeline and analytics (4 to 5 days)**
- Timeline by year and core tag. List charts. Compare two lists.
- Table alternatives for every chart.
- Exit: S8 passes.

**Phase 6. MCP (3 to 4 days)**
- Tools: search releases, get artist, list my lists, get list analytics, find gaps in a list (optional).
- OAuth. Eval set. Run in CI.
- Exit: S13 passes.

**Phase 7. Hardening (4 to 5 days)**
- Accessibility audit and fixes. Performance fixes. Stress test with synthetic rows.
- Stage and trace one error.
- Exit: S4 to S7, S11 pass. Numbers recorded.

**Phase 8. Write-up (3 to 4 days)**
- README, diagram, video, write-up.
- Exit: S14 passes.

Total: about 5 to 6 weeks of full-time work. The earlier 3 to 4 week guess assumed fewer phases. Cut order if time runs short: compare-two-lists, MCP gap tool, timeline core tag split, charts. Never cut S3, S7, S9, S11, S13.

## Open items

1. ~~Name.~~ Settled: Penombra. Handles `penombra` on GitHub, Bluesky and Instagram are taken. `.com`, `.app`, `.dev`, `.net`, `.xyz`, `.studio`, `.io` are registered. `.org`, `.club`, `.cat` looked free on 12 Nov 2026 (unconfirmed). `.fm`, `.co` and `.es` were not checkable. Custom domain is optional. Default: a subdomain of `menor.pro`.
2. ~~Hosting provider and monthly budget.~~ Settled: one OVHcloud VPS-1, cap €10 a month with VAT. See ADR 0008.
3. ~~Exact licence terms for MusicBrainz data and covers.~~ Checked 25 November 2026, see ADR 0007. Still open: whether a third-party site may show Cover Art Archive images.
4. Whether to add a Redis search cache. Only if it shows in the latency numbers.
