# Conversion Example: Claude Code Skill to Antigravity Skill

---

## 1. Original Claude Code Skill (`~/.claude/skills/code-review/SKILL.md`)

```markdown
---
name: code-review
description: Review git changes before creating PRs
allowed-tools: Bash, View, Grep
---

# Code Review

Perform thorough code review on git branches.

## Steps
1. Run `git diff main...HEAD` with the Bash tool.
2. If large changes exist, use Grep to check for console.log or debugger statements.
3. Open changed files with the View tool to inspect context.
4. Output a summary list of suggestions.
```

---

## 2. Converted Antigravity Skill (`~/.agents/skills/code-review/SKILL.md`)

```markdown
---
name: code-review
description: >-
  Reviews git branch changes, detects debugging artifacts, and produces structured pull request feedback.
  Use when the user asks for a code review, checks git diff, or runs "/code-review". Triggers include:
  "code review", "review diff", "audit PR", "check changes".
---

# Code Review Skill

Performs thorough static code reviews on git branches with automated artifact detection.

## Review Procedure

1. **Inspect Branch Diff**:
   Execute git diff against the primary branch using `run_command`:
   ```bash
   git diff main...HEAD
   ```

2. **Detect Leftover Debug Statements**:
   Use `grep_search` across changed directories for leftover debugging calls:
   - JavaScript/TypeScript: `console\.log|debugger;`
   - Python: `print\(|breakpoint\(\)|import pdb`

3. **Targeted File Inspection**:
   Use `view_file` with `StartLine` and `EndLine` slices to inspect changed functions without bloating context.

4. **Deliver Structured Findings**:
   Provide a categorized markdown review (Bugs, Performance, Style, Security) and include clickable file links (`[file.ts:L45-L60](file:///C:/path/to/file.ts#L45-L60)`).
```
