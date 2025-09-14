from pathlib import Path
import re

class SummarizeMdUseCase:
    def execute(self, path: str):
        p = Path(path)
        if not p.exists():
            return {"outline": f"Arquivo não encontrado: {path}"}
        lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        headings = []
        for l in lines:
            m = re.match(r"^(#{1,3})\s+(.*)", l)
            if m:
                indent = "  " * (len(m.group(1)) - 1)
                headings.append(f"{indent}- {m.group(2)}")
        return {"outline": "\n".join(headings) or "Sem headings H1–H3."}
