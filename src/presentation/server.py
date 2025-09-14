import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastmcp import FastMCP
from application.usecases.scan_repo import ScanRepoUseCase
from application.usecases.find_todos import FindTodosUseCase
from application.usecases.summarize_md import SummarizeMdUseCase
from application.usecases.review_code import ReviewCodeUseCase
from domain.types import ReviewReport
from pathlib import Path

mcp = FastMCP(name="jarvis-dev-insights")

@mcp.tool()
def scan_repo(path: str) -> str:
    data = ScanRepoUseCase().execute(path)
    m = data["metrics"]
    return (
        "# Jarvis • Repo Scan\n"
        f"Arquivos: {m['total_files']}\n"
        f"Linhas (amostra): {m['sampled_lines']}\n"
        f"Linguagens: {m['languages']}\n"
        "Sinalizadores:\n"
        f"- Tests: {'✅' if m['has_tests'] else '❌'}\n"
        f"- CI: {'✅' if m['has_ci'] else '❌'}\n"
        f"- ESLint: {'✅' if m['has_lint'] else '❌'}\n"
        f"- tsconfig.json: {'✅' if m['has_tsconfig'] else '❌'}"
    )

@mcp.tool()
def find_todos(path: str) -> str:
    hits = FindTodosUseCase().execute(path)["hits"]
    if not hits:
        return "Nenhum TODO/FIXME encontrado."
    parts = []
    for h in hits[:100]:
        parts.append(f"• {h['file']}:{h['line']}\n{h['snippet']}")
    return "\n---\n".join(parts)

@mcp.tool()
def summarize_md(path: str) -> str:
    return SummarizeMdUseCase().execute(path)["outline"]

@mcp.tool()
def review_code(path: str) -> ReviewReport:
    print("Reviewing code at:", path)
    report = ReviewCodeUseCase().execute(path)
    return report

@mcp.resource("repo://readme")
def readme_resource() -> str:
    p = Path("README.md")
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else "README.md não encontrado."

if __name__ == "__main__":
    mcp.run()
