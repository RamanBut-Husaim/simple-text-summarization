class NewsEntry:
    _header: str = ""
    _sentences: list[str] = []

    def __init__(self, header: str, sentences: list[str]):
        self._header = header
        self._sentences = sentences

    @property
    def header(self):
        return self._header

    @property
    def sentences(self):
        return self._sentences
