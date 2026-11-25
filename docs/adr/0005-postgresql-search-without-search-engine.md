---
status: accepted
date: 2026-11-25
---

# PostgreSQL full-text and trigram search, no search engine

Search runs in PostgreSQL with full-text search plus trigram indexes. We chose this because the catalogue is small, up to about 18,000 release groups by tag counts, and one less service means less to host, sync and secure. The cost: weaker typo tolerance and ranking than a dedicated engine.

## Considered options

- **A dedicated search engine** (Meilisearch, Typesense, Elasticsearch). Rejected for now: a second store to keep in sync with the import.

## Consequences

- Success criterion S3 sets search p95 under 200 ms on the real data. Record it before and after indexing.
- Revisit if S3 fails after indexing, at a catalogue size to name once Phase 3 measures it.
