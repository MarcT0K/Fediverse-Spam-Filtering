import math
import string
from typing import Dict, Optional, List

from fedispam.database import ModelDatabase


STOPWORDS = [
    "i",
    "me",
    "my",
    "myself",
    "we",
    "our",
    "ours",
    "ourselves",
    "you",
    "your",
    "yours",
    "yourself",
    "yourselves",
    "he",
    "him",
    "his",
    "himself",
    "she",
    "her",
    "hers",
    "herself",
    "it",
    "its",
    "itself",
    "they",
    "them",
    "their",
    "theirs",
    "themselves",
    "what",
    "which",
    "who",
    "whom",
    "this",
    "that",
    "these",
    "those",
    "am",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "having",
    "do",
    "does",
    "did",
    "doing",
    "a",
    "an",
    "the",
    "and",
    "but",
    "if",
    "or",
    "because",
    "as",
    "until",
    "while",
    "of",
    "at",
    "by",
    "for",
    "with",
    "about",
    "against",
    "between",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "to",
    "from",
    "up",
    "down",
    "in",
    "out",
    "on",
    "off",
    "over",
    "under",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "when",
    "where",
    "why",
    "how",
    "all",
    "any",
    "both",
    "each",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "not",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "s",
    "t",
    "can",
    "will",
    "just",
    "don",
    "should",
    "now",
]


def strip_text(text):
    table = str.maketrans(dict.fromkeys(string.punctuation))
    return text.translate(table).lower()


class NaiveBayes:
    """NaiveBayes implementation for **binary classification**

    Reference: https://link.springer.com/chapter/10.1007/978-3-540-30549-1_43
    """

    log_prior: Optional[List[float]] = None
    nb_samples: Optional[List[int]] = None
    log_posterior: Optional[Dict[str, List[float]]] = None
    word_counts: Optional[Dict[str, List[int]]] = None
    log_default_prob: Optional[List[float]] = None

    def __init__(self, lang="english", outliar_threshold=3, db_file="model.db"):
        self.outliar_threshold = (
            outliar_threshold  # Number of unknown words to classify as outliar
        )
        self.lang = lang
        self.db = ModelDatabase(db_file)
        # TODO: import model from DB

    def _update_log_prob(self):
        assert self.word_counts is not None
        assert self.nb_samples is not None

        nb_nnz_features = len(self.word_counts.keys())

        self.log_prior = [0.0, 0.0]

        self.log_prior[0] = math.log(self.nb_samples[0]) - math.log(
            self.nb_samples[0] + self.nb_samples[1]
        )
        self.log_prior[1] = math.log(self.nb_samples[1]) - math.log(
            self.nb_samples[0] + self.nb_samples[1]
        )

        self.log_posterior = {}
        total_words = [0, 0]
        for count_0, count_1 in self.word_counts.values():
            total_words[0] += count_0
            total_words[1] += count_1

        self.log_default_prob = [0.0, 0.0]
        self.log_default_prob[0] = -math.log(total_words[0] + nb_nnz_features)
        self.log_default_prob[1] = -math.log(total_words[1] + nb_nnz_features)

        for word, (count_0, count_1) in self.word_counts.items():
            posterior_0 = math.log(1 + count_0) - math.log(
                total_words[0] + nb_nnz_features
            )

            posterior_1 = math.log(1 + count_1) - math.log(
                total_words[1] + nb_nnz_features
            )
            self.log_posterior[word] = [posterior_0, posterior_1]
            # Remark: we apply a Laplace smoothing on the probabilities to cover unknown words.

    def update_model_database(
        self, updated_keys: Optional[List[str]] = None
    ): ...  # TODO

    def add_training_data(self, data): ...  # TODO

    def import_model(self, nb_samples, word_counts):
        self.nb_samples = nb_samples
        self.word_counts = word_counts
        self._update_log_prob()
        self.update_model_database()

    def export_model(self):
        return self.nb_samples, self.word_counts

    def predict(self, message):
        """Predict whether a message is a spam or not.

        Possible outputs:
        -> 1 = Spam
        -> 0 = Ham
        -> -1 = Outliar
        """
        if self.log_posterior is None or self.log_prior is None:
            raise ValueError("Model must be trained first")

        sp_vect = self._preprocess_text(message)

        log_prob_0 = self.log_prior[0]
        log_prob_1 = self.log_prior[1]

        outliar_count = 0

        for word, count in sp_vect.items():
            if word in self.log_posterior:
                log_prob_0 += self.log_posterior[word][0] * count
                log_prob_1 += self.log_posterior[word][1] * count
            else:
                outliar_count += 1

        pred = int(log_prob_1 > log_prob_0)

        if outliar_count > self.outliar_threshold:
            pred = -1

        return pred

    def _preprocess_text(self, message):
        message = strip_text(message)
        sp_vect = {}
        words = message.split()
        for word in words:
            if word not in STOPWORDS:
                # Remark: we do not remove punctuation
                sp_vect[word] = sp_vect.get(word, 0) + 1

        return sp_vect
