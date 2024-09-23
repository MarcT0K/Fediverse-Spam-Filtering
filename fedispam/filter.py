import json
import math
import random
import re
from typing import Dict, Optional, List, Tuple

from fedispam.database import Database

URL_REGEX = r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
LINKREGEX = re.compile(r"<a\s*href=['|\"](.*?)['\"].*?>")
PUNCTUATION = r'!"#%&\'()*,-./:;?@[\\]_{}¡§«¶·»¿;·՚՛՜՝՞՟։֊־׀׃׆׳״؉؊،؍؛؞؟٪٫٬٭۔܀܁܂܃܄܅܆܇܈܉܊܋܌܍߷߸߹࠰࠱࠲࠳࠴࠵࠶࠷࠸࠹࠺࠻࠼࠽࠾࡞।॥॰৽੶૰౷಄෴๏๚๛༄༅༆༇༈༉༊་༌།༎༏༐༑༒༔༺༻༼༽྅࿐࿑࿒࿓࿔࿙࿚၊။၌၍၎၏჻፠፡።፣፤፥፦፧፨᐀᙮᚛᚜᛫᛬᛭᜵᜶។៕៖៘៙៚᠀᠁᠂᠃᠄᠅᠆᠇᠈᠉᠊᥄᥅᨞᨟᪠᪡᪢᪣᪤᪥᪦᪨᪩᪪᪫᪬᪭᭚᭛᭜᭝᭞᭟᭠᯼᯽᯾᯿᰻᰼᰽᰾᰿᱾᱿᳀᳁᳂᳃᳄᳅᳆᳇᳓‐‑‒–—―‖‗‘’‚‛“”„‟†‡•‣․‥…‧‰‱′″‴‵‶‷‸‹›※‼‽‾‿⁀⁁⁂⁃⁅⁆⁇⁈⁉⁊⁋⁌⁍⁎⁏⁐⁑⁓⁔⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞⁽⁾₍₎⌈⌉⌊⌋〈〉❨❩❪❫❬❭❮❯❰❱❲❳❴❵⟅⟆⟦⟧⟨⟩⟪⟫⟬⟭⟮⟯⦃⦄⦅⦆⦇⦈⦉⦊⦋⦌⦍⦎⦏⦐⦑⦒⦓⦔⦕⦖⦗⦘⧘⧙⧚⧛⧼⧽⳹⳺⳻⳼⳾⳿⵰⸀⸁⸂⸃⸄⸅⸆⸇⸈⸉⸊⸋⸌⸍⸎⸏⸐⸑⸒⸓⸔⸕⸖⸗⸘⸙⸚⸛⸜⸝⸞⸟⸠⸡⸢⸣⸤⸥⸦⸧⸨⸩⸪⸫⸬⸭⸮⸰⸱⸲⸳⸴⸵⸶⸷⸸⸹⸺⸻⸼⸽⸾⸿⹀⹁⹂⹃⹄⹅⹆⹇⹈⹉⹊⹋⹌⹍⹎⹏⹒、。〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〽゠・꓾꓿꘍꘎꘏꙳꙾꛲꛳꛴꛵꛶꛷꡴꡵꡶꡷꣎꣏꣸꣹꣺꣼꤮꤯꥟꧁꧂꧃꧄꧅꧆꧇꧈꧉꧊꧋꧌꧍꧞꧟꩜꩝꩞꩟꫞꫟꫰꫱꯫﴾﴿︐︑︒︓︔︕︖︗︘︙︰︱︲︳︴︵︶︷︸︹︺︻︼︽︾︿﹀﹁﹂﹃﹄﹅﹆﹇﹈﹉﹊﹋﹌﹍﹎﹏﹐﹑﹒﹔﹕﹖﹗﹘﹙﹚﹛﹜﹝﹞﹟﹠﹡﹣﹨﹪﹫！＂＃％＆＇（）＊，－．／：；？＠［＼］＿｛｝｟｠｡｢｣､･𐄀𐄁𐄂𐎟𐏐𐕯𐡗𐤟𐤿𐩐𐩑𐩒𐩓𐩔𐩕𐩖𐩗𐩘𐩿𐫰𐫱𐫲𐫳𐫴𐫵𐫶𐬹𐬺𐬻𐬼𐬽𐬾𐬿𐮙𐮚𐮛𐮜𐺭𐽕𐽖𐽗𐽘𐽙𑁇𑁈𑁉𑁊𑁋𑁌𑁍𑂻𑂼𑂾𑂿𑃀𑃁𑅀𑅁𑅂𑅃𑅴𑅵𑇅𑇆𑇇𑇈𑇍𑇛𑇝𑇞𑇟𑈸𑈹𑈺𑈻𑈼𑈽𑊩𑑋𑑌𑑍𑑎𑑏𑑚𑑛𑑝𑓆𑗁𑗂𑗃𑗄𑗅𑗆𑗇𑗈𑗉𑗊𑗋𑗌𑗍𑗎𑗏𑗐𑗑𑗒𑗓𑗔𑗕𑗖𑗗𑙁𑙂𑙃𑙠𑙡𑙢𑙣𑙤𑙥𑙦𑙧𑙨𑙩𑙪𑙫𑙬𑜼𑜽𑜾𑠻𑥄𑥅𑥆𑧢𑨿𑩀𑩁𑩂𑩃𑩄𑩅𑩆𑪚𑪛𑪜𑪞𑪟𑪠𑪡𑪢𑱁𑱂𑱃𑱄𑱅𑱰𑱱𑻷𑻸𑿿𒑰𒑱𒑲𒑳𒑴𖩮𖩯𖫵𖬷𖬸𖬹𖬺𖬻𖭄𖺗𖺘𖺙𖺚𖿢𛲟𝪇𝪈𝪉𝪊𝪋𞥞𞥟'

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


class SpamFilter:
    """NaiveBayes implementation for **binary classification**

    Reference: https://link.springer.com/chapter/10.1007/978-3-540-30549-1_43
    """

    log_prior: Optional[List[float]] = None
    log_posterior: Optional[Dict[str, List[float]]] = None
    log_default_prob: Optional[List[float]] = None
    nb_samples: Optional[List[int]] = None
    feature_counts: Optional[Dict[str, List[int]]] = None

    def __init__(self, lang="english", outliar_threshold=3, random_check_rate=0.05):
        # Number of unknown words to classify as outliar
        self.outliar_threshold = outliar_threshold
        # Probability to keep a status for manual validation
        self.random_check_rate = random_check_rate

        self.lang = lang

        self.outliar_db = Database("outliers.db")
        self.random_checks_db = Database("random_checks.db")
        self.model_db = Database("model.db")

    def start(self):
        self.outliar_db.open()
        self.random_checks_db.open()
        self.model_db.open()

        # Default values
        self.nb_samples = [0, 0]
        self.feature_counts = {}

        model_information = self.model_db.extract_db()
        if model_information:
            # We use "#" as prefix for special model information
            self.nb_samples[0] = self.decode_int(model_information[b"#class0"])
            self.nb_samples[1] = self.decode_int(model_information[b"#class1"])
            # We use "0/" as prefix for keywords in class 0 and "1/" for class 1
            for key, value in model_information.items():
                assert isinstance(key, bytes)
                dec_feat = key[2:].decode()
                if key.startswith(b"0/"):
                    feature_values = self.feature_counts.get(dec_feat, [0, 0])
                    feature_values[0] = self.decode_int(value)
                    self.feature_counts[dec_feat] = feature_values
                elif key.startswith(b"1/"):
                    feature_values = self.feature_counts.get(dec_feat, [0, 0])
                    feature_values[1] = self.decode_int(value)
                    self.feature_counts[dec_feat] = feature_values

        self._update_log_prob()

    def stop(self):
        self.model_db.close()
        self.outliar_db.close()
        self.random_checks_db.close()

    @staticmethod
    def encode_int(nb: int) -> bytes:
        return nb.to_bytes(8, byteorder="big")

    @staticmethod
    def decode_int(byte_string: bytes) -> int:
        return int.from_bytes(byte_string, byteorder="big")

    def encode_preprocessed(
        self, decision: int, status_features: Dict[str, int]
    ) -> str:
        enc_count = json.dumps(status_features)
        return str(decision) + "||" + enc_count

    def decode_preprocessed(self, enc_status: str) -> Tuple[int, Dict[str, int]]:
        enc_decision, enc_count = enc_status.split("||", 1)
        decision = int(enc_decision)
        status_features = json.loads(enc_count)
        return decision, status_features

    def _update_log_prob(self) -> None:
        assert self.feature_counts is not None
        assert self.nb_samples is not None

        nb_nnz_features = len(self.feature_counts.keys())

        self.log_prior = [-math.inf, -math.inf]

        if self.nb_samples[0] != 0:
            self.log_prior[0] = math.log(self.nb_samples[0]) - math.log(
                self.nb_samples[0] + self.nb_samples[1]
            )

        if self.nb_samples[1] != 0:
            self.log_prior[1] = math.log(self.nb_samples[1]) - math.log(
                self.nb_samples[0] + self.nb_samples[1]
            )

        self.log_posterior = {}
        total_words = [0, 0]
        for count_0, count_1 in self.feature_counts.values():
            total_words[0] += count_0
            total_words[1] += count_1

        self.log_default_prob = [0.0, 0.0]
        if nb_nnz_features != 0:
            self.log_default_prob[0] = -math.log(total_words[0] + nb_nnz_features)
            self.log_default_prob[1] = -math.log(total_words[1] + nb_nnz_features)

        for word, (count_0, count_1) in self.feature_counts.items():
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
            updated_keys = list(self.feature_counts.keys())

        db_dict = {}
        # We use "#" as prefix for special model information
        db_dict["#class0"] = self.encode_int(self.nb_samples[0])
        db_dict["#class1"] = self.encode_int(self.nb_samples[1])

        for key in updated_keys:
            value_list = self.feature_counts[key]
            db_dict["0/" + key] = self.encode_int(value_list[0])
            db_dict["1/" + key] = self.encode_int(value_list[1])

        await self.model_db.set_multiple_keys(db_dict)

    async def _update_model(self, model_update):
        self.nb_samples[0] += model_update["nb_samples"][0]
        self.nb_samples[1] += model_update["nb_samples"][1]

        for feature, counts in model_update["feature_counts"].items():
            curr_counts = self.feature_counts.get(feature, [0, 0])
            curr_counts[0] += counts[0]
            curr_counts[1] += counts[1]
            self.feature_counts[feature] = curr_counts

        self._update_log_prob()
        await self.update_model_database(model_update["feature_counts"].keys())

    @staticmethod
    def __feature_dictionary_update(feat_dict, status_features, status_type):
        for feature, count in status_features.items():
            curr_count = feat_dict.get(feature, [0, 0])
            curr_count[status_type] += count
            feat_dict[feature] = curr_count
        return feat_dict

    async def add_training_data(self, data: List[Tuple[Dict, int]]):
        model_update = {"nb_samples": [0, 0], "feature_counts": {}}
        for status, decision in data:
            status_features = self._extract_features_from_status(status)
            model_update["nb_samples"][decision] += 1
            model_update["feature_counts"] = SpamFilter.__feature_dictionary_update(
                model_update["feature_counts"], status_features, decision
            )

        await self._update_model(model_update)

    async def outliar_manual_confirmation(self, data: List[Tuple[str, int]]) -> None:
        model_update = {"nb_samples": [0, 0], "feature_counts": {}}
        for status_id, decision in data:
            enc = await self.outliar_db.get_val_and_del_key(status_id)
            status_features = json.loads(enc)
            model_update["nb_samples"][decision] += 1
            model_update["feature_counts"] = SpamFilter.__feature_dictionary_update(
                model_update["feature_counts"], status_features, decision
            )

        await self._update_model(model_update)

    async def get_all_outliers(self) -> List[str]:
        outliers = await self.outliar_db.get_all_keys()
        return [outliar.decode() for outliar in outliers]

    async def random_checks_manual_confirmation(
        self, data: List[Tuple[str, int]]
    ) -> None:
        model_update = {"nb_samples": [0, 0], "feature_counts": {}}
        for status_id, decision in data:
            enc = await self.random_checks_db.get_val_and_del_key(status_id)
            _prev_decision, status_features = self.decode_preprocessed(enc.decode())
            model_update["nb_samples"][decision] += 1
            model_update["feature_counts"] = SpamFilter.__feature_dictionary_update(
                model_update["feature_counts"], status_features, decision
            )

        await self._update_model(model_update)

    async def get_all_random_checkss(self) -> List[Tuple[str, int]]:
        random_checks_dict = await self.random_checks_db.get_all_key_values()
        res = []
        for status_id, payload in random_checks_dict.items():
            decision, _ = self.decode_preprocessed(payload.decode())
            res.append((status_id.decode(), decision))
        return res

    async def import_model(self, model) -> None:
        self.nb_samples = model["nb_samples"]
        self.feature_counts = model["feature_counts"]
        self._update_log_prob()
        await self.update_model_database()

    def export_model(self):
        model = {"nb_samples": self.nb_samples, "feature_counts": self.feature_counts}
        return model

    async def predict(self, status) -> int:
        """Predict whether a status is a spam or not.

        Possible outputs:
        -> 1 = Spam
        -> 0 = Ham
        -> -1 = Outliar
        """
        features = self._extract_features_from_status(status)

        log_prob_0 = self.log_prior[0]
        log_prob_1 = self.log_prior[1]

        outliar_count = 0

        for feat, count in features.items():
            if feat in self.log_posterior:
                log_posterior_0, log_posterior_1 = self.log_posterior[feat]
                log_prob_0 += log_posterior_0 * count
                log_prob_1 += log_posterior_1 * count
            else:
                if feat.startswith("content#"):
                    # We count outliars only in the content field
                    outliar_count += 1

        pred = int(log_prob_1 > log_prob_0)

        if outliar_count > self.outliar_threshold:
            pred = -1
            await self.outliar_db.set_key(status["id"], json.dumps(features))
        else:
            r = random.random()
            if r < self.random_check_rate:

                await self.random_checks_db.set_key(
                    status["id"], self.encode_preprocessed(pred, features)
                )

        return pred

    def _extract_features_from_status(self, status: Dict):
        features = {}

        def extract_features_from_text(text, prefix):
            table = str.maketrans(PUNCTUATION, " " * len(PUNCTUATION))
            stripped_text = text.translate(table).lower()
            for word in stripped_text.split():
                if word not in STOPWORDS:
                    # Remark: we do not remove punctuation
                    features[prefix + "#" + word] = features.get(word, 0) + 1

        # Process content
        ## URL counting
        mention_urls = [mention["url"] for mention in status["mentions"]]
        url_count = 0
        for url in LINKREGEX.findall(status["content"]):
            if url not in mention_urls:
                url_count += 1
        features["urls#"] = url_count
        content = re.sub(
            r"<a[^>]*>(.*?)</a>", "", status["content"]
        )  # remove <a> tags (i.e., URLs) and their content

        stripped_html = re.sub(
            "<[^<]+?>", " ", content
        )  # Remove HTML tags (and keep content)

        ## Keyword extraction
        extract_features_from_text(stripped_html, "content")

        # Process spoiler text
        extract_features_from_text(status["spoiler_text"], "spoiler")

        # Process tags
        for tag in status["tags"]:
            features["tag" + "#" + tag.lower()] = 1

        # Process others
        features["media"] = len(status["media_attachments"])
        features["sensitive"] = int(status["sensitive"])
        features["mentions"] = len(status["mentions"])

        return features
