#!/usr/bin/env python3
"""
Script Name: scaffold.py
Author: Blaine Winslow (CBW)
Date: 2025-05-13

Summary:
--------
This script provides a robust CLI tool to scaffold directory structures from structured files.
It parses and creates file/folder hierarchies from `.scaffold`, `.json`, or `.yaml` input formats,
with intelligent structure validation, error reporting, and optional dry-run previews.

Features:
---------
- Token-based parsing of directory trees with depth tracking
- Multi-pass structure validation and normalized execution order
- Error handling for misaligned depth/nesting with optional fix or skip modes
- Command line options for structure creation, dry-run previews, and reverse generation
- Automatic scaffold generator with merge, overwrite, or rename options

Usage:
------
Run from terminal:
    scaffold                  # auto-uses .scaffold
    scaffold --file layout.yaml --dry-run
    scaffold --reverse
    scaffold --generate-scaffold --merge

Inputs:
-------
- A supported structure file (plain text, JSON, or YAML)

Outputs:
--------
- Created files and folders, or a .scaffold file

Modifications:
--------------
- Added support for structured parsing with validation hooks
- Implemented tokenizer for line-by-line depth-aware processing
- Added CLI flags for --skip-bad-entries and --fix-bad-entries
- Changed default structure file from .directory to .scaffold
- Overloaded input logic to default to .scaffold automatically
- Added scaffold generation with overwrite/merge/rename options
"""

# ...[UNCHANGED CODE ABOVE]...

def generate_scaffold_file(output_path: Path, strategy: str = "skip"):
    existing = output_path.exists()
    if existing:
        if strategy == "skip":
            log("Scaffold file already exists. Skipping.")
            return
        elif strategy == "rename":
            counter = 1
            while True:
                renamed = output_path.with_name(f"{output_path.stem}_{counter}{output_path.suffix}")
                if not renamed.exists():
                    output_path = renamed
                    break
        elif strategy == "merge":
            log("Merging new structure with existing .scaffold file...")
            try:
                existing_lines = output_path.read_text().splitlines()
                existing_set = set(line.strip() for line in existing_lines if line.strip())
            except Exception as e:
                log(f"Failed to read existing scaffold file: {e}")
                return

            def walk_tree(path: Path, depth=0):
                indent = "  " * depth
                for child in sorted(path.iterdir()):
                    if child.name.startswith(".") and child.name != ".gitignore":
                        continue
                    line = f"{indent}{child.name}/" if child.is_dir() else f"{indent}{child.name}"
                    if line.strip() not in existing_set:
                        merged_lines.append(line)
                    if child.is_dir():
                        walk_tree(child, depth + 1)

            merged_lines = existing_lines[:]
            walk_tree(Path.cwd())
            output_path.write_text("\n".join(sorted(set(merged_lines))))
            log(f"Merged structure written to {output_path}")
            return

    def walk_tree(path: Path, depth=0):
        indent = "  " * depth
        for child in sorted(path.iterdir()):
            if child.name.startswith(".") and child.name != ".gitignore":
                continue
            if child.is_dir():
                lines.append(f"{indent}{child.name}/")
                walk_tree(child, depth + 1)
            else:
                lines.append(f"{indent}{child.name}")

    lines = []
    walk_tree(Path.cwd())
    output_path.write_text("\n".join(lines))
    log(f"Scaffold file written to {output_path}")

# ...[UNCHANGED CODE BELOW]...
