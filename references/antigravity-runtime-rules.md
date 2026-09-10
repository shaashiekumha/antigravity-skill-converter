# Antigravity Runtime Rules & Host Constraints

When converting and generating skills for Antigravity, the skill must adhere to the host runtime constraints and user rules.

---

## 1. Output Path Reporting (Mandatory)

1. **Full Absolute Paths**:
   Whenever a skill generates, exports, or modifies deliverables, the agent must explicitly state the full absolute directory or file path.
2. **Clickable Markdown Links**:
   Every reported path must be a clickable markdown link using forward slashes and the `file:///` URI scheme:
   - Folder: `[Output Directory](file:///C:/Users/Admin/path/to/dir)`
   - File: `[README.md](file:///C:/Users/Admin/path/to/README.md)`
   - Specific lines: `[config.py:L10-L25](file:///C:/Users/Admin/path/to/config.py#L10-L25)`

---

## 2. Hardware & Architecture Constraints

1. **Host Configuration**:
   - Intel Core i5 (3rd Gen), 12 GB RAM, No discrete GPU (CPU-only).
   - Supported SIMD: **AVX only**. (Does NOT support AVX2 or AVX512).
2. **Local Model Rules**:
   - Never run raw float32/float16 PyTorch or unquantized transformers models directly on CPU.
   - Restrict local inference to lightweight (<3B parameters) quantized (Q4_K_M) models via Ollama / GGUF.
3. **Tooling & Binaries**:
   - Use baseline non-AVX2 builds of CLI tools (e.g. baseline Bun / Node).
   - In scripts, prefer standard library Python to ensure universal cross-platform execution without native binary crashes.

---

## 3. Surgical Editing Discipline

- Never replace entire files when modifying existing codebases.
- Use `replace_file_content` with exact `[StartLine, EndLine]` line ranges.
- Omit `ArtifactMetadata` when writing project code with `write_to_file`.
