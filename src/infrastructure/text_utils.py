def split_lines(txt: str) -> list[str]:
    return txt.splitlines()

def count_lines(txt: str) -> int:
    return len(split_lines(txt))

def hash_block(s: str) -> int:
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return h
