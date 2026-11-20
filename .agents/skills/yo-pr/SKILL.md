---
name: yo-pr
description: Open or refresh a pull request with a Conventional title and a body that both reviewers and agents can read - what and why, issue and plan links, evidence, merge danger, and what was left out. Use when opening a PR, updating its title or body, or preparing a branch for review.
disable-model-invocation: true
---

# Pull request

A pull request body is a cover note for the reviewer. The reviewer may be a human or an agent that did not build the change and knows only what it reads.

## Steps

1. **Inspect.** Run `git branch --show-current`, `git status` and `gh pr view --json number,title,body,baseRefName`. If no PR exists, the base is the default branch. Then read `git log <base>..HEAD --oneline` and `git diff <base>...HEAD`. Read the whole branch diff, not only the last commit.

2. **Check the branch.**
   - On `main`: stop. The branch should come from `gh issue develop <N> --checkout` (see `docs/adr/0001-github-flow-squash-merge.md`). Ask the user which issue the work belongs to.
   - Uncommitted changes: commit them first with `/yo-commit`, or ask.
   - The verification command from `AGENTS.md` or `CLAUDE.md` must pass. Report its real result.

3. **Find the links.** Take the issue number from the user, the branch name, the commit footers or `gh issue view`. Never guess one. If the issue links a plan phase, link that too.

4. **Write the title and body** to a file in the scratchpad or `/tmp`, using the format below.

5. **Show the user** the title and body. Wait for approval.

6. **Push and open as a draft:**

   ```bash
   git push -u origin HEAD
   gh pr create --draft --title "<title>" --body-file <file>
   ```

   Update an existing PR with `gh pr edit <number> --title "<title>" --body-file <file>`.

7. **Report** the PR link and the CI state from `gh pr checks <number>`. Never mark it ready, merge it or request reviewers unless the user asks.

## Title

The title becomes the commit on `main`, because the repo uses squash merge (`docs/adr/0001-github-flow-squash-merge.md`). Follow the summary-line rules in `/yo-commit`: `type(scope): summary`, the same 6 types and the same scopes. Describe the whole branch, not the last commit.

## Body

```markdown
<What changed and why, in 1 to 3 sentences. Name the behaviour, not the files.>

Closes #<issue> · Plan: [<plan name>, phase <n>](<path to plan.md>)

## Summary

<Optional. One small visual that saves the reviewer reconstruction work. Leave the section out when prose is enough.>

## Evidence

**Before:** <screenshot, output or failing test>
**After:** <screenshot, output or passing test>

## Merge danger

**Door:** <one-way or two-way>. <Why, if one-way.>
**Blast radius:** <what can break, in a few words>

## Left out

- <what the issue asked for that this PR does not do, and why. Write "Nothing" if that is true.>
```

### Links line

- `Closes #N` when merging finishes the issue. `Refs #N` when it does not.
- Leave out the plan link when no plan exists. Leave out the line entirely only when there is neither an issue nor a plan.

### Summary visuals

Pick the smallest one that makes the point:

- a call tree for runtime flow;
- a component tree for UI structure;
- a shallow file tree for a broad refactor;
- a `diff` block of one of these trees when the shape already exists and the PR changes it;
- a Mermaid diagram for async flows or state transitions;
- pseudocode for an algorithm;
- a before and after example for a changed API, MCP tool or table.

Use one. Two at most. Introduce each with one sentence saying what to notice.

### Evidence

Required. Rank by strength:

1. Screenshots of the real app, when the change is visible. Never a mock or a page built for the PR. One row per page or state the change reaches.
2. A test that failed before and passes after. Name it and say what it checks.
3. Command output, trimmed to the lines that prove the point.

For docs, skills or config, one line is enough: what you checked and how.

List a check only if you saw its output in this session. Write everything else under "Not checked". Before opening, reread each claim in the body and point to the command that proves it. If you cannot upload a screenshot, say where it is and ask the user to attach it.

### Merge danger

- **Two-way door:** a revert undoes it fully.
- **One-way door:** a revert does not. Examples: a database migration that drops data, a changed public API or MCP tool, a sent email, deleted files in storage.
- **Blast radius:** think about other pages, API and MCP clients, mobile layout, performance, existing user data.

## Refresh

Rewrite the title and body when later commits change scope, approach, risk or what was left out. Describe the PR as it stands now. Do not narrate the review history. Skip refreshes for typo, format or rename commits.

## Never

- File-by-file change lists, commit logs, full CI logs or pasted commands.
- Placeholders or empty template sections, except "Left out: Nothing".
- Personal details: email addresses, names of private people, anything about the author's life outside the code. This repo is public.
- Issue numbers you did not verify.
