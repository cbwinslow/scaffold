# 📦 CBW Scaffold

A Python CLI tool that scaffolds folders and files from a structured plain text file like `.scaffold`, `.json`, or `.yaml`.

## 🔧 Features

- Token-based parsing with indentation-aware structure
- Dry-run mode to preview changes
- Fix or skip misaligned entries
- Reverse mode to generate `.scaffold` from an existing directory tree

## 🛠 Installation

```bash
chmod +x scaffold.py
mv scaffold.py ~/bin/scaffold

## Or

git clone https://github.com/cbwinslow/cbw-scaffold.git
cd cbw-scaffold
python scaffold.py

## Usage

scaffold --file layout.yaml
scaffold --dry-run
scaffold --skip-bad-entries
scaffold --fix-bad-entries
scaffold --reverse

## Example of a .scaffold file 
## Copy and paste this into the .scaffold file:
src/
  main.py
  utils/
    helpers.py
README.md

## Author
Peace and Love @cbwinslow