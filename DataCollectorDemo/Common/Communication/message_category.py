from enum import StrEnum

class MessageCategory(StrEnum):
    """Message categories to avoid trying to match typos."""
    ok = "ok"
    nok = "error"
    na = "na"