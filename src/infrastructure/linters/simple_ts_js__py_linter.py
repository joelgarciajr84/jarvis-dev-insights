import re
from typing import List
from ...domain.types import ReviewIssue
from ...domain.review_rules import (
    MAX_FN_LINES, MAX_LINE_LENGTH, MAGIC_NUMBER_THRESHOLD, CAMEL_CASE, jarvis_voice
)
from ..text_utils import split_lines
from ..dup_detector import detect_duplicate_blocks

CAMEL_RE = re.compile(CAMEL_CASE)

def to_camel(s: str) -> str:
    def repl(m: re.Match[str]) -> str:
        return m.group(1).upper()
    s2 = re.sub(r"[_-]+(.)", repl, s)
    return s2[0:1].lower() + s2[1:] if s2 else s2

def lint_ts_js_py(file_path: str, code: str) -> List[ReviewIssue]:
    issues: List[ReviewIssue] = []
    lines = split_lines(code)
    is_python = file_path.endswith('.py')

    for i, l in enumerate(lines):
        if len(l) > MAX_LINE_LENGTH:
            issues.append({
                "rule_id": "line-length",
                "severity": "info",
                "file": file_path,
                "line": i + 1,
                "message": f"Linha com {len(l)} colunas (>{MAX_LINE_LENGTH}).",
                "suggestion": jarvis_voice("quebrar a linha ou extrair subexpressões."),
            })

    num_matches = re.findall(r"\b\d+\b", code)
    if len(num_matches) >= MAGIC_NUMBER_THRESHOLD:
        issues.append({
            "rule_id": "magic-number",
            "severity": "warn",
            "file": file_path,
            "message": f"Muitos números literais ({len(num_matches)}).",
            "suggestion": jarvis_voice("extrair para constantes nomeadas."),
        })

    if is_python:
        # Check Python variable and function names (snake_case)
        py_names = [m.group(1) for m in re.finditer(r"\b(?:def|class)\s+([A-Za-z_][A-Za-z0-9_]*)", code)]
        py_vars = [m.group(1) for m in re.finditer(r"\b([a-z_][a-z0-9_]*)\s*=", code)]

        for name in py_names + py_vars:
            if not re.match(r"^[a-z_][a-z0-9_]*$", name) and not re.match(r"^[A-Z][A-Za-z0-9]*$", name):
                issues.append({
                    "rule_id": "naming",
                    "severity": "info",
                    "file": file_path,
                    "message": f"Nome '{name}' fora do padrão snake_case para Python.",
                    "suggestion": jarvis_voice(f"renomear usando snake_case (letras minúsculas e underscores)."),
                })
    else:
        # Check JS/TS variable names (camelCase)
        var_names = [m.group(2) for m in re.finditer(r"\b(const|let|var|function)\s+([A-Za-z_][A-Za-z0-9_]*)", code)]
        for name in var_names:
            if not CAMEL_RE.match(name) and not re.match(r"^[A-Z0-9_]+$", name):
                issues.append({
                    "rule_id": "naming",
                    "severity": "info",
                    "file": file_path,
                    "message": f"Nome '{name}' fora do padrão camelCase.",
                    "suggestion": jarvis_voice(f"renomear para camelCase (ex.: '{to_camel(name)}')."),
                })

    # Check function length for both Python and JS/TS
    if is_python:
        for m in re.finditer(r"def\s+[A-Za-z0-9_]*\s*\([^)]*\):[^\n]*\n((?:\s+[^\n]*\n)+)", code):
            body = m.group(1)
            fn_len = len(split_lines(body))
            if fn_len > MAX_FN_LINES:
                issues.append({
                    "rule_id": "fn-length",
                    "severity": "warn",
                    "file": file_path,
                    "message": f"Função com {fn_len} linhas (>{MAX_FN_LINES}).",
                    "suggestion": jarvis_voice("extrair funções menores."),
                })
    else:
        for m in re.finditer(r"function\s+[A-Za-z0-9_]*\s*\([^)]*\)\s*\{([\s\S]*?)\}", code):
            body = m.group(1)
            fn_len = len(split_lines(body))
            if fn_len > MAX_FN_LINES:
                issues.append({
                    "rule_id": "fn-length",
                    "severity": "warn",
                    "file": file_path,
                    "message": f"Função com {fn_len} linhas (>{MAX_FN_LINES}).",
                    "suggestion": jarvis_voice("extrair funções menores."),
                })

    dups = detect_duplicate_blocks(code, 6)
    if dups > 0:
        issues.append({
            "rule_id": "dup-blocks",
            "severity": "info",
            "file": file_path,
            "message": f"Blocos repetidos detectados (~{dups}).",
            "suggestion": jarvis_voice("centralizar lógica compartilhada (DRY)."),
        })

    return issues
