# 📦 CBW Scaffold

**CBW Scaffold** is a smart, token-based Python CLI tool that builds directory structures from `.scaffold`, `.json`, or `.yaml` blueprint files. Designed to be fast, intuitive, and highly scriptable, it's your best friend for scaffolding new projects or exporting file structures.

---

## 🚀 Features

* ✅ **Plaintext `.scaffold` parsing** with indentation awareness
* ✅ **Dry-run mode** to preview what will be created
* ✅ **Skip/fix invalid entries** for resilience
* ✅ **Reverse mode** to generate `.scaffold` from existing folders
* ✅ **Merge, Overwrite, or Rename** behavior when `.scaffold` already exists
* ✅ Supports `.yaml` and `.json` formats as well

---

## 📦 Installation

### 📁 Clone Locally

```bash
git clone https://github.com/cbwinslow/scaffold.git
cd scaffold
chmod +x scaffold.py
mv scaffold.py ~/bin/scaffold
```

### 📡 (Coming Soon) PyPI Package

```bash
pip install cbw-scaffold
```

---

## 🛠 Usage

### 📁 Generate folders from `.scaffold`

```bash
scaffold  # uses .scaffold by default
```

### 🧪 Dry Run

```bash
scaffold --dry-run
```

### ♻️ Reverse Scaffold (export file layout)

```bash
scaffold --reverse
```

### 🔨 Generate `.scaffold` if missing

```bash
scaffold --generate-scaffold
```

### 🧩 Conflict Handling Options

```bash
scaffold --generate-scaffold --merge            # merges current structure into existing .scaffold
scaffold --generate-scaffold --overwrite        # replaces existing .scaffold
scaffold --generate-scaffold --rename-if-exists # renames new one to .scaffold_1, etc.
```

---

## 📝 Example `.scaffold`

```text
src/
  main.py
  utils/
    helpers.py
README.md
.gitignore
tests/
  test_main.py
```

Will create:

```
├── README.md
├── .gitignore
├── src
│   ├── main.py
│   └── utils
│       └── helpers.py
└── tests
    └── test_main.py
```

---

## 👨‍💻 Author

Built with 🔥 by **Blaine Winslow**
[@cbwinslow](https://github.com/cbwinslow)

MIT License

---

## 📣 Contributing / Roadmap

* [ ] Add template packs (`--template=fastapi`, `--template=flask`, etc.)
* [ ] Add syntax highlighting and IDE plugin
* [ ] Integrate `.scaffoldrc` for default configs
* [ ] GUI Wrapper

PRs and ideas welcome! 🎉
