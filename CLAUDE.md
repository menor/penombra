# Penombra

A visual synthwave and darkwave catalogue on MusicBrainz data, with lists and an MCP server.

Read these before doing anything:

@CONTEXT.md
@plan.md

Data findings and limits: `data-check/README.md`.

Agent skills, their sources and how to fork one: `.agents/skills/README.md`.

Plans live in `docs/plans/`, one folder per plan. Create them with `/yo-create-plan`.

Setup: `pnpm install`. It also installs the `commit-msg` hook that runs commitlint.

Branching: 1 issue, 1 branch (`gh issue develop <N> --checkout`), 1 squash-merged PR into `main`. Never commit to `main` directly. Why: `docs/adr/0001-github-flow-squash-merge.md`.

This repo is public. Never commit email addresses or other personal details.

## Agent skills

### Issue tracker

Issues live in GitHub Issues for `menor/penombra`, through the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The 5 default labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single context: one glossary and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
