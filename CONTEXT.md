# Penombra: context for a new session

Read this file first. Then read `plan.md`. Written 12 November 2026.

## What this is

Penombra is a visual catalogue of synthwave and darkwave, built on MusicBrainz data. Fans browse by tag, year, country and label. They keep public or private lists. Claude can query the catalogue and the user's lists through an MCP server.

Penombra is Catalan for half-light. The word fits both genres: sunset and night.

**The app must be demoable in one click, with no account, no hardware and no external service.**

## Product

### Scope in
1. Guest browsing with no account.
2. Cover grid and dense table. Filters: tag, year, country, label. Live counts.
3. Release timeline by year, split by sub-genre.
4. Artist pages: releases, tags, band members and side projects where present, links to Bandcamp, Discogs and Spotify.
5. Lists: public or private. Manual add (for example "Owned", "Want to listen", "Favourite darkwave albums"). Public share pages. Optional link on each entry.
6. List analytics: decade, label, country, tag mix. Compare two lists.
7. MCP server with user-scoped tools.
8. Sign up, sign in, delete account.

### Scope out (with reasons)
- **Credits explorer.** Data check: 1 of 26 sampled releases had a producer or mixer credit.
- **Imports from Plex, Jellyfin or Bandcamp.** Matching messy libraries costs about a third of the build. It also limits users to those with the services. Lists are manual.
- **Wider genre scope.** Synthwave, darkwave and coldwave stay the core. A wider catalogue loses its identity.
- **Real-time, comments, follows, recommendations, native apps, audio playback.**

### A user flow (the story the demo must support)
Anna, a darkwave fan, opens the link and clicks "Try as guest". She filters the table by year and country, opens an artist, and sees releases, tags and a Bandcamp link. She adds records to a list called "Night drive 2". She signs up to keep it and makes it public. She shares the page. Later she connects Claude and asks: "Which labels appear most in my Favourites list?" Claude calls the MCP tools and answers from her data.

### Considered and rejected
- **Listening-history analytics** (ListenBrainz, Last.fm, Spotify exports). Needs accounts or files. A visitor cannot try it in one click.
- **Collaborative mixtape builder.** Drifts toward real-time and conflict-free replicated data type (CRDT) work.
- **A clone of record.club.** Reads as unoriginal, and the social features are mostly create, read, update, delete (CRUD).
- **Recommender.** Out of scope.

## Data facts

Measured on 11 November 2026. Full detail in `data-check/README.md`.

| Fact | Result |
|---|---|
| Core tags | up to about 2,450 artists and 18,000 release groups |
| Estimated size | under 1M rows (rough, 18 artists) |
| Date present | 26 of 26 releases |
| Country present | 24 of 26 |
| Real label | 13 of 26 (synthwave 2 of 10) |
| Person credit | 1 of 26 |
| Artist-level Bandcamp link | 54 of 69 (78%) |
| Release-level Bandcamp link | 24 of 69 (35%) |
| Cover art | 127 of 136 (93%) |
| Artist-to-artist relationships | 11 of 26, mostly band membership |

Consequences:
- The catalogue is small. Run a **labelled synthetic stress test** (5M or more generated rows) to get a performance claim. Never present synthetic numbers as real data.
- Show a "Buy" link only when a Bandcamp URL exists. Otherwise offer a Bandcamp search link, labelled as a search. Let users attach their own link to a list entry.
- Plan a fallback tile for the 7 to 10% of releases without cover art.
- The true tail is unmeasured. The search API rejects offsets of 500 and above. Exact counts need the data dumps.

## Decisions and reasons

Every hard-to-reverse decision gets an ADR in `docs/adr/`. Each states the trade-off and a revisit trigger.

| Decision | Chosen | Rejected | Reason and cost |
|---|---|---|---|
| Data source | Own PostgreSQL loaded from MusicBrainz dumps | Live MusicBrainz API | API allows about 1 request per second. Own copy costs hosting and refresh work |
| Scope | Core genre tags only | Wider electronic scope | Stronger identity. Smaller data, so a labelled stress test |
| Frontend | Single-page app: React, TanStack Router, TanStack Query, Tailwind, TypeScript | Next.js; TanStack Start | See below |
| API | Separate TypeScript service, REST | GraphQL; framework server functions | Clear separation of backend. Simpler to cache and test |
| Database | PostgreSQL, full-text search plus trigram | Dedicated search engine | One less service. Revisit at a size to name after measuring |
| Auth | Server sessions in cookies; OAuth for MCP | Tokens in browser storage | Easier to revoke. Needs CSRF protection |
| Privacy | Private lists by default, no comments | Social features | No moderation burden |
| Charts | Always ship a table alternative | Charts only | Accessibility. More code |
| Testing | Vitest for logic, Playwright for flows | Cypress, Jest | Fast unit runs, real-browser flow tests |
| CI/CD | GitHub Actions | Other CI | Lives next to the repo |
| Errors | Sentry (or OpenTelemetry) | None | Errors traced from alert to fix |
| Hosting and domain | Undecided. Default: a subdomain of `menor.pro` | Custom domain | A custom domain is optional |

### Why not Next.js
- Server rendering only helps link previews and indexing here.
- Known complaints: caching rules that changed between versions, and the server component mental model. These come from memory, so check current docs before repeating them in public.

### Why not TanStack Start (yet)
- Researched 11 November 2026: Start 1.0 was declared stable on 13 October 2026. It is built on TanStack Router and needs Vite 8 or newer. React Server Components are experimental.
- It adds a Node server to run and secure. A server-function XSS vulnerability was fixed in a Vite 7-era release, which shows server functions are an attack surface.
- Server rendering only helps link previews and indexing here.
- If link previews for shared lists matter, add one small server route on the API that returns HTML with meta tags. About 50 lines.
- Migration path from Router to Start should exist but is unverified. Check the docs if it comes up.
- No install size or bundle measurement was done. If revisited, scaffold an empty app and record `node_modules` size, gzipped bundle and build time.

### Why TanStack Router
- Typed URL search parameters fit the faceted filters.
- Pairs with TanStack Query.

## Working rules

- Short sentences. Under 15 words where possible. Numbers instead of adjectives. No adverbs.
- Define success criteria before implementing. Verify against them.
- Present trade-offs before choosing when options exist.
- Write tests first where it makes sense.
- Watch for abstraction bloat, dead code and silent assumptions.
- Label estimates, samples and synthetic data everywhere, including the README.
- Capture evidence when it happens: query plans before and after, Lighthouse and bundle reports, axe reports, error traces, MCP eval output, dated decision notes.
- Respect MusicBrainz: about 1 request per second, a real User-Agent, and licence terms.
- Do not send personal details, such as an email address, in request headers.

## What to do first

Phase 0 in `plan.md`:
1. Confirm the MusicBrainz data licence and Cover Art Archive terms for a public site.
2. Choose: Node framework (Hono, Express or Fastify), database access library, hosting provider, MCP SDK.
3. Write the first five ADRs in `docs/adr/`.

Then Phase 1: the walking skeleton. Deployed, with CI and error tracking, before any feature.

## Things not verified

- MusicBrainz and Cover Art Archive licence and usage terms.
- Domain availability beyond a registry lookup: `.org`, `.club` and `.cat` looked free. `.fm`, `.co` and `.es` were not checkable. Handles `penombra` on GitHub, Bluesky and Instagram are taken, and `.com`, `.app`, `.dev`, `.net`, `.xyz`, `.studio` and `.io` are registered.
- The data size estimate and the tail coverage.
- Claims about Next.js complaints and TanStack Start maturity beyond the sources listed below.
- The 5 to 6 week estimate in `plan.md`. It is a guess from phase counts.
- Whether the Catalan meaning and phrasing are natural.

## Files in this folder

| File | Purpose |
|---|---|
| `CLAUDE.md` | Loads this context in a new session |
| `CONTEXT.md` | This file |
| `plan.md` | Success criteria S1 to S15, build phases 0 to 8, open items |
| `data-check/` | Sampling scripts, raw JSON, README with results and limits |
| `docs/adr/` | Architecture decision records |
| `docs/plans/` | One folder per plan, created with `/yo-create-plan` |
| `.agents/skills/` | Agent skills for plans, commits and pull requests |

## Sources

- TanStack Start 1.0: https://tanstack.com/blog/tanstack-start-1-0
- TanStack Start overview: https://tanstack.com/start/latest/docs/framework/react/overview
- Record Club (reviewed, not cloned): https://record.club/
- MusicBrainz API: https://musicbrainz.org/doc/MusicBrainz_API
- Cover Art Archive: https://coverartarchive.org
