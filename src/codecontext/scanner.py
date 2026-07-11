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


def should_ignore(name, root):
    path = os.path.join(root, name)
    if any(fnmatch.fnmatch(name, p) for p in IGNORE_PATTERNS):
        return True
    if os.path.islink(path):
        return True
    return False


def scan_tree(root, prefix="", max_files=200, _count=[0]):
    if _count[0] >= max_files:
        return []
    lines = []
    try:
        entries = sorted(os.listdir(root))
    except PermissionError:
        return lines

    entries = [e for e in entries if not should_ignore(e, root)]
    for i, name in enumerate(entries):
        if _count[0] >= max_files:
            break
        path = os.path.join(root, name)
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{name}")
        _count[0] += 1
        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            lines.extend(scan_tree(path, prefix + extension, max_files, _count))
    return lines


def get_tree(root, max_files=200):
    name = os.path.basename(os.path.abspath(root))
    lines = [name]
    lines.extend(scan_tree(root, max_files=max_files))
    return "\n".join(lines)


def find_key_files(root, max_size=50_000):
    key_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_ignore(d, dirpath)]
        for f in filenames:
            if should_ignore(f, dirpath):
                continue
            path = os.path.join(dirpath, f)
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
