# Agent skills

The agents in this repo use skills from 2 places:

1. **This folder.** The `yo-*` skills. I own and change them.
2. **The [`mattpocock/skills`](https://github.com/mattpocock/skills) plugin** (MIT), used as is. Version 1.3.1, upstream commit `49dd158`. Install it with `claude plugin install mattpocock-skills@claude-plugins-official`. I keep auto-update off, so the version changes only when I update it and record it here.

A plugin skill becomes a `yo-*` skill only when evidence shows it must change. Until then, the plugin version runs.

## Skills in this folder

| Skill | What it does | Replaces |
|---|---|---|
| [`yo-ask`](yo-ask/SKILL.md) | Says which skill or flow fits, and lists skill name clashes | `ask-matt` |
| [`yo-commit`](yo-commit/SKILL.md) | Splits work into Conventional Commits and waits for approval before committing | none |
| [`yo-create-plan`](yo-create-plan/SKILL.md) | Writes a plan file in `docs/plans/` | none. Overlaps with `to-spec`; not decided yet |
| [`yo-pr`](yo-pr/SKILL.md) | Opens a draft pull request with evidence, merge danger and what was left out | `pr` |
| [`yo-research`](yo-research/SKILL.md) | Researches primary sources. Confirms any finding that rules out an option with a second method | `research` |

Each skill's `CREDITS.md` lists the sources it borrowed from, with their licences.

## Plugin skills in use

| Step | Skills |
|---|---|
| Plan | `wayfinder`, `grill-with-docs`, `to-spec`, `to-tickets` |
| Build | `implement`, `tdd`, `code-review` |
| Improve the workflow | `retro` |
| As needed | `prototype`, `wizard`, `diagnosing-bugs`, `triage`, `handoff` |
| Called by other skills | `grilling`, `domain-modeling`, `codebase-design`, `writing-for-agents` |
| Once per repo | `setup-matt-pocock-skills` |

Not used: `pr`, replaced by `yo-pr`, `ask-matt`, replaced by `yo-ask`, and `research`, replaced by `yo-research`.

`wayfinder` calls `research` by name. A map's Notes must name `yo-research` for its research tickets.

## Turning a plugin skill into a `yo-*` skill

1. **Copy it unchanged, in its own commit.** Copy the folder to `yo-<name>/`. A shorter name is fine when the copy commit names the original. Change only the `name:` line. Add the upstream `LICENSE` and a `CREDITS.md` that names the upstream commit.
2. **Check the callers.** Skills call each other by name. `implement` calls `tdd` and `code-review`, so a new `yo-code-review` isn't used by the plugin's `implement`. Copy the caller too, or run that step by hand.
3. **Change it in later commits.** One change per commit. `git diff` from the copy commit shows everything that differs from upstream.
4. **Add ideas from other sources** to the same skill. Add each source to `CREDITS.md` with its licence.
5. **Update the tables above.**
