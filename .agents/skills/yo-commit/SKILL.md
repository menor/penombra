---
name: yo-commit
description: Split the working tree into logical Conventional Commits, propose them, and commit only after approval. Use when the user asks to commit, split work into commits, or write a commit message.
disable-model-invocation: true
---

# Commit

One commit is one change a reviewer can read, revert or cherry-pick alone.

## Steps

1. **Inspect.** If the current branch is `main`, stop: create the issue branch with `gh issue develop <N> --checkout`, or ask which issue this work belongs to (see `docs/adr/0001-github-flow-squash-merge.md`). Then run `git status`, `git diff`, `git diff --cached` and `git log --oneline -10`. Read `AGENTS.md` or `CLAUDE.md` for the verification command.

2. **Group.** Split the changes into the fewest commits that keep unrelated concerns apart. Rules:
   - Never mix app code with agent tooling (skills, `AGENTS.md`, `CLAUDE.md`, agent workflows).
   - Keep a behaviour change and its tests in the same commit.
   - Keep a refactor apart from the behaviour change it enables. Refactor first.
   - Leave out files the user did not mention when their scope is unclear. Ask.

3. **Propose.** Show each planned commit: its message and its files. Do not stage anything until the user approves.

4. **Commit each group in order:**
   1. Stage explicit paths. Use `git add -p` for files with mixed changes. Never `git add .`, `git add -A` or `git commit -a`.
   2. Run `git diff --cached --check` and read `git diff --cached --stat` in their own command, not chained into the commit. If `--check` prints anything, stop and fix it before committing. Look for debug output, secrets, personal data and unrelated files.
   3. Run the verification command when the commit touches code. Report the real result.
   4. Commit. Never use `--no-verify`. If a hook fails, fix the cause and make a new commit attempt. Never amend a commit that already existed before this session.

5. **Report.** List each commit hash and subject, the checks run and their results, and what remains uncommitted. Do not push unless the user asks.

## Message format

```text
type(scope): summary

Body: why the change was made. Optional.

Refs: #12
Co-Authored-By: ...
```

### Types

Use only these six.

| Type | When |
|---|---|
| `feat` | New behaviour a user, API client or MCP client can see |
| `fix` | Corrects wrong behaviour |
| `refactor` | Changes structure, not behaviour. Includes performance work with no behaviour change |
| `test` | Adds or fixes tests only |
| `docs` | Documentation only |
| `chore` | Everything else: dependencies, config, CI, scripts, agent tooling |

Add `!` after the scope for a breaking change, and a `BREAKING CHANGE: <impact>` footer.

### Scopes

The scope says where the change lives. Use one of: `catalogue`, `lists`, `accounts`, `api`, `db`, `data`, `mcp`, `ui`, `ci`, `agents`, `docs`. Leave the scope out when a change spans more than two. Add a scope to this list in the same commit that first needs it.

### Summary line

- Imperative mood: "add", not "added" or "adds".
- Lowercase first letter. No period.
- At most 72 characters including type and scope.
- Says what changed for the reader, not which files: "add trigram index to release search", not "update search.sql".

### Body

- Only when the summary does not explain the why.
- Wrap at 72 characters. One blank line after the summary.
- Explain why and the previous behaviour. The diff already shows what.

### Footers

- `Fixes: #N` when the commit completes an issue. `Refs: #N` when it only relates to one.
- `Co-Authored-By: {tool} - {model.name} {model.version} <{email}>`, for example `Co-Authored-By: Claude Code - Claude Opus 5.5 <noreply@anthropic.com>`. Skip it if the tool already adds a co-author trailer.

## Never

- Personal details in messages: email addresses, names of private people, anything about the author's life outside the code. This repo is public.
- Secrets, tokens or `.env` files in a commit.
- Vague summaries: "update files", "fix stuff", "wip".

## Writing the commit

Pass the summary and each body paragraph as its own `-m`. Pass footers with `--trailer`, so git keeps them together in the last paragraph. Never write a literal `\n` or open an editor.

```bash
git commit -m "feat(lists): add public share page" \
  -m "Guests could not see a list without an account." \
  --trailer "Refs: #14" \
  --trailer "Co-Authored-By: Claude Code - Claude Opus 5.5 <noreply@anthropic.com>"
```

`--trailer` writes `Key: value`, so issue footers become `Refs: #14` and `Fixes: #14`. GitHub closes issues from `Fixes: #14` too.
