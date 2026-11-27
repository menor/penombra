---
status: accepted
date: 2026-11-27
---

# Kysely on `pg`, with plain SQL migrations

The API queries PostgreSQL with Kysely 0.29 (`kysely@^0.29`) on the `pg` driver, through Kysely's built-in `PostgresDialect`. Kysely runs only in the API process. Migrations are plain `.sql` files, one change each. Kysely's `Migrator` runs them from a `pnpm db:migrate` script, through a loader of about 15 lines that reads each file. We chose Kysely because its builder reads like the SQL it sends. Its `.explain()` captures the query plan of the exact query the API runs, which S3 needs. Its conditional `where` calls build the catalogue filters with checked table and column names. Options and sources: [research note](https://github.com/menor/penombra/blob/research/database-access/research/database-access.md).

Search and bulk loading carried no weight. No candidate models pg_trgm, so trigram and full-text queries are `sql` fragments in every option. No candidate runs `COPY`, so the import uses a driver or `psql` directly. Bundle size carried no weight either: the code lives in the API, not the browser (ADR 0004).

## Considered options

- **Drizzle 0.45.** Rejected: version 1.0 is a release candidate with breaking driver changes, so an early rewrite was likely. It has no `EXPLAIN` helper, with requests #2498 and #6128 still open. Its strengths are one TypeScript schema for types and indexes, compile errors as soon as the schema changes, generated migrations, and a short nested-query API.
- **Prisma 7.** Rejected: the schema cannot declare expression indexes, so the full-text index sits outside it. Full-text search and TypedSQL are preview features. npm `latest` points at a release candidate.
- **A raw driver alone.** Rejected: no migration runner and no checked types. Optional filters become nested SQL fragments, and a misspelled column fails only at runtime.
- **postgres.js as the driver.** Deferred: it has `COPY` built in, but its 4.0 rewrite of the pool and protocol shipped on 29 October 2026. It needs the `kysely-postgres-js` package and a hand-added Sentry wrapper (SDK 10.41.0 or later). Only the import needs `COPY`, and Phase 2 picks the import's tool.
- **Kysely TypeScript migrations.** Rejected: the SQL sits inside TypeScript, and old files import Kysely, so a breaking Kysely change can break them. Plain `.sql` files read as evidence, run in `psql`, and survive a library switch.
- **Our own migration runner.** Rejected: 30 to 50 lines of tracking and locking code to write and test. `Migrator` provides both.

## Consequences

- Migrations go forward only, with no `down` files. A bad migration is fixed by a new one or by restoring the nightly backup (ADR 0008).
- Phase 1 checks that `pg` runs a multi-statement migration file as one query. If it does not, the loader splits the file.
- `kysely-codegen` writes the database types, and the file is committed. CI runs every migration on an empty database, regenerates the file and fails on a diff. Types written by hand are not allowed.
- Zod stays at the API edges (ADR 0009). It checks input and is not a source of database types.
- No library adds the owner check that S12 needs on private lists. Every list query filters on the owner.
- `kysely-codegen` last shipped in February 2026. `kysely-ctl` is not used, because it does not support Kysely 0.30 yet.
- Revisit if Kysely stops shipping releases for 6 months, if `kysely-codegen` cannot read the schema, or if the multi-statement check fails and splitting files becomes fragile.
