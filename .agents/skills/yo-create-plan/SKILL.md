---
name: yo-create-plan
description: Turn the current conversation into a plan file in docs/plans/, with provenance frontmatter, success criteria and phases as vertical slices. Proposes first, writes only after approval.
disable-model-invocation: true
---

# Create a plan

A plan is a committed file in `docs/plans/`. It records what we will build, how we will know it works, and why we chose this way.

## Steps

1. **Gather.** Use the current conversation first. Read `GLOSSARY.md` and the ADRs in `docs/adr/` that touch the area, if they exist. Use glossary terms throughout. If no task is clear, ask for it. Do not re-interview on what the conversation already settled.

2. **Define success criteria.** Each one is concrete and checkable, with the command or check that verifies it. Prefer numbers. Ask the user to confirm them before anything else.

3. **Choose the phases.** Offer three granularities with the phases each would contain: 1 phase, 2 to 3 phases, or more than 3. Let the user pick. Rules:
   - Each phase is a vertical slice. It spans every layer it needs (UI, API, database, tests) for one behaviour. Never split one behaviour by layer.
   - Phase 1 produces something the user can see, run or call.
   - Each phase merges on its own: checks pass and the code makes sense alone.
   - Setup (a new dependency, a migration tool) gets its own phase when it is more than a few lines.

4. **Name the contracts and test seams.** For each phase, list only the contract types that change:
   - API endpoints and their request and response shapes;
   - module interfaces;
   - database tables;
   - MCP tools;
   - user-facing copy;
   - test suites and their cases.

   Test at the highest seam that exists. Propose a new seam only when none fits.

5. **Propose.** Show the user the goal, success criteria, phases and contracts in the conversation. Do not write the file until the user approves.

6. **Write** `docs/plans/YYYY-MM-DD-<kebab-name>/plan.md` using the template below. The folder holds the plan's other files later, such as an exported conversation. If the folder exists, ask whether to overwrite or rename.

7. **Offer next steps.** Ask the user which they want:
   - stop here;
   - commit the plan alone;
   - create GitHub issues from it with `/to-tickets`, then link each phase to its issue (see "Plans and issues");
   - implement phase 1 only.

## Frontmatter

Fill every field. Never guess a value: if you cannot find it, write `"unknown"`.

```yaml
---
name: "{ plan_name }"
description: "{ plan_description }"
created_at: "{ current_date }"

created_by:
  tool: "{ tool }"
  model:
    name: "{ model.name }"
    version: "{ model.version }"
---
```

- `current_date`: ISO 8601 RFC 3339 in UTC, `YYYY-MM-DDTHH:MM:SSZ`. Get it with `date -u +%Y-%m-%dT%H:%M:%SZ`. Do not write it from memory.
- `created_by.tool`: the AI coding tool, for example `Claude Code`, `Cursor`, `Copilot`, `Codex`.
- `created_by.model.name`: the model family, for example `Claude Opus`, `Cursor Composer`, `OpenAI GPT`.
- `created_by.model.version`: for example `5.5`, `1.5`, `5.4`.

## Template

```markdown
<frontmatter>

# <Plan name>

## Goal

<1 to 3 sentences: what we build and why.>

## Success criteria

| # | Criterion | How to verify |
|---|---|---|
| 1 | <checkable outcome, with a number where possible> | <command or check> |

## Context

- <file, folder, doc, ADR or issue to read, linked>

## Decisions

- <choice made in the conversation, and the reason. Link the ADR if one exists.>

## Constraints

- <hard rule this plan must respect>

## Phases

### Phase 1: <behaviour, not layer>

Issue: <link, added after `/to-tickets`. Leave out until then.>

<1 to 2 sentences.>

Contracts:
- <only the types that change>

- [ ] <action>
  > [CONSTRAINT] <example of an inline annotation on one action>
- [ ] Run the project's verification command (see `AGENTS.md` or `CLAUDE.md`). Fix what fails.
- [ ] Stop. Present the changes and suggest a commit message. Do not start the next phase until the user asks.

## Out of scope

- <what this plan will not do, and why>

## Open questions

- <what is still undecided. Write "None" only if that is true.>

## Changelog

- <YYYY-MM-DD>: Plan created.
```

## Annotations

Annotations attach a note to one phase or one action. Write them as a quote line directly under it: `> [TAG] text`. Humans add them while reviewing a plan; agents add them when the conversation settles something about one step.

| Tag | Meaning | Effect on an agent |
|---|---|---|
| `[DECISION]` | A choice made for this step, with the reason | Do not revisit it. If it is hard to reverse, record an ADR and link it |
| `[CONSTRAINT]` | A hard rule for this step | Must hold. If it cannot, stop and say so |
| `[SKIP]` | Deliberately not done in this step | Do not do it |
| `[QUESTION]` | Undecided, and it blocks this step | Stop before the step. Ask the user. Replace the tag with the answer as a `[DECISION]` |

Use only these four tags. Do not tag lines under a heading that already says what they are, such as "Decisions" or "Out of scope".

Find every open question across plans with `grep -rn "\[QUESTION\]" docs/plans`.

## Plans and issues

Each fact has one owner. Never keep the same thing in two places by hand.

- **The plan owns intent:** goal, success criteria, decisions, constraints, phases and contracts.
- **The issue owns progress:** open or closed, who claimed it, the linked pull request.

Before `/to-tickets`, track progress with the checkboxes in the plan. After it, each phase links its issue and its checkboxes stop being updated. The issue state wins.

When intent changes mid-build:
1. Edit the plan first.
2. Add a changelog line with the date and the reason.
3. Update the affected issues to match.

When every phase is done, the plan is history. Do not keep editing it. Move lasting decisions to ADRs and new terms to `GLOSSARY.md`.

## Writing

- Short sentences. Numbers instead of adjectives.
- No code snippets in phases. They go stale. A type shape or schema settled in a prototype is the exception.
- Link files rather than paste them.
- Write in English.
