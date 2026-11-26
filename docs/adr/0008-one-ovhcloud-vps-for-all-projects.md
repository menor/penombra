---
status: accepted
date: 2026-11-26
---

# One OVHcloud VPS for Penombra and later projects

Penombra runs on one OVHcloud VPS-1 in Germany: 2 vCores, 4 GB RAM, 40 GB NVMe, billed monthly at €4.49 (€5.34 with 19% VAT). The same server runs the API, PostgreSQL and the static single-page app, all on one origin, `penombra.menor.pro`. Later projects share the server. The monthly cap is €10 including VAT for everything on it. Prices checked on 26 November 2026 in the OVHcloud public catalogue. Options and sources: [research note](https://github.com/menor/penombra/blob/research/hosting/research/hosting.md).

- **Backups.** A nightly `pg_dump` goes to OVHcloud Object Storage in another region, such as Gravelines, at about €0.0073 per GB per month. Only member data needs it: the import rebuilds the catalogue from the dumps. No paid VPS backup.
- **Upkeep.** Unattended security updates, a firewall, SSH keys only, disk alerts. One restore is tested in Phase 1.
- **Deploy tool.** Not decided here. Phase 1 picks one of Docker Compose with Caddy, Dokku, Coolify or Kamal. It is easy to reverse.

## Considered options

- **Hetzner CX23** (€5.99 with IPv4). Rejected: not orderable in any location. Hetzner's status page has listed "Limited availability of cloud instances" since 26 June 2026, with no end date. The cheapest orderable 4 GB plan, CPX22, costs €16.99.
- **Oracle Cloud Always Free.** Rejected: Oracle may reclaim instances under 20% load over 7 days. A quiet demo meets that rule, and a reclaimed server breaks the one-click demo (S1).
- **Platform hosts** (Fly.io, Render, Railway). Rejected: $8 to $14 a month for Penombra alone, and each later project adds about the same.
- **Free tiers** (Render, Railway, Koyeb, Neon, Supabase). Rejected: they sleep, expire or hold less than the 1.5 to 3 GB database estimate.
- **Static app on Cloudflare Pages.** Rejected: it needs cross-origin requests with credentials, which risk an origin-reflection bug. `SameSite` cookies stop protecting against other `*.menor.pro` subdomains. The app and the API deploy separately. The speed gain is small for EU visitors.
- **12 months paid upfront** (€3.81 a month). Deferred: it saves €8.16 a year but locks the choice in before Phase 1 tests the server.

## Consequences

- One server is a single point of failure. A server outage takes the demo down.
- OS, PostgreSQL and backup upkeep is Penombra's work, not the host's.
- Each visitor's requests reach one EU location. Far-away visitors get more latency.
- Record the first invoice for S15.
- Revisit if S5 misses its target (first try a CDN proxy in front of the same origin), if a month exceeds €10, or after Phase 1 to choose the 12-month term.
