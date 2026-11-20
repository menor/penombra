---
status: accepted
date: 2026-11-18
---

# GitHub flow with squash merge

`main` is always deployable. Each issue gets one short-lived branch, created with `gh issue develop <N> --checkout`, and one pull request. Pull requests are squash-merged, so each one becomes a single commit on `main`, titled with the PR title in Conventional Commits format. We chose this because plan phases are already sized to merge alone, each agent works one issue in its own worktree, and small, fast merges keep conflicts low. The cost: the commits inside a PR do not reach `main`; they stay on the PR page.

## Considered options

- **Integration branch per plan.** Phase PRs merge into `plan/<name>`, then one PR goes to `main`. Rejected: integration happens late, the final PR is large, and squash merge collapses every phase into one commit.
- **Stacked PRs** (Graphite, git-spice, ghstack). Kept as an exception, not the default. Use it with plain git when a phase is blocked on review. Adopt a tool if that happens more than about 3 times.
- **Git flow.** Rejected: built for versioned releases. Penombra has one deployed environment and no versions.
- **Merge commits.** Rejected: every intermediate commit lands on `main`, and history gets noisy.

## Consequences

- The PR title is the commit on `main`. It follows the format in `.agents/skills/yo-commit/SKILL.md`.
- The repo allows squash merge only, deletes branches on merge, and protects `main`: PRs required, checks must pass, no force push.
- Only the root commit went to `main` directly, so protection had a branch to apply to. Everything after it arrived through pull requests.
