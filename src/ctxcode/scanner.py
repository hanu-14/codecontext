import os
import fnmatch


IGNORE_PATTERNS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv", "env",
    ".tox", ".eggs", "*.egg-info", "dist", "build", ".next",
    ".nuxt", "target", "bin", "obj", ".idea", ".vscode",
    "*.pyc", "*.pyo", "*.so", "*.dll", "*.dylib",
    "*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg", "*.ico",
    "*.ttf", "*.woff", "*.woff2", "*.eot",
    "*.zip", "*.tar", "*.gz", "*.7z", "*.rar",
    ".DS_Store", "Thumbs.db", "*.lock", "package-lock.json",
    "*.min.js", "*.min.css", "*.map",
    ".coverage", ".pytest_cache", ".mypy_cache", ".ruff_cache",
}

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg",
    ".ttf", ".woff", ".woff2", ".eot",
    ".zip", ".tar", ".gz", ".7z", ".rar",
    ".so", ".dll", ".dylib", ".exe", ".bin",
    ".pyc", ".pyo",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".mp3", ".mp4", ".avi", ".mov",
    ".woff2", ".woff", ".eot",
    ".map", ".min.js", ".min.css",
}

CONFIG_FILENAMES = [".codecontext.toml", ".codecontext.json", ".codecontext.yml", ".codecontext.yaml"]


def should_ignore(name, extra_patterns=None):
    if any(fnmatch.fnmatch(name, p) for p in IGNORE_PATTERNS):
        return True
    if extra_patterns:
        for p in extra_patterns:
            if fnmatch.fnmatch(name, p):
                return True
    return False


def _format_size(size):
    if size < 1024:
        return f"{size}B"
    elif size < 1024 ** 2:
        return f"{size / 1024:.0f}KB"
    elif size < 1024 ** 3:
        return f"{size / 1024 ** 2:.1f}MB"
    return f"{size / 1024 ** 3:.1f}GB"


def scan_tree(root, prefix="", max_files=200, _count=None, extra_ignore=None, show_hidden=False):
    if _count is None:
        _count = [0]
    if _count[0] >= max_files:
        return []
    lines = []
    try:
        entries = sorted(os.listdir(root))
    except PermissionError:
        return lines

    entries = [e for e in entries if not should_ignore(e, extra_ignore)]
    if not show_hidden:
        entries = [e for e in entries if not e.startswith(".") or e in (".gitignore", ".env.example")]

    for i, name in enumerate(entries):
        if _count[0] >= max_files:
            break
        path = os.path.join(root, name)
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "

        if os.path.isdir(path):
            lines.append(f"{prefix}{connector}{name}/")
            _count[0] += 1
            extension = "    " if is_last else "│   "
            lines.extend(scan_tree(path, prefix + extension, max_files, _count, extra_ignore, show_hidden))
        elif os.path.isfile(path):
            try:
                size = os.path.getsize(path)
                size_str = _format_size(size)
            except OSError:
                size_str = "?"
            lines.append(f"{prefix}{connector}{name} ({size_str})")
            _count[0] += 1
    return lines


def get_tree(root, max_files=200, extra_ignore=None, show_hidden=False):
    name = os.path.basename(os.path.abspath(root))
    lines = [f"{name}/"]
    lines.extend(scan_tree(root, max_files=max_files, extra_ignore=extra_ignore, show_hidden=show_hidden))
    return "\n".join(lines)


def find_key_files(root, max_size=50_000, extra_ignore=None):
    key_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_ignore(d, extra_ignore)]
        for f in filenames:
            if should_ignore(f, extra_ignore):
                continue
            path = os.path.join(dirpath, f)
            ext = os.path.splitext(f)[1].lower()
            if ext in BINARY_EXTENSIONS:
                continue
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            if size > max_size:
                continue
            rel = os.path.relpath(path, root)
            key_files.append((rel, path))
    key_files.sort()
    return key_files


def read_file(path, max_lines=200):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            lines.append(f"... ({len(lines)} lines shown, truncated)\n")
        return "".join(lines)
    except Exception as e:
        return f"// Error reading file: {e}\n"


def load_config(root):
    for filename in CONFIG_FILENAMES:
        path = os.path.join(root, filename)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
            if filename.endswith(".toml"):
                try:
                    import tomllib
                    return tomllib.loads(raw)
                except ImportError:
                    import tomli as tomllib
                    return tomllib.loads(raw)
            elif filename.endswith(".json"):
                import json
                return json.loads(raw)
            elif filename.endswith((".yml", ".yaml")):
                import yaml
                return yaml.safe_load(raw)
        except Exception:
            pass
    return {}
