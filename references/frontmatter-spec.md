# Antigravity Skill Frontmatter & Progressive Disclosure Specification

This document details how Antigravity indexes skills, how progressive disclosure operates, and how to craft optimal frontmatter for converted skills.

---

## 1. Frontmatter Structure

Every Antigravity skill must begin with a YAML header at line 1 of `SKILL.md`:

```yaml
---
name: my-converted-skill
description: >-
  Provides specialized workflows for XYZ. Use when the user requests ABC, runs "/xyz",
  or needs help with 123. Triggers include: "xyz", "abc", "process xyz".
---
```

### Required Fields:
1. **`name`** (string):
   - Lowercase alphanumeric with hyphens (`kebab-case`).
   - Must match the parent directory name: `skills/<name>/SKILL.md`.
2. **`description`** (string):
   - Written strictly in **third-person** ("Provides...", "Converts...", "Automates...").
   - Must state **what** the skill does.
   - Must state **when** the agent should activate it.
   - Must explicitly list **trigger keywords** (`Triggers include: ...`).

---

## 2. Progressive Disclosure Mechanics

1. **Passive Phase (Catalog Indexing)**:
   - When Antigravity initializes or receives a prompt, it does **not** read all `SKILL.md` bodies.
   - It only loads the `name` and `description` of available skills.
   - If your description is vague (e.g. `description: Helper for tests`), the model will fail to activate the skill when needed.
2. **Active Phase (Activation)**:
   - When the user's prompt matches the description keywords or intent, the agent activates the skill and reads the full `SKILL.md` body.
3. **Deep Retrieval Phase**:
   - For complex skills, keep `SKILL.md` under 150 lines.
   - Store detailed specifications, schema models, and edge-case documentation in `references/<topic>.md`.
   - The agent will selectively view those reference files only if required.

---

## 3. Disallowed / Filtered Frontmatter Fields

External agents often put host-specific flags in frontmatter that Antigravity ignores or handles differently:
- `allowed-tools`: Filtered out. Antigravity manages permissions at the tool layer.
- `tags` / `category`: Incorporated directly into the `description` as trigger words.
- `alwaysApply`: Converted into a project rule (`GEMINI.md`) if continuous, or kept as on-demand skill if conditional.
- `version`: Recorded in internal notes or changelog.
