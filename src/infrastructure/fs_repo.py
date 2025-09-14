from __future__ import annotations
from pathlib import Path
from typing import Dict, List
from .text_utils import count_lines
from domain.types import RepoMetrics

LANG_MAP = {
    ".ts": "TypeScript", ".tsx": "TypeScript/React",
    ".js": "JavaScript", ".jsx": "JavaScript/React",
    ".py": "Python", ".go": "Go", ".rb": "Ruby",
    ".java": "Java", ".cs": "C#", ".rs": "Rust",
    ".md": "Markdown", ".json": "JSON", ".yml": "YAML", ".yaml": "YAML"
}

def walk(root: str) -> list[str]:
    files: list[str] = []
    for p in Path(root).rglob("*"):
        try:
            if p.is_file() and ".git" not in p.parts:
                files.append(str(p))
        except Exception:
            continue
    return files

def detect_lang_by_ext(files: List[str]) -> Dict[str, int]:
    buckets: Dict[str, int] = {}
    for f in files:
        ext = Path(f).suffix.lower()
        buckets[ext] = buckets.get(ext, 0) + 1
    out: Dict[str, int] = {}
    for ext, n in buckets.items():
        k = LANG_MAP.get(ext, ext.replace(".", "").upper() or "NOEXT")
        out[k] = out.get(k, 0) + n
    return out

def compute_repo_metrics(root: str) -> RepoMetrics:
    files = walk(root)
    sampled = files[:2000]
    sampled_lines = 0
    for f in sampled:
        try:
            sampled_lines += count_lines(Path(f).read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            pass

    has_tests = any(("__tests__" in f or "/test/" in f or "/tests/" in f or f.endswith((".test.ts", ".test.tsx", ".test.js", ".test.jsx"))) for f in files)
    has_ci = any("/.github/workflows/" in f or f.endswith("/azure-pipelines.yml") for f in files)
    has_lint = any(Path(root, name).exists() for name in [".eslintrc.js", ".eslintrc.cjs", ".eslintrc.json"])
    has_tsconfig = Path(root, "tsconfig.json").exists()

    return {
        "total_files": len(files),
        "sampled_lines": sampled_lines,
        "languages": detect_lang_by_ext(files),
        "has_tests": has_tests,
        "has_ci": has_ci,
        "has_lint": has_lint,
        "has_tsconfig": has_tsconfig,
    }
