import json
import math
import random
import string
from typing import Dict, Optional, List, Tuple

from fedispam.database import Database

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


class SpamFilter:
    """NaiveBayes implementation for **binary classification**

    Reference: https://link.springer.com/chapter/10.1007/978-3-540-30549-1_43
    """

    log_prior: Optional[List[float]] = None
    log_posterior: Optional[Dict[str, List[float]]] = None
    log_default_prob: Optional[List[float]] = None

    def __init__(
        self, lang="english", outliar_threshold=3, random_confirmation_rate=0.05
    ):
        # Number of unknown words to classify as outliar
        self.outliar_threshold = outliar_threshold
        # Probability to keep a message for manual validation
        self.random_confirmation_rate = random_confirmation_rate

        self.lang = lang
        self.model_db = Database("model.db")
        self.outliar_db = Database("outliars.db")
        self.random_check_db = Database("preprocessed.db")

        self.nb_samples: List[int] = []
        self.word_counts: Dict[str, List[int]] = {}

    def start(self):
        self.model_db.open()
        self.outliar_db.open()
        self.random_check_db.open()

        model_information = self.model_db.extract_db()

        # We use "#" as prefix for special model information
        self.nb_samples.append(self.decode_int(model_information[b"#class0"]))
        self.nb_samples.append(self.decode_int(model_information[b"#class1"]))
        # We use "0/" as prefix for keywords in class 0 and "1/" for class 1
        for key, value in model_information.items():
            assert isinstance(key, bytes)
            dec_key = key[2:].decode()
            if dec_key.startswith("0/"):
                if self.word_counts.get(dec_key) is None:
                    self.word_counts[dec_key] = [self.decode_int(value), 0]
            elif dec_key.startswith("1/"):
                if self.word_counts.get(dec_key) is None:
                    self.word_counts[dec_key] = [0, self.decode_int(value)]

        self._update_log_prob()

    def stop(self):
        self.model_db.close()
        self.outliar_db.close()
        self.random_check_db.close()

    @staticmethod
    def encode_int(nb: int) -> bytes:
        return nb.to_bytes(8, byteorder="big")

    @staticmethod
    def decode_int(byte_string: bytes) -> int:
        return int.from_bytes(byte_string, byteorder="big")

    def encode_preprocessed(
        self, decision: int, message_word_count: Dict[str, int]
    ) -> str:
        enc_count = json.dumps(message_word_count)
        return str(decision) + "||" + enc_count

    def decode_preprocessed(self, enc_message: str) -> Tuple[int, Dict[str, int]]:
        enc_decision, enc_count = enc_message.split("||", 1)
        decision = int(enc_decision)
        message_word_count = json.loads(enc_count)
        return decision, message_word_count

    def _update_log_prob(self) -> None:
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

    async def update_model_database(
        self, updated_keys: Optional[List[str]] = None
    ) -> None:
        if updated_keys is None:  # Overwrite the whole database
            await self.model_db.del_all_keys()
            updated_keys = list(self.word_counts.keys())

        db_dict = {}
        # We use "#" as prefix for special model information
        db_dict["#class0"] = self.encode_int(self.nb_samples[0])
        db_dict["#class1"] = self.encode_int(self.nb_samples[1])

        for key in updated_keys:
            value_list = self.word_counts[key]
            db_dict["0/" + key] = self.encode_int(value_list[0])
            db_dict["1/" + key] = self.encode_int(value_list[0])

        await self.model_db.set_multiple_keys(db_dict)

    def _add_word_count_to_model(self, message_word_count, message_type):
        updated_keys = set()
        for word, count in message_word_count.items():
            curr_count = self.word_counts.get(word, [0, 0])
            curr_count[message_type] += count
            self.word_counts[word] = curr_count
            self.nb_samples[message_type] += 1
            updated_keys.add(word)

        return updated_keys

    async def add_training_data(self, data: List[Tuple[str, int]]):
        updated_keys = set()
        for message_content, decision in data:
            message_word_count = self._preprocess_text(message_content)
            updated_keys = updated_keys.union(
                self._add_word_count_to_model(message_word_count, decision)
            )

        await self.update_model_database(list(updated_keys))

    async def outliar_manual_confirmation(self, data: List[Tuple[str, int]]) -> None:
        updated_keys = set()
        for message_id, decision in data:
            enc = await self.outliar_db.get_and_del_key(message_id)
            message_word_count = json.loads(enc)
            updated_keys = updated_keys.union(
                self._add_word_count_to_model(message_word_count, decision)
            )

        await self.update_model_database(list(updated_keys))

    async def get_all_outliars(self) -> List[str]:
        outliars = await self.outliar_db.get_all_keys()
        return [outliar.decode() for outliar in outliars]

    async def random_check_manual_confirmation(
        self, data: List[Tuple[str, int]]
    ) -> None:
        updated_keys = set()
        for message_id, decision in data:
            enc = await self.random_check_db.get_and_del_key(message_id)
            message_word_count = json.loads(enc)
            updated_keys = updated_keys.union(
                self._add_word_count_to_model(message_word_count, decision)
            )

        await self.update_model_database(list(updated_keys))

    async def get_all_random_checks(self) -> List[Tuple[str, int]]:
        random_check_dict = await self.random_check_db.get_all_key_values()
        res = []
        for message_id, payload in random_check_dict.items():
            decision, _ = self.decode_preprocessed(payload.decode())
            res.append((message_id.decode(), decision))
        return res

    async def import_model(self, model) -> None:
        self.nb_samples = model["nb_samples"]
        self.word_counts = model["word_counts"]
        self._update_log_prob()
        await self.update_model_database()

    def export_model(self):
        model = {"nb_samples": self.nb_samples, "word_counts": self.word_counts}
        return model

    async def predict(self, message) -> int:
        """Predict whether a message is a spam or not.

        Possible outputs:
        -> 1 = Spam
        -> 0 = Ham
        -> -1 = Outliar
        """
        if self.log_posterior is None or self.log_prior is None:
            raise ValueError("Model must be trained first")

        sp_vect = self._preprocess_text(message["content"])

        log_prob_0 = self.log_prior[0]
        log_prob_1 = self.log_prior[1]

        outliar_count = 0

        for word, count in sp_vect.items():
            if word in self.log_posterior:
                log_posterior_0, log_posterior_1 = self.log_posterior[word]
                log_prob_0 += log_posterior_0 * count
                log_prob_1 += log_posterior_1 * count
            else:
                outliar_count += 1

        pred = int(log_prob_1 > log_prob_0)

        if outliar_count > self.outliar_threshold:
            pred = -1
            await self.outliar_db.set_key(message["id"], json.dumps(sp_vect))
        else:
            r = random.random()
            if r < self.random_confirmation_rate:

                await self.random_check_db.set_key(
                    message["id"], self.encode_preprocessed(pred, sp_vect)
                )

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
