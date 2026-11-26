# Research: hosting options under the cost and cold-start rules

Answers issue #36. Checked on 26 November 2026. Prices change often. Recheck before buying.
This file lays out options and trade-offs. It does not pick a host.

## Constraints (from issue #34)

- The cheapest option wins.
- A paid host must also host other projects later.
- No cold start on first visit (S1, S5).
- Node on the current LTS release.
- One API process serves REST and `/mcp`.
- A static single-page app. PostgreSQL.
- A subdomain of `menor.pro` now. A custom domain later.
- Production holds the core-tag subset plus 5M synthetic rows. The import runs locally.

## Short answer

1. Every free tier that runs a Node process or PostgreSQL either sleeps, expires or is too small. Oracle Cloud Always Free is the one exception. It carries a reclaim risk.
2. The cheapest paid fit is one virtual private server (VPS) at $4.54 to €8.26 a month. It runs the API, PostgreSQL and the static files, and it can host later projects.
3. Platform hosts (Fly.io, Render, Railway) fit the rules at about $8 to $14 a month for this project alone. Each later project adds its own cost.
4. Estimated database size: 1.5 to 3 GB. That rules out the free PostgreSQL tiers of Neon, Supabase, Render and Koyeb.
5. The local import downloads about 7.7 GB of compressed dumps.

## Storage estimate (estimate, not a measurement)

Sources for sizes: PostgreSQL page layout docs, https://www.postgresql.org/docs/current/storage-page-layout.html (checked 26 Nov 2026). Page 8,192 bytes. Page header 24 bytes. Line pointer 4 bytes per row. Row header 23 bytes, padded to 24.

### Core-tag subset

`data-check/README.md` estimates under 1M rows in total. That is an order of magnitude from 18 artists.

- Assume 1M rows at 150 bytes each (28 bytes overhead plus about 120 bytes of data).
- Heap: 1M × 150 B = 150 MB.
- Indexes: assume 1× to 2× the heap = 150 to 300 MB.
- Subset total: **0.3 to 0.45 GB**.

### 5M synthetic rows

Assume release-group-shaped rows: 8-byte id, 25-byte title, year, country, label id, timestamps.

- Row: 28 B overhead + about 110 B data = about 140 B.
- Heap: 5M × 140 B = **700 MB**.
- Primary key B-tree: about 20 B per entry × 5M = 100 MB.
- 3 more B-trees (year, country, label): 3 × 100 MB = 300 MB.
- Trigram GIN index on title: titles are 5M × 25 B = 125 MB of text. Assume 1× to 3× = 125 to 375 MB.
- Tag join table: 5M × 1.3 tags × 40 B = 260 MB, plus a 130 MB index.
- Synthetic total: **1.6 to 1.9 GB**.

### Total and disk to provision

- Database: 0.3 + 1.6 = 1.9 GB low, 0.45 + 1.9 = 2.35 GB high. Round to **1.5 to 3 GB** to cover error in the assumptions.
- Add write-ahead log, a vacuum margin and one local dump file: provision **about 10 GB** of disk for PostgreSQL.
- Replace these numbers with `pg_total_relation_size` output after Phase 2.

## MusicBrainz dump files (for the local import)

Source: https://data.metabrainz.org/pub/musicbrainz/data/fullexport/20261125-002239/ (checked 26 Nov 2026).

| File | Size (compressed) | Needed |
|---|---|---|
| `mbdump.tar.bz2` | 7 GB | Yes. Core data (CC0) |
| `mbdump-derived.tar.bz2` | 508 MB | Yes. Tags (CC BY-NC-SA 3.0, ADR 0007) |
| `mbdump-cover-art-archive.tar.bz2` | 164 MB | Likely. Cover art ids |
| `mbdump-edit.tar.bz2` | 16 GB | No |
| `mbdump-stats.tar.bz2` | 117 MB | No |
| `mbdump-editor.tar.bz2` | 83 MB | No |
| `mbdump-cdstubs.tar.bz2` | 61 MB | No |

- Download for the import: 7 GB + 508 MB + 164 MB = **about 7.7 GB**.
- The listing held 2 dumps: 21 November (a Saturday) and 25 November (a Wednesday). So dumps appear about twice a week, and older ones are removed from this folder. This answers an open item in `CONTEXT.md` from one observation.
- Uncompressed size is not measured. A full local MusicBrainz database is much larger than 7.7 GB. Phase 2 must measure it.

## Comparison table

Prices exclude VAT unless marked. "Fits" means the option meets the no-cold-start rule and holds about 3 GB of PostgreSQL.

| Option | Monthly cost | Spec | Cold start | PostgreSQL 3 GB | More projects | Fits |
|---|---|---|---|---|---|---|
| OVHcloud VPS-1 | $4.54 | 2 vCPU, 4 GB RAM, 40 GB NVMe | None | Yes, self-run | Yes | Yes |
| Hetzner CX23 | €5.99 | 2 vCPU, 4 GB, 40 GB, 20 TB traffic | None | Yes, self-run | Yes | Yes, but shown unavailable |
| Hetzner CPX02 (Helsinki) | €5.49 | 1 vCPU, 1 GB, 20 GB | None | Tight | Weak (1 GB RAM) | Partly |
| Netcup VPS 500 G12.5 | €8.26 (€9.50 incl. 19% VAT) | 2 vCPU, 4 GB, 64 GB, 12-month term | None | Yes, self-run | Yes | Yes |
| DigitalOcean droplet | $12 | 1 vCPU, 2 GB, 50 GB | None | Yes, self-run | Yes | Yes |
| Oracle Cloud Always Free | $0 | Arm: 2 OCPU, 12 GB total. 200 GB block storage | None, but reclaim risk | Yes, self-run | Yes | Yes, with risks below |
| Fly.io machine + Managed Postgres | $3.69 + $4 = $7.69 | 512 MB Node machine + Developer Postgres | None if auto-stop is off | Developer plan size unverified | Each project pays | Likely |
| Render web + Postgres | $7 + $6 + 3 GB × $0.30 = $13.90 | 512 MB web, 256 MB Postgres | None on paid | Yes | Each project pays | Yes |
| Railway Hobby | $5 base incl. $5 usage. Estimate $8 to $12 | Usage: $10 per GB RAM, $20 per vCPU, $0.15 per GB volume | None on Hobby | Yes | Each project pays | Yes (cost is an estimate) |
| Koyeb eco-nano + Postgres Small | $1.61 + $29.76 = $31.37 | 256 MB Node, Postgres 0.25 to 1 vCPU | None on paid | Yes | Each project pays | Yes, costly |
| Render free | $0 | Free web, 1 GB Postgres | Sleeps after 15 min, about 1 min to wake | Expires after 30 days | No | No |
| Railway free trial | $5 one-time credit, 30 days | 1 GB per service | Sleeps after 5 to 10 min | 500 MB volume cap | No | No |
| Koyeb free | $0 | 512 MB, 0.1 vCPU | Scales to zero after 1 hour | Free Postgres 1 GB, 5 hours of compute | No | No |
| Neon free | $0 | 1 GB per project, 100 compute-hours | Scales to zero after 5 min. Restart in a few hundred ms | No (1 GB) | n/a | No |
| Supabase free | $0 | 500 MB per project, 2 projects | Pauses after 7 days of inactivity | No (500 MB) | n/a | No |
| Neon Launch (paid) | $0.106 per compute-hour + $0.35 per GB | Always-on allowed | None if scale-to-zero is off | Yes | n/a | Database only. 730 h × 0.25 CU ≈ $19 + $1 storage (estimate) |
| Supabase Pro | $25 | 8 GB disk, $10 compute credit | None | Yes | n/a | Database only. Costly |
| DigitalOcean Managed PostgreSQL | $15.15 | 1 vCPU, 1 GiB, 10 GiB | None | Yes | n/a | Database only |
| Cloudflare Pages | $0 | 500 builds per month, 20,000 files, 100 custom domains | None | n/a | Yes | Static app only |
| Cloudflare Workers | $0 free, $5 paid | 10 ms CPU per request on free | Not a Node process | n/a | Yes | No: not Node LTS, not one API process |

### Notes on the table

- **Hetzner.** The Cost-Optimized page marked every plan "currently unavailable" on 26 Nov 2026. The Regular Performance page showed the same note on its create buttons. Prices include IPv4. Locations: Falkenstein, Nuremberg, Helsinki.
- **OVHcloud.** The English page listed USD prices. The EU location list did not load. Verify the EU price and region before buying.
- **Netcup.** The listed price is for a 12-month term. The 1-month price was not shown. Locations include Vienna, Nuremberg and Amsterdam.
- **DigitalOcean.** EU regions: Amsterdam, London, Frankfurt. The 4 GB plan was not in the fetched list.
- **Scaleway.** Pricing pages returned HTTP 403 to the fetch. Not compared.
- **Fly.io.** New accounts get $1 of credit. After adding a card, $5 of usage each month is free, per the pricing page. That could cut the $7.69 to about $2.69. Not verified on an invoice. Developer Postgres storage size was not stated on the page.
- **Railway.** The $8 to $12 range assumes about 0.75 GB RAM and 0.1 to 0.2 vCPU on average, plus a 3 GB volume. It is an estimate, not a quote.
- **Oracle risks.** Idle instances "may be reclaimed" when, over 7 days, 95th-percentile CPU, network and memory (Arm shapes) all stay under 20%. A low-traffic demo can meet that rule. Free shapes can also fail with "out of host capacity". Resources must stay in the home region.
- **Node LTS.** Node 26, 24 and 22 are all LTS lines on 26 Nov 2026. Every VPS, Fly.io, Render, Railway and Koyeb runs a chosen Node version through a container image or build setting. Cloudflare Workers runs its own runtime.

## Running several projects on one server

| Tool | What it is | Server needs | TLS | Databases | Backups |
|---|---|---|---|---|---|
| Coolify | Self-hosted web dashboard | 2 CPU cores, 2 GB RAM, 10 GB disk minimum. Linux, amd64 or arm64 | Through its proxy (domain page not fetched) | One-click databases | Scheduled `pg_dump` to S3-compatible storage, SFTP or WebDAV |
| Dokku | Command-line, git-push platform | 1 GB RAM (or swap). Ubuntu 22.04 to 26.04 or Debian 12 or 13 | `letsencrypt` plugin plus a renewal cron job | Official `dokku-postgres` plugin | Plugin export commands (backup page not fetched) |
| Kamal | Deploy tool run from the laptop | SSH as root. Installs Docker. Needs a container registry | kamal-proxy gets Let's Encrypt certificates per host | "Accessories" containers (page not fetched) | Not covered. You build it |

- All 3 route by host name. So `penombra.menor.pro` and a later project share one server and one IP.
- Coolify uses the most memory of the 3. Its docs warn that builds on the same server can make it unresponsive. On a 4 GB VPS this matters.
- Kamal adds a registry account and a Ruby or Docker install on the laptop.
- Plain Docker Compose with a reverse proxy such as Caddy is a 4th option. Not researched here.

## Upkeep each option needs

| Option | You own | The host owns |
|---|---|---|
| VPS (OVHcloud, Hetzner, Netcup, DigitalOcean, Oracle) | OS security updates, firewall, SSH keys, PostgreSQL upgrades and backups, disk alerts, the deploy tool's updates | Hardware, network |
| Platform host (Fly.io, Render, Railway, Koyeb) | Deploy config, app version | OS, TLS, restarts. Managed Postgres backups where the plan includes them |
| Managed PostgreSQL (Neon, Supabase, DigitalOcean) | Schema, connection limits | Backups, upgrades, failover |

For a VPS, the minimum routine is:
- Turn on unattended security updates (for example `unattended-upgrades` on Debian or Ubuntu).
- Schedule a nightly `pg_dump` to off-server storage. Test a restore once.
- Watch disk use. The import does not run on the server, so production disk stays near the 10 GB estimate.
- Keep the restore path simple: the catalogue can be rebuilt from the dumps. Only member data (lists, sessions) needs backups.

## Subdomain now, custom domain later

- **VPS.** Any DNS A record works. Add `penombra.menor.pro` now and a custom domain later. The deploy tool issues certificates for both.
- **Fly.io.** `fly certs add` plus a CNAME for a subdomain or A/AAAA for an apex. Let's Encrypt certificates are free. Source: https://docs.fly.io/networking/custom-domain/
- **Render.** Custom domains and subdomains with automatic TLS on Hobby, Pro and Scale. The page does not confirm free services. Source: https://render.com/docs/custom-domains
- **Cloudflare Pages.** 100 custom domains per project.
- **Railway, Koyeb.** Not checked in this pass.

## Trade-offs for the decision

- **One VPS ($4.54 to €8.26).** Lowest cost per project, and the cost stays flat as projects are added. Costs: OS and backup upkeep, and a single point of failure. Shows more backend and operations work.
- **Oracle Always Free ($0).** Lowest cost. Costs: reclaim and capacity risk, an Arm build, and the same upkeep as a VPS. A reclaimed server breaks the one-click demo.
- **Platform host ($8 to $14 for this project).** Least upkeep. Costs: each later project adds about the same again, and the database size limits apply.
- **Split static app.** Cloudflare Pages can serve the single-page app for free next to any API host. It adds a second deploy and cross-origin setup for sessions (ADR 0006).

## Not verified

- OVHcloud EU price and regions. Netcup 1-month price. Hetzner stock dates.
- Fly.io Developer Postgres storage and the $5 monthly free usage on a real bill.
- Whether Oracle requires a card at sign-up, and how often it reclaims idle Arm instances in practice.
- Uncompressed dump size and the real database size. Both come from Phase 2.
- Coolify's own memory use. Dokku backup commands. Kamal accessories.
- Scaleway prices.

## Sources (all checked 26 November 2026)

- Hetzner Cloud: https://www.hetzner.com/cloud, https://www.hetzner.com/cloud/cost-optimized, https://www.hetzner.com/cloud/regular-performance
- Netcup VPS: https://www.netcup.com/en/server/vps
- OVHcloud VPS: https://www.ovhcloud.com/en/vps/
- DigitalOcean: https://www.digitalocean.com/pricing/droplets, https://www.digitalocean.com/pricing/managed-databases
- Oracle Always Free: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- Fly.io: https://docs.fly.io/about/pricing, https://docs.fly.io/networking/custom-domain/
- Render: https://render.com/pricing, https://render.com/docs/free, https://render.com/docs/custom-domains
- Railway: https://railway.com/pricing
- Koyeb: https://www.koyeb.com/pricing, https://www.koyeb.com/docs/reference/instances, https://www.koyeb.com/docs/faqs/pricing
- Neon: https://neon.com/pricing
- Supabase: https://supabase.com/pricing
- Cloudflare: https://developers.cloudflare.com/workers/platform/pricing/, https://developers.cloudflare.com/pages/platform/limits/
- Coolify: https://coolify.io/docs/get-started/installation, https://coolify.io/docs/databases/backups
- Dokku: https://dokku.com/docs/getting-started/installation/, https://dokku.com/docs/deployment/application-deployment/
- Kamal: https://kamal-deploy.org/docs/installation/, https://kamal-deploy.org/docs/configuration/proxy/
- Node.js releases: https://nodejs.org/en/about/previous-releases
- PostgreSQL page layout: https://www.postgresql.org/docs/current/storage-page-layout.html
- MusicBrainz dumps: https://data.metabrainz.org/pub/musicbrainz/data/fullexport/
