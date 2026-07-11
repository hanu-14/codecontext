# codecontext

<p align="center">
  <b>Extract your codebase context for AI assistants.</b><br>
  <a href="https://github.com/hanu-14/codecontext/actions/workflows/ci.yml">
    <img src="https://github.com/hanu-14/codecontext/actions/workflows/ci.yml/badge.svg" alt="CI">
  </a>
  <img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
  <img src="https://img.shields.io/badge/dependencies-0-brightgreen" alt="Zero dependencies">
  <img src="https://img.shields.io/badge/version-0.2.0-blue" alt="v0.2.0">
</p>

A zero-dependency CLI tool that packages your project structure, key files, and git history into a formatted prompt for Claude, ChatGPT, and other AI coding assistants.

```bash
pip install codecontext
cd my-project
codecontext
```

## Why?

When asking AI assistants about your code, you spend minutes copy-pasting file trees, key files, and git history. `codecontext` does it in one command — giving the AI full project context for better answers.

## Install

```bash
pip install codecontext
```

Or run directly:

```bash
curl -O https://raw.githubusercontent.com/hanu-14/codecontext/main/src/codecontext/cli.py
python cli.py
```

## Usage

```bash
# Full context (tree + files + git history)
codecontext

# Specific project
codecontext path/to/project

# Output formats
codecontext --format markdown    # default - ready for AI chat
codecontext --format plain       # plain text
codecontext --format json        # machine-readable

# Copy to clipboard
codecontext --clipboard

# Save to file
codecontext -o context.md

# Exclude custom patterns
codecontext --exclude "*.log" "tmp/" "*.csv"

# Show hidden files
codecontext --hidden

# Exclude git info
codecontext --no-git

# Adjust limits
codecontext --max-files 100 --max-lines 150
```

### Short alias

```bash
ctx                # same as codecontext
ctx ./src          # specific directory
ctx --clipboard    # copy to clipboard
```

## Configuration

Place a `.codecontext.toml` in your project root:

```toml
git = true
max_files = 300
max_lines = 250
format = "markdown"
exclude = ["*.log", "tmp/"]
hidden = false
```

JSON and YAML formats are also supported (`.codecontext.json`, `.codecontext.yml`).

## Output

The tool produces a structured document with:

1. **Project metadata** — path, git remote, branch
2. **Git history** — recent commits and uncommitted changes
3. **File tree** — with file sizes for every entry
4. **Key files** — source files with syntax highlighting
5. **Stats summary** — total files and size at a glance

Perfect for pasting directly into Claude, ChatGPT, or any AI coding assistant.

## Features

- **Zero dependencies** — pure Python, no pip installs beyond this package
- **Smart ignore** — automatically skips `.git`, `node_modules`, `__pycache__`, binaries, and more
- **Git aware** — includes branch, remote, recent commits, and diff stats
- **File limit safety** — won't overwhelm your context window
- **Language detection** — syntax-highlighted code blocks for 30+ languages
- **Clipboard support** — `--clipboard` copies output directly to your clipboard
- **Multiple formats** — markdown, plain text, or JSON
- **Config file** — project-specific settings via `.codecontext.toml`
- **Custom excludes** — ignore additional patterns with `--exclude`
- **File sizes** — every file in the tree shows its size

## Example

```bash
$ codecontext --format markdown
```

Produces:

```
# Codebase Context

Generated from: /Users/me/my-project
Remote: git@github.com:user/my-project.git
Branch: main

Recent commits:
abc1234 feat: add user authentication
def5678 fix: resolve payment timeout

## Project Structure

my-project/
├── src/
│   ├── main.py (2KB)
│   └── utils.py (1KB)
├── tests/
│   └── test_main.py (3KB)
├── pyproject.toml (1KB)
└── README.md (3KB)

## Key Files (6 files, 10KB)

### `src/main.py`

```python
def greet(name):
    return f"Hello, {name}!"
```

...
```

## Changelog

### v0.2.0
- Clipboard support (`--clipboard`)
- Multiple output formats: markdown, plain, JSON
- Configuration file support (`.codecontext.toml`, `.json`, `.yml`)
- File sizes in tree output
- Custom exclude patterns (`--exclude`)
- Hidden files flag (`--hidden`)
- Stats summary in output

### v0.1.0
- Initial release
- File tree with smart ignore patterns
- Git history integration
- Syntax highlighting for 30+ languages
- CLI alias `ctx`

## License

MIT
