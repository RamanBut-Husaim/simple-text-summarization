from tokenized_sentence import TokenizedSentence

class TokenizedNewsEntry:
    _header: list[TokenizedSentence] = []
    _sentences: list[TokenizedSentence] = []

    def __init__(self, header: list[TokenizedSentence], sentences: list[TokenizedSentence]):
        self._header = header
        self._sentences = sentences

    @property
    def header_sentences(self):
        return self._header

    @property
    def text_sentences(self):
        return self._sentences

    def get_original_header(self):
        original_header_sentences = [header.original for header in self._header]
        return " ".join(original_header_sentences)

    def get_header_vocabulary(self):
        header_vocabulary = set()
        for header_sentence in self._header:
            for header_word in header_sentence.words:
                header_vocabulary.add(header_word)

        return header_vocabulary
