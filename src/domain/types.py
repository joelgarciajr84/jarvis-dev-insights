from typing import Dict, List, Literal, Optional, TypedDict

class RepoMetrics(TypedDict):
    total_files: int
    sampled_lines: int
    languages: Dict[str, int]
    has_tests: bool
    has_ci: bool
    has_lint: bool
    has_tsconfig: bool

class TodoHit(TypedDict):
    file: str
    line: int
    snippet: str

ReviewSeverity = Literal["info", "warn", "crit"]

class ReviewIssue(TypedDict, total=False):
    rule_id: str
    message: str
    file: str
    line: Optional[int]
    severity: ReviewSeverity
    suggestion: Optional[str]

class ReviewReport(TypedDict):
    summary: Dict[str, int]
    issues: List[ReviewIssue]
