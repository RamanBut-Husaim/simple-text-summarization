import math

from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import numpy as np

from tokenized_news_entry import TokenizedNewsEntry
from news_entry import NewsEntry

class NewsSummarizer:

    EXTRA_WEIGHT = 3

    def summarize(self, news: list[TokenizedNewsEntry]) -> list[NewsEntry]:
        news_entries = [self._summarize_news_entry(news_entry) for news_entry in news]
        return news_entries

    def _summarize_news_entry(self, news_entry: TokenizedNewsEntry) -> NewsEntry:
        sentence_count = self._calculate_sentence_count(len(news_entry.text_sentences))

        raw_sentences = [sentence.get_raw() for sentence in news_entry.text_sentences]
        vectorizer = TfidfVectorizer(tokenizer=nltk.word_tokenize)
        vector_matrix = vectorizer.fit_transform(raw_sentences)

        best_scoring_sentence_indexes = self._get_best_scoring_sentence_indexes(news_entry, vectorizer.vocabulary_, vector_matrix, sentence_count)
        best_scoring_sentences = self._extract_best_scoring_sentences(news_entry, best_scoring_sentence_indexes)

        return NewsEntry(news_entry.get_original_header(), best_scoring_sentences)

    def _get_best_scoring_sentence_indexes(self, news_entry: TokenizedNewsEntry, vocabulary: dict, vector_matrix, sentence_count: int) -> list[int]:
        mean_index_arr = []

        number_of_sentences = vector_matrix.shape[0]
        i = 0
        while i < number_of_sentences:
            sentence_vector = vector_matrix[i].toarray()
            adjusted_sentence_vector = self._adjust_sentence_vector_with_header_word_match_multiplier(news_entry, sentence_vector, vocabulary)
            sentence_vector_mean = self._calculate_sentence_vector_mean(adjusted_sentence_vector)
            mean_index_arr.append((sentence_vector_mean, i))
            i += 1

        sorted_means = sorted(mean_index_arr, key=lambda x: x[0], reverse=True)
        best_scoring_sentences = sorted_means[:sentence_count]

        return [mean_index[1] for mean_index in best_scoring_sentences]

    @staticmethod
    def _extract_best_scoring_sentences(news_entry: TokenizedNewsEntry, best_scoring_sentence_indexes: list[int]) -> list[str]:
        best_scoring_sentence_indexes = sorted(best_scoring_sentence_indexes)
        best_scoring_sentences = []

        for index in best_scoring_sentence_indexes:
            tokenized_sentence = news_entry.text_sentences[index]
            original_sentence = tokenized_sentence.original
            best_scoring_sentences.append(original_sentence)

        return best_scoring_sentences

    @staticmethod
    def _calculate_sentence_vector_mean(sentence_vector):
        np_sentence_vector = np.array(sentence_vector)
        np_sentence_vector = np_sentence_vector[np_sentence_vector != 0.0]
        if np_sentence_vector.size > 0:
            return np.mean(np_sentence_vector)
        else:
            return 0.0

    def _adjust_sentence_vector_with_header_word_match_multiplier(self, news_entry: TokenizedNewsEntry, sentence_vector: np.ndarray, vocabulary: dict) -> np.ndarray:
        new_sentence_vector = sentence_vector.copy()
        header_vocabulary = news_entry.get_header_vocabulary()

        for header_word in header_vocabulary:
            if header_word in vocabulary:
                index = vocabulary[header_word]
                new_sentence_vector[0][index] = sentence_vector[0][index] * self.EXTRA_WEIGHT

        return new_sentence_vector


    @staticmethod
    def _calculate_sentence_count(count: int) -> int:
        return round(math.sqrt(count))
