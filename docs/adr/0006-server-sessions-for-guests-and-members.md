---
status: accepted
date: 2026-11-25
---

# Server sessions in cookies for guests and members

Guests and members are identified by a server session. The browser holds only a random session ID in a cookie set with `HttpOnly`, `Secure` and `SameSite=Lax`, and a new ID is issued at sign-in. A guest gets a server-side account at the first list, kept for 30 days; signing up turns it into a member account and keeps the lists. We chose this because a session can be revoked by deleting a row, a script cannot read the cookie, and guests and members share one code path for lists. The cost: CSRF protection, guest rows, and a job that deletes expired guests.

## Considered options

- **Tokens in browser storage** (for example a JWT in `localStorage`). Rejected: any script on the page can read it, so one XSS bug leaks it, and it stays valid until it expires.
- **Guest lists in `localStorage`.** Rejected: a second code path for lists, a merge step at sign-up, and lists lost when browser data is cleared or the device changes.

## Consequences

- Creating guest accounts needs a rate limit.
- Social sign-in ("Sign in with GitHub") can come later as an extra sign-in method. It ends in the same session.
- Open for Phase 4: how members sign up.
- OAuth for the MCP server is a separate decision and gets its own ADR in Phase 6.
