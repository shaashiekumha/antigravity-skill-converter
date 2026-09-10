#!/usr/bin/env python3
"""
Antigravity Skill Converter (scripts/convert_skill.py)
Converts Claude Code, GitHub Copilot CLI, Amp, Cursor, Cline/Roo Code,
or other agent skills into 100% Antigravity-compatible skills.

Zero external dependencies - standard library only.
"""

import os
import sys
import re
import json
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Tool translation map: Source agent tools -> Antigravity native tools
TOOL_MAPPINGS = {
    # Claude Code / Anthropic tools
    "Bash": "run_command",
    "bash": "run_command",
    "View": "view_file",
    "view": "view_file",
    "Read": "view_file",
    "read": "view_file",
    "Edit": "replace_file_content",
    "edit": "replace_file_content",
    "Write": "write_to_file",
    "write": "write_to_file",
    "Glob": "find_by_name",
    "glob": "find_by_name",
    "Grep": "grep_search",
    "grep": "grep_search",
    "LS": "list_dir",
    "ls": "list_dir",
    "WebSearch": "search_web",
    "web_search": "search_web",
    "FetchUrl": "read_url_content",
    "fetch_url": "read_url_content",
    "AskUser": "ask_question",
    "ask_user": "ask_question",
    "Subagent": "invoke_subagent",
    "subagent": "invoke_subagent",

    # Cline / Roo Code tools
    "execute_command": "run_command",
    "read_file": "view_file",
    "write_to_file": "write_to_file",
    "replace_in_file": "replace_file_content",
    "search_files": "grep_search",
    "list_files": "list_dir",
    "list_code_definition_names": "grep_search",
    "browser_action": "read_url_content",
    "ask_followup_question": "ask_question",

    # Cursor / Windsurf tools
    "codebase_search": "grep_search",
    "file_search": "find_by_name",
    "terminal": "run_command",
    "run_terminal_command": "run_command",
}


def sanitize_slug(name: str) -> str:
    """Normalize any name into a clean kebab-case skill identifier."""
    name = re.sub(r"[^a-zA-Z0-9\-_ ]", "", name)
    slug = re.sub(r"[\s_]+", "-", name).strip("-").lower()
    return slug or "converted-skill"


def parse_yaml_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    """Parse YAML frontmatter without external dependencies."""
    frontmatter: Dict[str, str] = {}
    remaining = content.strip()

    if remaining.startswith("---"):
        parts = remaining.split("---", 2)
        if len(parts) >= 3:
            raw_fm = parts[1].strip()
            remaining = parts[2].strip()

            current_key = None
            multiline_val: List[str] = []

            for line in raw_fm.splitlines():
                # Check for new key
                key_match = re.match(r"^([a-zA-Z0-9_-]+)\s*:\s*(.*)$", line)
                if key_match:
                    if current_key and multiline_val:
                        frontmatter[current_key] = "\n".join(multiline_val).strip()
                        multiline_val = []

                    key = key_match.group(1).lower()
                    val = key_match.group(2).strip()

                    if val in [">", ">-", "|", "|-"]:
                        current_key = key
                    else:
                        current_key = None
                        # Strip surrounding quotes if present
                        val_clean = val.strip("'\"")
                        frontmatter[key] = val_clean
                elif current_key and line.startswith("  "):
                    multiline_val.append(line.strip())

            if current_key and multiline_val:
                frontmatter[current_key] = " ".join(multiline_val).strip()

    return frontmatter, remaining


def translate_tools(text: str) -> str:
    """Translate tool names to native Antigravity tools using exact token matching."""
    # 1. Backticked tools: `Bash` -> `run_command`
    for src_tool in sorted(TOOL_MAPPINGS.keys(), key=len, reverse=True):
        text = re.sub(rf"`{re.escape(src_tool)}`", f"`{TOOL_MAPPINGS[src_tool]}`", text)

    # 2. Natural language phrases: "use the Bash tool", "using the View tool", etc.
    keys_sorted = sorted(TOOL_MAPPINGS.keys(), key=len, reverse=True)
    pattern_tools = "|".join(re.escape(k) for k in keys_sorted)
    phrase_pattern = rf"\b(use\s+(?:the\s+)?|using\s+(?:the\s+)?|run\s+(?:the\s+)?)({pattern_tools})(\s+tool\b)?"

    def _replace_phrase(match):
        prefix = match.group(1) or ""
        tool_matched = match.group(2)
        suffix = match.group(3) or ""
        agy_tool = TOOL_MAPPINGS.get(tool_matched, tool_matched)
        return f"{prefix}`{agy_tool}`{suffix}"

    text = re.sub(phrase_pattern, _replace_phrase, text, flags=re.IGNORECASE)

    # 3. Replace Claude slash arguments ($ARGUMENTS)
    text = re.sub(r"\$ARGUMENTS\b", "<user-arguments>", text)
    return text


def build_antigravity_description(slug: str, original_desc: Optional[str], body: str) -> str:
    """
    Construct a top-tier third-person description for Antigravity progressive disclosure.
    Antigravity indexes this description to decide when to activate the skill.
    """
    desc = ""
    if original_desc and len(original_desc.strip()) > 15:
        clean = original_desc.strip()
        # Ensure third-person phrasing
        if clean.lower().startswith("you are") or clean.lower().startswith("i will"):
            clean = "Provides specialized workflow to " + clean
        elif not any(clean.lower().startswith(w) for w in ["use", "provides", "converts", "generates", "automates", "guides"]):
            clean = f"Provides guidance and procedures to {clean[:1].lower() + clean[1:]}"
        desc = clean
    else:
        # Generate from slug and body content
        title = slug.replace("-", " ").title()
        desc = f"Specialized procedures and workflows for {title}."

    # Extract keywords and generate explicit trigger phrases if missing
    triggers: List[str] = [t for t in slug.split("-") if len(t) > 2]
    
    # Check body for additional high-value triggers
    for kw in ["workflow", "audit", "build", "deploy", "generate", "analyze", "test", "convert"]:
        if kw in body.lower() and kw not in triggers:
            triggers.append(kw)

    triggers_formatted = ", ".join([f'"{t}"' for t in triggers[:5]])
    if "trigger" not in desc.lower() and "use when" not in desc.lower():
        desc += f" Use when working on {slug.replace('-', ' ')}. Triggers include: {triggers_formatted}."
    elif "triggers include:" not in desc.lower() and triggers:
        desc += f" Triggers include: {triggers_formatted}."

    return desc


def split_progressive_disclosure(body: str, max_lines: int = 140) -> Tuple[str, Dict[str, str]]:
    """
    Split lengthy manuals, tables, or API reference sections into separate
    files inside references/ to keep SKILL.md lightweight and context-efficient.
    """
    lines = body.splitlines()
    if len(lines) <= max_lines:
        return body, {}

    references: Dict[str, str] = {}
    main_lines: List[str] = []
    current_ref_title = None
    current_ref_lines = []
    in_ref = False

    for line in lines:
        if line.startswith("## ") or line.startswith("### "):
            header_text = line.lstrip("#").strip()
            # If previous section was long, finalize it
            if in_ref and len(current_ref_lines) > 20:
                ref_slug = sanitize_slug(current_ref_title) + ".md"
                references[ref_slug] = f"# {current_ref_title}\n\n" + "\n".join(current_ref_lines)
                main_lines.append(f"\nFor detailed specifications on **{current_ref_title}**, see [references/{ref_slug}](references/{ref_slug}).\n")
                current_ref_lines = []
                in_ref = False

            lower = header_text.lower()
            if any(k in lower for k in ["reference", "spec", "schema", "appendix", "guidelines", "rules", "api", "cheat sheet", "options"]):
                in_ref = True
                current_ref_title = header_text
                current_ref_lines = []
                continue
            else:
                in_ref = False

        if in_ref:
            current_ref_lines.append(line)
        else:
            main_lines.append(line)

    if in_ref and len(current_ref_lines) > 10:
        ref_slug = sanitize_slug(current_ref_title) + ".md"
        references[ref_slug] = f"# {current_ref_title}\n\n" + "\n".join(current_ref_lines)
        main_lines.append(f"\nFor detailed specifications on **{current_ref_title}**, see [references/{ref_slug}](references/{ref_slug}).\n")

    return "\n".join(main_lines), references


def convert_skill(
    source_path: Path,
    output_root: Path,
    custom_name: Optional[str] = None,
    custom_desc: Optional[str] = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """Convert a single external skill folder or file into an Antigravity skill."""
    skill_file = None
    source_dir = None

    if source_path.is_file():
        skill_file = source_path
        source_dir = source_path.parent
    elif source_path.is_dir():
        source_dir = source_path
        # Look for standard skill entrypoints
        candidates = ["SKILL.md", "skill.md", "README.md", f"{source_path.name}.md"]
        for c in candidates:
            if (source_path / c).is_file():
                skill_file = source_path / c
                break
        if not skill_file:
            # Look for any markdown file
            md_files = list(source_path.glob("*.md"))
            if md_files:
                skill_file = md_files[0]
            else:
                raise FileNotFoundError(f"No markdown skill entrypoint found in {source_path}")

    with open(skill_file, "r", encoding="utf-8", errors="ignore") as f:
        raw_text = f.read()

    frontmatter, clean_body = parse_yaml_frontmatter(raw_text)

    # Determine skill slug
    slug = custom_name or frontmatter.get("name") or source_dir.name
    slug = sanitize_slug(slug)

    # Build description
    raw_desc = custom_desc or frontmatter.get("description")
    description = build_antigravity_description(slug, raw_desc, clean_body)

    # Translate tools in body
    translated_body = translate_tools(clean_body)

    # Ensure clean title
    if not translated_body.startswith("# "):
        title = slug.replace("-", " ").title()
        translated_body = f"# {title}\n\n{translated_body}"

    # Progressive disclosure partitioning
    main_skill_md, references = split_progressive_disclosure(translated_body)

    # Standard Antigravity SKILL.md composition
    final_skill_md = f"""---
name: {slug}
description: >-
  {description.strip()}
---

{main_skill_md.strip()}

---

## Operational Guidelines for Antigravity
- **Surgical Tooling**: Prefer line-targeted inspection (`view_file` with line slices, `grep_search`) and surgical edits (`replace_file_content`).
- **Explicit Output Paths**: Whenever generating or baking files, explicitly state the full absolute path and provide a clickable markdown link using `file:///` format.
- **Hardware Efficiency**: Respect CPU-only constraints; never execute unquantized local models.
"""

    result = {
        "slug": slug,
        "description": description,
        "skill_md": final_skill_md,
        "references": references,
        "source_dir": source_dir,
        "target_dir": output_root / slug
    }

    if dry_run:
        return result

    # Write output structure
    target_dir = result["target_dir"]
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "scripts").mkdir(parents=True, exist_ok=True)
    (target_dir / "references").mkdir(parents=True, exist_ok=True)
    (target_dir / "examples").mkdir(parents=True, exist_ok=True)
    (target_dir / "resources").mkdir(parents=True, exist_ok=True)

    # Write SKILL.md
    with open(target_dir / "SKILL.md", "w", encoding="utf-8") as f:
        f.write(final_skill_md)

    # Write extracted references
    for ref_name, ref_content in references.items():
        with open(target_dir / "references" / ref_name, "w", encoding="utf-8") as f:
            f.write(ref_content)

    # Copy existing files and subdirectories from source if present
    if source_dir and source_dir.is_dir() and source_dir != target_dir:
        for item in source_dir.iterdir():
            # Skip SKILL.md since it was rewritten
            if item.name.lower() in ["skill.md", "readme.md"]:
                continue
            dst_item = target_dir / item.name
            if item.is_file() and not dst_item.exists():
                shutil.copy2(item, dst_item)
            elif item.is_dir():
                dst_item.mkdir(parents=True, exist_ok=True)
                for root, dirs, files in os.walk(item):
                    rel = Path(root).relative_to(item)
                    target_sub = dst_item / rel
                    target_sub.mkdir(parents=True, exist_ok=True)
                    for f in files:
                        dst_file = target_sub / f
                        if not dst_file.exists():
                            shutil.copy2(Path(root) / f, dst_file)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Convert any Claude Code, Copilot, Amp, or external agent skill into an Antigravity skill."
    )
    parser.add_argument("source", help="Path to source skill directory, SKILL.md file, or root folder for batch")
    parser.add_argument(
        "-o", "--output",
        default=os.path.expanduser(r"~\.agents\skills"),
        help="Target skills root directory (default: ~/.agents/skills)"
    )
    parser.add_argument("-n", "--name", help="Override skill name / slug")
    parser.add_argument("-d", "--description", help="Override skill description")
    parser.add_argument("--batch", action="store_true", help="Batch convert all skills found under source directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview output without writing files")

    args = parser.parse_args()
    source_path = Path(args.source).resolve()
    output_root = Path(args.output).resolve()

    if not source_path.exists():
        print(f"Error: Source path does not exist: {source_path}", file=sys.stderr)
        sys.exit(1)

    print(f"============================================================")
    print(f"  Antigravity Skill Converter Engine")
    print(f"============================================================")
    print(f"Source: {source_path}")
    print(f"Destination: {output_root}")

    skills_to_convert: List[Path] = []
    if args.batch:
        for child in source_path.iterdir():
            if child.is_dir() and ((child / "SKILL.md").is_file() or (child / "skill.md").is_file()):
                skills_to_convert.append(child)
        print(f"[*] Discovered {len(skills_to_convert)} skill(s) for batch conversion.")
    else:
        skills_to_convert.append(source_path)

    converted_count = 0
    for item in skills_to_convert:
        try:
            res = convert_skill(
                item,
                output_root=output_root,
                custom_name=args.name,
                custom_desc=args.description,
                dry_run=args.dry_run
            )
            converted_count += 1
            print(f"\n[+] Successfully converted: {res['slug']}")
            print(f"    Description: {res['description']}")
            if args.dry_run:
                print(f"    [Dry-run] SKILL.md size: {len(res['skill_md'])} bytes")
            else:
                target = res["target_dir"]
                norm_target = str(target).replace('\\', '/')
                print(f"    Output Directory: {target}")
                print(f"    Clickable Link: [Skill Folder](file:///{norm_target})")
                print(f"    Entrypoint: [SKILL.md](file:///{norm_target}/SKILL.md)")
                if res["references"]:
                    print(f"    Extracted {len(res['references'])} references:")
                    for rname in res["references"]:
                        print(f"      - [{rname}](file:///{norm_target}/references/{rname})")
        except Exception as e:
            print(f"[-] Failed to convert {item}: {e}", file=sys.stderr)

    print(f"\nCompleted: {converted_count}/{len(skills_to_convert)} skill(s) converted successfully.")


if __name__ == "__main__":
    main()
