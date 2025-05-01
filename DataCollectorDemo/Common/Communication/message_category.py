from enum import StrEnum

class MessageCategory(StrEnum):
    """Message categories to avoid trying to match typos."""
    ok = "ok"
    """Operation was performed as expected."""
    nok = "error"
    """Operation raised errors."""
    na = "na"
    """Rating of "ok" or "nok" is not applicable."""