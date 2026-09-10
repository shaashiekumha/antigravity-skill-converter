# Antigravity Skill Converter (`skill-converter`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/)
[![Antigravity](https://img.shields.io/badge/compatible-Google%20Antigravity-4285F4.svg)](https://antigravity.google)
[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-38bdf8.svg)](https://shaashiekumha.github.io/antigravity-skill-converter/)

A universal conversion engine and progressive disclosure skill that converts agent skills from **Anthropic Claude Code**, **GitHub Copilot CLI**, **Amp**, **Cursor**, **Cline / Roo Code**, and generic agent formats into 100% native, production-grade **Google Antigravity** skills.

---

## Features

- **Progressive Disclosure Normalization**: Synthesizes high-citability YAML frontmatter with crisp third-person descriptions and explicit trigger keywords so Antigravity can accurately index and activate skills.
- **Surgical Tool Translation**: Maps foreign tooling conventions (`Bash`, `View`, `Edit`, `Write`, `Grep`, `Glob`, `AskUser`) to Antigravity primitives (`run_command`, `view_file`, `replace_file_content`, `write_to_file`, `grep_search`, `find_by_name`, `ask_question`).
- **Context-Preserving Partitioning**: Automatically extracts long specifications, schema catalogs, and reference tables (>140 lines) into `references/` documents, preventing LLM context bloat.
- **Zero External Dependencies**: Pure Python 3 standard library implementation. Works immediately on any operating system without installing third-party pip packages.
- **Batch Migration Engine**: Migrate dozens of skills in seconds using the `--batch` flag.
- **Hardware-Aware**: Optimized for baseline hardware constraints (AVX baseline, CPU-only execution, clean line slicing).

---

## Directory Layout

```text
antigravity-skill-converter/
├── SKILL.md                          # Antigravity skill specification & orchestration
├── LICENSE                           # Open-source MIT License
├── README.md                         # Project documentation & reference
├── docs/
│   └── skill-converter-guide.html    # Interactive, stylized operator manual
├── scripts/
│   └── convert_skill.py              # Zero-dependency Python migration engine
├── references/
│   ├── tool-translation-matrix.md   # Complete tool crosswalk reference
│   ├── frontmatter-spec.md           # Progressive disclosure & YAML specification
│   └── antigravity-runtime-rules.md  # Runtime constraints & output reporting rules
└── examples/
    ├── claude-code-to-antigravity.md # Claude Code skill before & after
    └── copilot-cli-to-antigravity.md # Copilot CLI skill before & after
```

---

## Quickstart

### 1. Installation into Antigravity
Clone or copy this repository into your global or workspace Antigravity skills directory:

```bash
# Global Antigravity skills directory (Windows)
git clone https://github.com/shaashiekumha/antigravity-skill-converter.git %USERPROFILE%\.agents\skills\skill-converter

# Global Antigravity skills directory (Linux / macOS)
git clone https://github.com/shaashiekumha/antigravity-skill-converter.git ~/.agents/skills/skill-converter
```

Once placed in `.agents/skills/`, Antigravity will automatically detect `skill-converter`.

---

## Usage

### Method 1: Conversational Chat Invocations
Ask Antigravity directly in the chat interface:
- *"agy, convert the claude skill at `C:\path\to\skill` into an antigravity skill"*
- *"agy, port my copilot skill in `.github/skills/deploy` to antigravity"*
- *"agy, migrate all skills in `~/.claude/skills` to `~/.agents/skills`"*

### Method 2: Command-Line Interface (CLI)
Run the bundled converter script directly:

```bash
# Convert a single skill directory or SKILL.md
python scripts/convert_skill.py "path/to/source-skill"

# Specify a custom output root
python scripts/convert_skill.py "path/to/source-skill" -o "~/.agents/skills"

# Preview conversion without writing to disk
python scripts/convert_skill.py "path/to/source-skill" --dry-run

# Batch migrate an entire directory of skills
python scripts/convert_skill.py "~/.claude/skills" --batch -o "~/.agents/skills"
```

---

## Tool Translation Crosswalk

| Source Agent Tool | Antigravity Native Tool | Description & Differences |
| :--- | :--- | :--- |
| `Bash` / `execute_command` | `run_command` | Executes shell commands in PowerShell/Bash with synchronous wait control. |
| `View` / `Read` / `read_file` | `view_file` | Reads file content using absolute paths and line slices (`StartLine`/`EndLine`). |
| `Edit` / `replace_in_file` | `replace_file_content` | Precision in-place code edits within explicit line boundaries. |
| `Write` / `write_to_file` | `write_to_file` | Writes whole files; omits artifact metadata for source files. |
| `Grep` / `search_files` | `grep_search` | High-speed ripgrep search with glob filtering. |
| `Glob` / `file_search` | `find_by_name` | Fast file/directory resolution powered by `fd`. |
| `AskUser` | `ask_question` | Renders an interactive modal in chat UI with selectable options. |
| `$ARGUMENTS` | `<user-arguments>` | Converted to semantic prompt parameter instructions. |

---

## Operator Manual & Guide

A comprehensive, stylized HTML manual is included in [`docs/skill-converter-guide.html`](docs/skill-converter-guide.html). You can open it in any browser for an interactive visual guide, copy-to-clipboard terminal snippets, and architectural breakdowns.

---

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/shaashiekumha/antigravity-skill-converter/issues).

---

## License

This project is licensed under the [MIT License](LICENSE) - open-source, public, and freely usable for personal and commercial workflows.
