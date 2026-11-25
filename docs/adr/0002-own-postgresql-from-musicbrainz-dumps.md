---
status: accepted
date: 2026-11-25
---

# Own PostgreSQL copy loaded from MusicBrainz dumps

The catalogue lives in Penombra's own PostgreSQL database, loaded from the MusicBrainz data dumps and cut down to items with a core tag. We chose this because the MusicBrainz API allows about 1 request per second, which cannot serve live filters and counts, and because its search API rejects offsets of 500 and above, so exact counts need the dumps anyway. The cost: we host the data and rerun the import to refresh it.

## Considered options

- **Live MusicBrainz API.** Rejected: about 1 request per second, no faceted counts, and the offset limit hides the long tail.
- **API with a cache in front.** Rejected: the first visit to each page still waits on the rate limit, and counts across the catalogue stay out of reach.

## Consequences

- The import script must be repeatable. Phase 2 of `plan.md` builds it.
- The catalogue is a snapshot. Pages should show the dump date.
- Tags come from `mbdump-derived`, which is CC BY-NC-SA 3.0, not CC0. See ADR 0007.
- Revisit if the dumps stop being published or their licence rules out a public copy.
