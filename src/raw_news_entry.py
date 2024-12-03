class RawNewsEntry:
    _header: str = ""
    _text: str = ""

    def __init__(self, header: str, text: str):
        self._header = header
        self._text = text

    @property
    def header(self):
        return self._header

    @property
    def text(self):
        return self._text
