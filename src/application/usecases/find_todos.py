from pathlib import Path
import re
from infrastructure.fs_repo import walk
from domain.types import TodoHit

class FindTodosUseCase:
    def execute(self, root: str):
        files = [f for f in walk(root) if not f.endswith(".md")]
        hits: list[TodoHit] = []
        for f in files[:1500]:
            try:
                txt = Path(f).read_text(encoding="utf-8", errors="ignore")
                lines = txt.splitlines()
                for i, line in enumerate(lines):
                    if re.search(r"(TODO|FIXME)", line, re.IGNORECASE):
                        start = max(0, i - 1)
                        end = min(len(lines), i + 2)
                        hits.append({"file": f, "line": i + 1, "snippet": "\n".join(lines[start:end])})
            except Exception:
                pass
        return {"hits": hits}
