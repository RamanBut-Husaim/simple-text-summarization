class TokenizedSentence:
    _words: list[str] = []
    _original: str = ""

    def __init__(self, words: list[str], original: str):
        self._words = words
        self._original = original

    @property
    def words(self) -> list[str]:
        return self._words

    @property
    def original(self) -> str:
        return self._original

    def get_raw(self) -> str:
        return " ".join(self._words)
