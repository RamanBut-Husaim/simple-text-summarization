from bs4 import BeautifulSoup

from raw_news_entry import RawNewsEntry

class NewsParser:
    _supported_format: str = 'xml'

    def __init__(self, supported_format = "xml"):
        if supported_format != 'xml':
            raise ValueError("Format must be xml")

        self._supported_format = supported_format

    @property
    def supported_format(self) -> str:
        return self._supported_format

    def parse(self, content: str) -> list[RawNewsEntry]:
        doc = BeautifulSoup(content, 'lxml')
        raw_news_entries = doc.find_all('news')

        news_entries = [self._parse_entry(raw_news_entry) for raw_news_entry in raw_news_entries]

        return news_entries

    def _parse_entry(self, raw_news) -> RawNewsEntry:
        heads = raw_news.find_all('value', attrs={'name': 'head'})
        texts = raw_news.find_all('value', attrs={'name': 'text'})

        self._guard_entry_structure(heads, texts)

        return RawNewsEntry(heads[0].text, texts[0].text)

    @staticmethod
    def _guard_entry_structure(heads, texts):
        if len(heads) != 1:
            raise ValueError("There should be only one head element for news")

        if len(texts) != 1:
            raise ValueError("There should be only one text element for news")
