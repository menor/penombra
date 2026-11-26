---
status: accepted
date: 2026-11-25
---

# Separate TypeScript API service with REST

The backend is its own TypeScript service with a REST interface, apart from the frontend. We chose this because a separate service keeps the backend boundary clear, and REST responses are simple to cache and to test with plain HTTP. The cost: two deployables and an API contract to keep in step with the frontend.

## Considered options

- **GraphQL.** Rejected: the filters are fixed facets, so flexible queries add a schema layer and harder caching for little gain.
- **Framework server functions** (Next.js or TanStack Start). Rejected with those frameworks in ADR 0003. They also blur where the backend starts.

## Consequences

- The MCP server can call the same service, so the catalogue and list rules live in one place.
- The Node framework is Hono. See ADR 0009.
