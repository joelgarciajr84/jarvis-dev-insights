from .text_utils import split_lines, hash_block

def detect_duplicate_blocks(code: str, window: int = 6) -> int:
    lines = split_lines(code)
    counts: dict[int, int] = {}
    for i in range(0, max(0, len(lines) - window + 1)):
        block = "\n".join(lines[i:i+window])
        h = hash_block(block)
        counts[h] = counts.get(h, 0) + 1
    return sum(1 for c in counts.values() if c > 1)
