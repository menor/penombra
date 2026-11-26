# Research: database access libraries for PostgreSQL

Ticket: #40. Checked 26 November 2026. Every source below was read on that date.

## Question

Which library should the API service (ADR 0004) use to reach PostgreSQL?
Candidates: Drizzle ORM, Kysely, Prisma, or a raw driver (postgres.js or node-postgres).
Criteria: raw SQL, pg_trgm and GIN indexes, full-text search, migrations, type safety, `EXPLAIN ANALYZE` capture for S3, `COPY` bulk loading for the import, bundle and cold-start cost, maintenance.

## Short answer

- Every candidate can run raw SQL. None models pg_trgm natively. Trigram and full-text indexes end up partly hand-written everywhere.
- Only Kysely has a built-in `.explain()` on its query builders. The rest need a raw `EXPLAIN` call.
- No query builder or ORM does `COPY`. The import uses the driver directly in every option. postgres.js has `COPY` built in; node-postgres needs `pg-copy-streams`.
- Prisma has the most gaps for this app: no expression indexes, preview-only full-text search and TypedSQL, and an npm `latest` tag that points at a release candidate.
- The real choice is between Drizzle (schema in TypeScript, generated migrations) and Kysely (SQL-shaped builder, hand-written migrations). Trade-offs are below. The human decides.

## Versions and maintenance

Source for versions: the npm registry (`https://registry.npmjs.org/<package>`). Source for repo data: GitHub API (`https://api.github.com/repos/<owner>/<repo>`). Both checked 26 Nov 2026.

| Package | Latest stable | Released | Pre-release in flight | Repo stars | Open issues + PRs | Last push | Licence |
|---|---|---|---|---|---|---|---|
| `drizzle-orm` | 0.45.4 | 8 Oct 2026 | 1.0.0-rc.6 (20 Nov 2026) | 36,394 | 2,086 | 25 Nov 2026 | Apache-2.0 |
| `drizzle-kit` | 0.31.11 | 21 Sep 2026 | 1.0.0-rc.6 | (same repo) | | | |
| `kysely` | 0.29.9 | 12 Nov 2026 | 0.30.0-beta.2 | 14,383 | 224 | 24 Nov 2026 | MIT |
| `@prisma/client` | 7.10.1 | 15 Oct 2026 | 8.0.0-rc.35 (23 Nov 2026) | 47,775 | 2,732 | 26 Nov 2026 | Apache-2.0 |
| `postgres` (postgres.js) | 4.1.1 | 11 Nov 2026 | none | 8,769 | 15 | 23 Nov 2026 | Unlicense |
| `pg` (node-postgres) | 8.23.1 | 30 Sep 2026 | none | 13,243 | 596 | 23 Oct 2026 | MIT |
| `pg-copy-streams` | 7.0.0 | 27 May 2025 | none | | | | |

Notes:
- Prisma's npm `latest` dist-tag points at `8.0.0-rc.35`. The newest stable is 7.10.1 (tag `prev`). A plain `pnpm add prisma` would install a release candidate. Source: https://registry.npmjs.org/prisma
- Drizzle is pre-1.0 on stable. A 1.0 release candidate shipped 20 Nov 2026 with breaking changes to driver decoding, including for `postgres-js`. Source: https://github.com/drizzle-team/drizzle-orm/releases/tag/v1.0.0-rc.6
- The Drizzle docs already describe 1.0 APIs in places, for example `getColumns` "(1.0.0-beta.2+; `getTableColumns` on pre-1 versions)". Source: https://orm.drizzle.team/docs/guides/postgresql-full-text-search
- postgres.js 4.0.0 shipped 29 Oct 2026. It rewrote the pool, connection and protocol layers. It now needs Node.js 20 or later and is ESM only. Parameter types are decided by the server by default (`infer: false`). Source: https://github.com/porsager/postgres/releases/tag/v4.0.0
- Kysely is pre-1.0 too, but ships patch releases on two lines (0.29.9 and 0.28.20 on 12 Nov 2026). Source: https://github.com/kysely-org/kysely/releases
- `pg-copy-streams` has had no release for 18 months. Source: https://registry.npmjs.org/pg-copy-streams

## Comparison by criterion

### Raw SQL

| Library | How | Safety note |
|---|---|---|
| Drizzle | `` db.execute(sql`...`) ``. `${value}` becomes `$1`. `sql<T>` sets a type; `.mapWith()` converts at runtime. `sql.raw()` inserts text unescaped | `sql<T>` "is purely a helper": not checked at runtime |
| Kysely | `` sql<Row>`...`.execute(db) ``, or `sql` fragments inside builder queries. `eb.ref('col')` checks a column name against the schema type. `sql.raw` inserts text unescaped | `sql<T>` "does not verify the SQL ... or convert the returned value" |
| Prisma | `` $queryRaw`...` `` or `Prisma.sql`. `$queryRawUnsafe` for strings. TypedSQL types `.sql` files | `$queryRaw` returns `unknown` unless given a generic. TypedSQL is preview |
| postgres.js | `` sql`...` `` is the whole API. Fragments nest. `sql.unsafe` for strings | `sql<User[]>` is a cast, not a check |
| node-postgres | `client.query(text, values)`. Types from `@types/pg` | Generic result type is a cast |

Sources:
- Drizzle: https://orm.drizzle.team/docs/sql
- Kysely: https://kysely.dev/docs/recipes/raw-sql
- Prisma raw: https://www.prisma.io/docs/orm/prisma-client/using-raw-sql/raw-queries
- Prisma TypedSQL: https://www.prisma.io/docs/orm/prisma-client/using-raw-sql/typedsql
- postgres.js README: https://github.com/porsager/postgres (sections "Dynamic queries", "Unsafe raw string queries", "TypeScript support")

### pg_trgm and GIN indexes

PostgreSQL facts (docs for PostgreSQL 19, https://www.postgresql.org/docs/current/pgtrgm.html):
- pg_trgm is a trusted extension. A non-superuser with `CREATE` on the database can install it. This matters on managed hosting.
- GIN (`gin_trgm_ops`) and GiST (`gist_trgm_ops`) both speed up `%`, `LIKE`, `ILIKE`, `~` and `~*`.
- Only GiST serves distance-ordered queries (`ORDER BY t <-> 'word' LIMIT 10`). GIN cannot.
- `pg_trgm.similarity_threshold` defaults to 0.3.

Library support:
- **Drizzle**: `index('name').using('gin', table.title.op('gin_trgm_ops'))` follows the documented `.using()` and `.op()` pattern. The docs show `.op('text_ops')` and expression indexes with `sql`, but no trigram example. The extension itself is not modelled: "There is no specific code to create an extension inside the Drizzle schema." `CREATE EXTENSION pg_trgm` goes in a custom migration (`drizzle-kit generate --custom`). Sources: https://orm.drizzle.team/docs/indexes-constraints, https://orm.drizzle.team/docs/extensions/pg, https://orm.drizzle.team/docs/kit-custom-migrations
- **Kysely**: no schema model. Indexes and the extension are written in migrations, with `db.schema.createIndex(...)` or `sql`. Source: https://kysely.dev/docs/migrations
- **Prisma**: `@@index(..., type: Gin)` is supported. `gin_trgm_ops` is not in the documented operator class list; `ops: raw("...")` passes unknown classes "without validation". Expression indexes are "not yet supported", so `GIN (lower(title) gin_trgm_ops)` or `GIN (to_tsvector(...))` cannot live in the schema. Source: https://www.prisma.io/docs/orm/prisma-schema/data-model/indexes
- **Raw drivers**: plain SQL migrations. No limits, no help.

### Full-text search

- **Drizzle**: no `tsvector` column type ("Drizzle doesn't support `tsvector` type natively"). Write `to_tsvector`, `@@`, `websearch_to_tsquery` and `ts_rank` in `sql`. GIN expression index is declarable: `.using('gin', sql`to_tsvector('english', ${table.title})`)`. Source: https://orm.drizzle.team/docs/guides/postgresql-full-text-search
- **Kysely**: `sql` fragments inside the builder. No dedicated helpers in the docs.
- **Prisma**: `search` filter behind the `fullTextSearchPostgres` preview flag. The page does not say whether it uses an index. Since the schema cannot declare a `to_tsvector` expression index, that index must be added by hand in the migration SQL. Sources: https://www.prisma.io/docs/orm/prisma-client/queries/full-text-search, https://www.prisma.io/docs/orm/prisma-schema/data-model/indexes
- **Raw drivers**: plain SQL.

### Migrations

| Library | Model | Notes |
|---|---|---|
| Drizzle | Schema in TypeScript. `drizzle-kit generate` diffs it and writes SQL files. `migrate` applies them. Also `push`, `pull`, `export`, and `--custom` empty files | Hand-written SQL covers what the kit cannot express. Source: https://orm.drizzle.team/docs/migrations |
| Kysely | Hand-written `up` and `down` in TypeScript. Run by `Migrator`, tracked in `kysely_migration`, with a database lock. CLI `kysely-ctl` is separate | No schema diffing. Source: https://kysely.dev/docs/migrations |
| Prisma | Schema in `schema.prisma`. `migrate dev` generates SQL. `--create-only` lets you edit it first | Custom SQL "must be written by hand". The docs do not say how hand-added indexes interact with later diffs. Source: https://www.prisma.io/docs/orm/prisma-migrate/workflows/customizing-migrations |
| Raw drivers | None built in | Needs a separate tool or a small script |

### Type safety

- **Drizzle**: types come from the TypeScript schema. No codegen step and no database connection at build time.
- **Kysely**: needs a `Database` interface, written by hand or generated. Generators named in the docs: `kysely-codegen` (introspects a live database), `kysely-typegen`, `prisma-kysely`, `kanel-kysely`. Source: https://kysely.dev/docs/generating-types
- **Prisma**: generated client. In Prisma 7 the generator `output` is required and the client is no longer written into `node_modules`. TypedSQL "requires an active database connection" at generate time. Sources: https://www.prisma.io/docs/orm/more/upgrade-guides/upgrading-versions/upgrading-to-prisma-7, https://www.prisma.io/docs/orm/prisma-client/using-raw-sql/typedsql
- **Raw drivers**: result types are casts. Nothing checks them against the database.

In all three query layers, any `sql` fragment is typed by assertion only. The trigram and full-text queries that S3 measures will be in such fragments.

### EXPLAIN ANALYZE capture for S3

PostgreSQL facts (https://www.postgresql.org/docs/current/sql-explain.html):
- `ANALYZE` runs the statement. Wrap writes in `BEGIN ... ROLLBACK`.
- `BUFFERS` is on by default with `ANALYZE`. `SUMMARY` too.
- `FORMAT JSON` gives machine-readable plans, suitable for committing as evidence.

Library support:
- **Kysely**: built in. `.explain('json', sql`analyze`)` produces `explain (analyze, format json) select ...`. Available on select, insert, update and delete builders. Source: https://kysely-org.github.io/kysely-apidoc/interfaces/Explainable.html
- **Drizzle**: not built in. Feature requests #2498 (open since 12 Jun 2024) and #6128 (open since 12 Aug 2026). Workaround from #6128: take `.toSQL()`, then run `EXPLAIN` with `sql.raw` and pass the parameters again. Sources: https://github.com/drizzle-team/drizzle-orm/issues/2498, https://github.com/drizzle-team/drizzle-orm/issues/6128
- **Prisma**: no helper. Run `EXPLAIN` through `$queryRaw`. Source: https://www.prisma.io/docs/orm/prisma-client/using-raw-sql/raw-queries
- **Raw drivers**: prefix the SQL text. postgres.js `.describe()` exposes the final query string. Source: https://github.com/porsager/postgres

A small `explain(query)` helper is about 10 lines in any option. Kysely saves writing it.

### Bulk loading with COPY

PostgreSQL facts:
- `COPY` "is optimized for loading large numbers of rows". Load first, then create indexes, raise `maintenance_work_mem` for the index builds, then `ANALYZE`. Source: https://www.postgresql.org/docs/current/populate.html
- `COPY FROM STDIN` streams over the client connection and needs only `INSERT` on the table. `COPY FROM 'file'` needs superuser or `pg_read_server_files`, which managed hosts may not grant. Text format defaults: tab delimiter, `\N` for null. `FREEZE` helps a first load into a table created or truncated in the same transaction. Source: https://www.postgresql.org/docs/current/sql-copy.html
- The MusicBrainz dump files are in PostgreSQL copy format: the official importer reads "a regular file in Postgres 'copy' format". So the dump tables can stream into staging tables with no parsing. Source: https://github.com/metabrainz/musicbrainz-server/blob/master/admin/MBImport.pl (lines 67 to 71)

Library support:
- **postgres.js**: built in. `` await sql`copy t (a, b) from stdin`.writable() `` returns a Node.js stream. The README calls it "a low-level API which does not provide any type safety". Source: https://github.com/porsager/postgres (section "Copy to/from as Streams")
- **node-postgres**: needs `pg-copy-streams` (`client.query(copyFrom('COPY ...'))`). Its README calls the mode "very fast and very brittle". Source: https://github.com/brianc/node-pg-copy-streams
- **Drizzle, Kysely, Prisma**: no `COPY` support in their docs. Drizzle and Kysely run on top of `pg` or postgres.js, so the import script can reach the same driver. Prisma 7 also connects through a driver adapter (`@prisma/adapter-pg`), but the import would open its own driver connection anyway.

Driver pairing:
- Drizzle supports both `pg` and postgres.js natively. Source: https://orm.drizzle.team/docs/get-started-postgresql
- Kysely's core `PostgresDialect` runs on `pg`. A postgres.js dialect exists as an organisation package, `kysely-postgres-js`. Source: https://kysely.dev/docs/dialects

### Bundle and cold-start cost

- S4 (200 KB initial JavaScript) measures the frontend. ADR 0004 puts the database code in a separate API service. So the library choice does not touch S4.
- Cold start matters only if hosting is serverless. Hosting is still open (plan.md, open item 2).
- Unpacked npm sizes, latest stable, from the registry. These are install sizes, not runtime bundles. Not measured further.

| Package | Unpacked size | Runtime dependencies |
|---|---|---|
| `pg` | 0.1 MB | 6 (`pg-pool`, `pg-protocol`, `pg-types`, and 3 more) |
| `postgres` | 0.3 MB | 0 |
| `kysely` | 1.8 MB | 0 |
| `drizzle-orm` | 10.5 MB | 0 (many entry points, one per driver) |
| `@prisma/client` | 74.5 MB | 1 |

- Prisma 7 replaced the Rust engine with a TypeScript client. The upgrade guide claims "smaller bundle size" with no figures. Source: https://www.prisma.io/docs/orm/more/upgrade-guides/upgrading-versions/upgrading-to-prisma-7
- postgres.js claims "Fastest full-featured PostgreSQL client". The README shows no benchmark. Treat as unverified.

## Trade-offs

**Drizzle with postgres.js or `pg`**
- For: schema and types in one TypeScript file. Migrations generated from it. GIN and expression indexes declarable. Largest community of the three builders.
- Against: no `EXPLAIN` helper. Stable line is 0.45, and 1.0 is in release candidate with breaking driver changes. Adopting now means either a migration soon or starting on a release candidate. 2,086 open issues and PRs.

**Kysely with `pg` (plus `pg-copy-streams` for the import)**
- For: SQL-shaped builder that stays close to the queries S3 measures. Built-in `.explain()`. 224 open issues and PRs. Steady patch releases.
- Against: hand-written migrations, no schema diffing. Types need a generator such as `kysely-codegen`, run against a live database. postgres.js is not a core dialect.

**Prisma 7**
- For: mature migrations and studio tooling. Widely known.
- Against: no expression indexes, so the full-text index sits outside the schema. Full-text search and TypedSQL are preview. Raw queries return `unknown` by default. npm `latest` is a release candidate. Largest install.

**Raw driver only (postgres.js)**
- For: one dependency, zero transitive dependencies, `COPY` built in, every query is literal SQL for the evidence write-up.
- Against: no migration tool, no schema types. Hand-written row types drift from the schema. More code per query.

## Open questions for the human

1. Schema-first (Drizzle, Prisma) or SQL-first (Kysely, raw)? This decides whether migrations are generated or written.
2. Start on Drizzle 0.45 stable, or wait for or adopt 1.0?
3. Will the import run against a host that allows `COPY FROM STDIN`? PostgreSQL requires only `INSERT` on the table for it. Provider limits were not checked.

## Not verified

- No library was installed or benchmarked. No query plans were captured.
- Drizzle's `.op('gin_trgm_ops')` and Prisma's `ops: raw("gin_trgm_ops")` are inferred from documented patterns. Neither doc shows a trigram example.
- Whether Prisma's full-text `search` filter can use a hand-made GIN index.
- Runtime bundle sizes and cold-start times.
