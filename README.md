# codecontext

<p align="center">
  <b>Extract your codebase context for AI assistants.</b><br>
  <a href="https://github.com/hanu-14/codecontext/actions/workflows/ci.yml">
    <img src="https://github.com/hanu-14/codecontext/actions/workflows/ci.yml/badge.svg" alt="CI">
  </a>
  <img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
  <img src="https://img.shields.io/badge/dependencies-0-brightgreen" alt="Zero dependencies">
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

# Exclude git info
codecontext --no-git

# Adjust limits
codecontext --max-files 100 --max-lines 150

# Save to file
codecontext -o context.md
```

### Short alias

```bash
ctx          # same as codecontext
ctx ./src    # specific directory
```

## Output

The tool produces a structured markdown document with:

1. **Project metadata** — path, git remote, branch
2. **Git history** — recent commits and uncommitted changes
3. **File tree** — clean visual tree of your project
4. **Key files** — source files with syntax highlighting

Perfect for pasting directly into Claude, ChatGPT, or any AI coding assistant.

## Features

- **Zero dependencies** — pure Python, no pip installs beyond this package
- **Smart ignore** — automatically skips `.git`, `node_modules`, `__pycache__`, binaries, and more
- **Git aware** — includes branch, remote, recent commits, and diff stats
- **File limit safety** — won't overwhelm your context window
- **Language detection** — syntax-highlighted code blocks for 30+ languages

## Example

```bash
$ ctx
```

Produces:

```
# Codebase Context

Generated from: `/Users/me/my-project`
Remote: `git@github.com:user/my-project.git`
Branch: `main`

Recent commits:
abc1234 feat: add user authentication
def5678 fix: resolve payment timeout

## Project Structure

my-project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
├── pyproject.toml
└── README.md

## Key Files
...
```

## License

MIT
