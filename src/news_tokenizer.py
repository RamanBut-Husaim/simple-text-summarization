import string

from tokenized_news_entry import TokenizedNewsEntry
from raw_news_entry import RawNewsEntry
from tokenized_sentence import TokenizedSentence
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer

class NewsTokenizer:
    def __init__(self):
        self._lemmatizer = WordNetLemmatizer()
        pass

    @staticmethod
    def initialize():
        nltk.download('punkt')
        nltk.download('stopwords')
        pass

    def tokenize(self, news: list[RawNewsEntry]) -> list[TokenizedNewsEntry]:
        sentence_tokenized_news = [self._tokenize_news_entry_by_sentences(entry) for entry in news]
        tokenized_news = [self._tokenize_news_entry_with_sentences(news_entry) for news_entry in sentence_tokenized_news]

        return tokenized_news

    @staticmethod
    def _tokenize_news_entry_by_sentences(news_entry: RawNewsEntry) -> tuple[str, str]:
        header_sentences = sent_tokenize(news_entry.header)
        text_sentences = sent_tokenize(news_entry.text)

        return header_sentences, text_sentences

    def _tokenize_news_entry_with_sentences(self, raw_news_entry: tuple[str, str]) -> TokenizedNewsEntry:
        header_sentences, text_sentences = raw_news_entry
        text_tokenized_sentences = [self._tokenize_news_entry_sentence_by_words(raw_sentence) for raw_sentence in text_sentences]
        header_tokenized_sentences = [self._tokenize_news_entry_sentence_by_words(raw_sentence) for raw_sentence in header_sentences]
        return TokenizedNewsEntry(header_tokenized_sentences, text_tokenized_sentences)

    def _tokenize_news_entry_sentence_by_words(self, raw_sentence: str) -> TokenizedSentence:
        words = nltk.word_tokenize(raw_sentence)
        words = [word.lower() for word in words]
        words_without_punctuation = [word for word in words if word not in string.punctuation]
        english_stopwords = stopwords.words('english')
        words_without_punctuation_and_stopwords = [word for word in words_without_punctuation if word not in english_stopwords]

        lemmatized_words = [self._lemmatizer.lemmatize(word) for word in words_without_punctuation_and_stopwords]

        return TokenizedSentence(lemmatized_words, raw_sentence)
