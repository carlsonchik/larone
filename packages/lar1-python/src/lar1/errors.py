"""LAR-1 parse errors."""


class Lar1ParseError(Exception):
    def __init__(self, code: str, message: str | None = None) -> None:
        self.code = code
        super().__init__(message or code)
