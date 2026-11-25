# Penombra: context for a new session

Read this file first. Then read `plan.md`. Written 12 November 2026. Shrunk 25 November 2026: scope, data facts and phases live in `plan.md`, terms in `GLOSSARY.md`, decisions in `docs/adr/`.

## What this is

Penombra is a visual catalogue of synthwave and darkwave, built on MusicBrainz data. Fans browse by tag, year, country and label. They keep public or private lists. Claude can query the catalogue and a member's lists through an MCP server.

Penombra is Catalan for half-light. The word fits both genres: sunset and night.

**The app must be demoable in one click, with no sign-up, no hardware and no external service.**

Scope in and out, with reasons: `plan.md`.

### A user flow (the story the demo must support)
Anna, a darkwave fan, opens the link and clicks "Try as guest". She filters the table by year and country, opens an artist, and sees releases, tags and a Bandcamp link. She adds release groups to a list called "Night drive 2". She signs up to keep it and makes it public. She shares the page. Later she connects Claude and asks: "Which labels appear most in my Favourites list?" Claude calls the MCP tools and answers from her data.

### Considered and rejected
- **Listening-history analytics** (ListenBrainz, Last.fm, Spotify exports). Needs accounts or files. A visitor cannot try it in one click.
- **Collaborative mixtape builder.** Drifts toward real-time and conflict-free replicated data type (CRDT) work.
- **A clone of record.club.** Reads as unoriginal, and the social features are mostly create, read, update, delete (CRUD).
- **Recommender.** Out of scope.

## Data consequences

The measured facts are in `plan.md` and `data-check/README.md`. They lead to these rules:
- The catalogue is small. Run a **labelled synthetic stress test** (5M or more generated rows) to get a performance claim. Never present synthetic numbers as real data.
- Show a "Buy" link only when a Bandcamp URL exists. Otherwise offer a Bandcamp search link, labelled as a search. Let guests and members attach an entry link to an entry.
- Plan a fallback tile for the 7 to 10% of releases without cover art.
- The true tail is unmeasured. The search API rejects offsets of 500 and above. Exact counts need the data dumps.

## Decisions without an ADR

Every hard-to-reverse decision gets an ADR in `docs/adr/`. Each states the trade-off and a revisit trigger. These decisions are easy to reverse, so they stay here:

| Decision | Chosen | Rejected | Reason and cost |
|---|---|---|---|
| Scope | Core genre tags only | Wider electronic scope | Stronger identity. Smaller data, so a labelled stress test |
| Privacy | Private lists by default, no comments | Social features | No moderation burden |
| Charts | Always ship a table alternative | Charts only | Accessibility. More code |
| Testing | Vitest for logic, Playwright for flows | Cypress, Jest | Fast unit runs, real-browser flow tests |
| CI/CD | GitHub Actions | Other CI | Lives next to the repo |
| Errors | Sentry (or OpenTelemetry) | None | Errors traced from alert to fix |
| Hosting and domain | Undecided. Default: a subdomain of `menor.pro` | Custom domain | A custom domain is optional |

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

## Things not verified

Domain availability and Cover Art Archive display rights are open items in `plan.md`.
- How often MusicBrainz publishes the data dumps.
- The data size estimate and the tail coverage.
- Claims about TanStack Start in ADR 0003 beyond the sources listed below.
- The 5 to 6 week estimate in `plan.md`. It is a guess from phase counts.
- Whether the Catalan meaning and phrasing are natural.

## Sources

- TanStack Start 1.0: https://tanstack.com/blog/tanstack-start-1-0
- TanStack Start overview: https://tanstack.com/start/latest/docs/framework/react/overview
- Record Club (reviewed, not cloned): https://record.club/
- MusicBrainz API: https://musicbrainz.org/doc/MusicBrainz_API
- MusicBrainz data licence: https://musicbrainz.org/doc/About/Data_License
- MusicBrainz core and supplementary data: https://musicbrainz.org/doc/MusicBrainz_Database
- Cover Art Archive: https://coverartarchive.org
