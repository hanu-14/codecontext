import subprocess
import os


def get_git_info(root):
    info = {}
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-20"],
            capture_output=True, text=True, cwd=root, timeout=10
        )
        if result.returncode == 0:
            info["recent_commits"] = result.stdout.strip()
    except Exception:
        info["recent_commits"] = ""

    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, cwd=root, timeout=5
        )
        if result.returncode == 0:
            info["remote"] = result.stdout.strip()
    except Exception:
        info["remote"] = ""

    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, cwd=root, timeout=5
        )
        if result.returncode == 0:
            info["branch"] = result.stdout.strip()
    except Exception:
        info["branch"] = ""

    try:
        result = subprocess.run(
            ["git", "diff", "--stat"],
            capture_output=True, text=True, cwd=root, timeout=5
        )
        if result.returncode == 0:
            info["uncommitted"] = result.stdout.strip()
    except Exception:
        info["uncommitted"] = ""

    return info
