---
name: skill-converter
description: >-
  Converts any Claude Code skill, GitHub Copilot CLI skill, Amp skill, Cursor rule, Cline mode,
  or external agent skill into a 100% Antigravity-compatible skill. Use when the user asks to
  "convert a skill", "port claude skill to antigravity", "convert copilot skill", "make skill antigravity compatible",
  "migrate agent skills", or "import claude skills". Triggers include: "convert skill", "claude skill",
  "port skill", "skill converter", "migrate skills".
---

# Antigravity Skill Converter

Transforms existing agent skills from **Claude Code** (`~/.claude/skills/`), **GitHub Copilot CLI** (`~/.copilot/skills/`, `.github/skills/`), **Amp** (`.agents/skills/`), **Cursor**, **Cline / Roo Code**, or generic AI frameworks into **100% native, production-grade Antigravity skills**.

---

## 1. Antigravity Skill Architecture

Antigravity uses **Progressive Disclosure** to maintain a lean context window:
1. **Catalog Indexing**: Only the YAML `name` and `description` are loaded into memory at startup.
2. **Semantic Activation**: When a user's prompt matches the description keywords or intent, Antigravity dynamically activates the skill and loads `SKILL.md`.
3. **Layered Depth**: Heavy specifications, APIs, and schemas are partitioned into `references/`, reusable scripts into `scripts/`, and examples into `examples/`.

For complete architectural details, see:
- Tool Translation: [references/tool-translation-matrix.md](references/tool-translation-matrix.md)
- Frontmatter Specification: [references/frontmatter-spec.md](references/frontmatter-spec.md)
- Antigravity Runtime Rules: [references/antigravity-runtime-rules.md](references/antigravity-runtime-rules.md)

---

## 2. Operating Modes

### Mode 1: Automated CLI Execution (Recommended)
Run the converter script directly via `run_command`:

```bash
# Convert a single skill directory or SKILL.md into ~/.agents/skills/<name>
python C:/Users/Admin/.agents/skills/skill-converter/scripts/convert_skill.py <path_to_source_skill>

# Dry-run preview without writing files
python C:/Users/Admin/.agents/skills/skill-converter/scripts/convert_skill.py <path_to_source_skill> --dry-run

# Batch convert an entire folder of skills (e.g. ~/.claude/skills)
python C:/Users/Admin/.agents/skills/skill-converter/scripts/convert_skill.py <path_to_skills_root> --batch
```

### Mode 2: Interactive In-Conversation Conversion
When the user pastes a raw skill, prompt, or points to an arbitrary file in chat:
1. Parse the input using the **Conversion Pipeline** below.
2. Apply surgical tool mappings (`Bash` $\to$ `run_command`, `View` $\to$ `view_file`, etc.).
3. Write the resulting files into `C:\Users\Admin\.agents\skills\<slug>\` using `write_to_file`.
4. Report the absolute directory path with a clickable `file:///` markdown link.

### Mode 3: Batch Migration
When migrating an entire developer environment (e.g. from Claude Code or Copilot):
1. Locate external skills using `find_by_name` across `~/.claude/skills` or `.github/skills`.
2. Execute `convert_skill.py --batch` against the directory.
3. Validate that each generated skill has a valid `SKILL.md` and trigger description.

---

## 3. Step-by-Step Conversion Pipeline

### Step 1: Ingest & Clean Frontmatter
- Strip foreign attributes like `allowed-tools:`, `tags:`, `version:`, `alwaysApply:`.
- Format `name`: Ensure lowercase alphanumeric with hyphens (`kebab-case`).
- Format `description`: Must be third-person, describing **what** it does, **when** to activate, and explicit **triggers** (`Triggers include: "...", "..."`).

### Step 2: Tool Translation
Map all external tool calls to native Antigravity tools:
- `Bash` / `terminal` / `execute_command` $\to$ `run_command`
- `View` / `Read` / `read_file` $\to$ `view_file` (prefer `StartLine`/`EndLine` slices)
- `Edit` / `replace_in_file` $\to$ `replace_file_content`
- `Write` / `write_to_file` $\to$ `write_to_file`
- `Grep` / `search_files` $\to$ `grep_search`
- `Glob` / `file_search` $\to$ `find_by_name`
- `AskUser` / `ask_followup_question` $\to$ `ask_question`
- `$ARGUMENTS` $\to$ `<user-arguments>`

### Step 3: Progressive Disclosure Partitioning
- If the body exceeds 140 lines or contains extensive sub-manuals (specifications, schema tables, API lists), extract them into `references/<subtopic>.md`.
- Link extracted references from `SKILL.md` using relative markdown links (`[spec](references/spec.md)`).

### Step 4: Validate & Output Reporting
- Verify `SKILL.md` exists and starts with valid YAML frontmatter.
- Report the full absolute directory path to the user.
- Provide clickable markdown links using forward slashes (e.g. `[SKILL.md](file:///C:/Users/Admin/.agents/skills/<name>/SKILL.md)`).
- Ensure host hardware constraints are respected (AVX baseline, CPU-only execution).
