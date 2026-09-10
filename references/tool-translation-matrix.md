# Tool Translation Matrix: External Agent Tools to Antigravity

This reference table maps tools from Claude Code, GitHub Copilot, Amp, Cursor, and Cline/Roo Code directly to Antigravity native tools, highlighting parameter differences and operational guidelines.

---

## 1. Primary Tool Crosswalk

| Source Ecosystem Tool | Antigravity Native Tool | Description & Parameter Transformation |
| :--- | :--- | :--- |
| `Bash(command)` / `terminal` / `execute_command` | `run_command` | Execute shell commands in PowerShell/cmd.<br>**Args**: `CommandLine`, `Cwd`, `WaitMsBeforeAsync`.<br>**Rule**: Never propose `cd`. Set `WaitMsBeforeAsync` appropriately. |
| `View(file)` / `Read(file)` / `read_file` | `view_file` | View contents of files.<br>**Args**: `AbsolutePath` (required), `StartLine`, `EndLine`, `ContentOffset`.<br>**Rule**: Use line slices to prevent context saturation. |
| `Edit(file, old, new)` / `replace_in_file` | `replace_file_content` | Precision in-place code editing.<br>**Args**: `TargetFile`, `TargetContent`, `ReplacementContent`, `StartLine`, `EndLine`.<br>**Rule**: Requires exact character match within specified line range. |
| `Write(file, content)` / `write_to_file` | `write_to_file` | Create or overwrite files.<br>**Args**: `TargetFile`, `CodeContent`, `Overwrite`, `Description`.<br>**Rule**: Omit `ArtifactMetadata` for project/source files; only include for conversational artifacts. |
| `Grep(pattern)` / `search_files` | `grep_search` | Ripgrep-based fast text search across codebases.<br>**Args**: `SearchPath`, `Query`, `Includes`, `CaseInsensitive`, `MatchPerLine`. |
| `Glob(pattern)` / `file_search` | `find_by_name` | Search files and folders by glob name using `fd`.<br>**Args**: `SearchDirectory`, `Pattern`, `Extensions`, `MaxDepth`. |
| `LS(dir)` / `list_files` | `list_dir` | Enumerate children of a directory with file sizes.<br>**Args**: `DirectoryPath`. |
| `AskUser(prompt)` / `ask_followup_question` | `ask_question` | Interactive multi-choice modal rendered in chat UI.<br>**Args**: `questions` array with `question`, `options`, `is_multi_select`. |
| `FetchUrl(url)` / `browser_action` | `read_url_content` | Read public web pages as clean markdown via HTTP. |
| `WebSearch(query)` | `search_web` | Run live Google web searches.<br>**Args**: `query`, `domain`. |
| `Subagent(role, prompt)` | `invoke_subagent` / `define_subagent` | Launch isolated subagent conversations.<br>**Args**: `Subagents` array with `TypeName`, `Role`, `Prompt`, `Model`. |

---

## 2. Command Argument Translators

- Claude Code custom command arguments (e.g. `$ARGUMENTS`, `$1`, `$2`) $\to$ `<user-arguments>` with prompt-parsing instructions.
- Cursor MDC file filters (`globs: *.ts`) $\to$ Direct `find_by_name` or `grep_search` invocations within the skill steps.
