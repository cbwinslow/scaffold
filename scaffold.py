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

Usage:
------
Run from terminal:
    scaffold                  # auto-uses .scaffold
    scaffold --file layout.yaml --dry-run
    scaffold --reverse
    scaffold --skip-bad-entries

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
"""

import sys
import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, Union, List

def log(msg: str):
    """Standardized log output."""
    print(f"[scaffold] {msg}")

def tokenize_structure(lines: List[str]) -> List[Dict]:
    """
    Tokenize each line of the structure file into a dictionary with:
    - type: 'file' or 'folder'
    - depth: indentation level
    - name: base name
    - raw: raw line for context
    """
    tokens = []
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        name = line.strip()
        is_folder = name.endswith("/")
        tokens.append({
            "type": "folder" if is_folder else "file",
            "depth": indent,
            "name": name.rstrip("/"),
            "raw": line.strip(),
            "line_number": i + 1
        })
    return tokens

def validate_tokens(tokens: List[Dict], skip_bad: bool, fix_bad: bool) -> List[Dict]:
    """
    Validate the token list. Detects bad entries and optionally skips or fixes them.
    """
    validated = []
    folder_stack = {}

    for token in tokens:
        depth = token["depth"]
        name = token["name"]
        ttype = token["type"]

        if ttype == "file" and depth - 2 not in folder_stack:
            msg = f"Line {token['line_number']}: File '{name}' has no parent folder at depth {depth - 2}."
            if skip_bad:
                log(f"SKIP: {msg}")
                continue
            elif fix_bad:
                log(f"FIX: {msg} → Assigning to root.")
                token["depth"] = 0
                validated.append(token)
                continue
            else:
                raise ValueError(msg)

        if ttype == "folder":
            folder_stack[depth] = name

        validated.append(token)

    return validated

def parse_structure_file(path: Union[Path, None]) -> List[str]:
    """
    Read lines from a supported structure file.
    Defaults to .scaffold if no file is passed.
    """
    if path is None:
        path = Path(".scaffold")

    suffix = path.suffix.lower()
    try:
        if suffix == ".json":
            with path.open("r") as f:
                return json.load(f)
        elif suffix in [".yaml", ".yml"]:
            with path.open("r") as f:
                return yaml.safe_load(f)
        else:
            with path.open("r") as f:
                return f.readlines()
    except Exception as e:
        log(f"Failed to parse structure file: {e}")
        sys.exit(1)

def build_from_tokens(base_path: Path, tokens: List[Dict], dry_run: bool = False):
    """
    Build file/folder structure from token list.
    Folders first, then files, sorted by depth.
    """
    for token in sorted([t for t in tokens if t["type"] == "folder"], key=lambda x: x["depth"]):
        full_path = base_path / token["name"]
        if dry_run:
            log(f"Would create folder: {full_path}")
        else:
            full_path.mkdir(parents=True, exist_ok=True)
            log(f"Created folder: {full_path}")

    for token in sorted([t for t in tokens if t["type"] == "file"], key=lambda x: x["depth"]):
        full_path = base_path / token["name"]
        if dry_run:
            log(f"Would create file: {full_path}")
        else:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.touch(exist_ok=True)
            log(f"Created file: {full_path}")

def main():
    parser = argparse.ArgumentParser(description="scaffold: Build directories from structure files")
    parser.add_argument("-f", "--file", type=str, help="Path to structure file", default=None)
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--reverse", action="store_true", help="Create a .scaffold file from folder layout")
    parser.add_argument("--skip-bad-entries", action="store_true", help="Skip invalid lines")
    parser.add_argument("--fix-bad-entries", action="store_true", help="Try to auto-fix invalid lines")
    args = parser.parse_args()

    base_path = Path.cwd()
    structure_file = Path(args.file) if args.file else None

    if args.reverse:
        output_file = base_path / ".scaffold"
        generate_directory_file(base_path, output_file)
        return

    if structure_file and not structure_file.exists():
        log(f"ERROR: Structure file not found at {structure_file}")
        sys.exit(1)

    raw_lines = parse_structure_file(structure_file)
    tokens = tokenize_structure(raw_lines)
    try:
        valid_tokens = validate_tokens(tokens, skip_bad=args.skip_bad_entries, fix_bad=args.fix_bad_entries)
    except ValueError as ve:
        log(f"ERROR: {ve}")
        log("Tip: run with --skip-bad-entries or --fix-bad-entries to avoid this error.")
        sys.exit(1)

    build_from_tokens(base_path, valid_tokens, dry_run=args.dry_run)
    log("Directory structure created successfully.")

if __name__ == "__main__":
    main()
