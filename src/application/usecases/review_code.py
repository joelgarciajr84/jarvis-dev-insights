from pathlib import Path
from infrastructure.fs_repo import walk
from infrastructure.linters.simple_ts_js__py_linter import lint_ts_js_py
from domain.types import ReviewReport, ReviewIssue

class ReviewCodeUseCase:
    def execute(self, root: str) -> ReviewReport:
        files = [f for f in walk(root) if Path(f).suffix.lower() in (".ts", ".tsx", ".js", ".jsx", ".py")]
        issues: list[ReviewIssue] = []
        for f in files[:1200]:
            try:
                code = Path(f).read_text(encoding="utf-8", errors="ignore")
                issues.extend(lint_ts_js_py(f, code))
            except Exception:
                pass
        return {"summary": {"filesScanned": len(files), "issues": len(issues)}, "issues": issues}
