import unicodedata

def normalize_upper_no_accent(value: str) -> str:
    v = unicodedata.normalize("NFD", value)
    v = "".join(ch for ch in v if unicodedata.category(ch) != "Mn")
    return v.upper().strip()

def escape_like(value: str) -> str:
    return value.replace("%", r"\%").replace("_", r"\_")
