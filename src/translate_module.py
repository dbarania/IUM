import csv
import os
from langdetect import detect
from alphabet_detector.alphabet_detector import AlphabetDetector
from utils import TranslatedItem, force_cleanup
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, BitsAndBytesConfig
import torch
from loguru import logger
from utils import get_weight_dir


class Translator:
    _ad = AlphabetDetector()

    def __init__(self):
        self._config_path = ""
        self._language_map: dict | None = None
        self._tokenizer = None
        self._model = None

    def __call__(self, text: str):
        lang, alph = self.id_text(text)
        source_code = self._language_map.get((lang, alph), "")
        translated_text = ""
        if source_code != "":
            translated_text = self.translate(text, source_code)
        else:
            logger.warning(f"[lang codes failure]:{text} | {lang} | {alph}")
        self._model.to("cpu")
        force_cleanup()
        return TranslatedItem(translation=translated_text,
                              source_language=lang,
                              source_alphabet=alph)

    def translate(self, text: str, code: str, target_lang_code="eng_Latn") -> str:

        if code == target_lang_code:
            return text
        self._tokenizer.src_lang = code
        self._model.to("cuda")
        inputs = self._tokenizer(text, return_tensors="pt").to("cuda")

        generated_tokens = self._model.generate(
            **inputs,
            forced_bos_token_id=self._tokenizer.convert_tokens_to_ids(target_lang_code))
        result = self._tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        return result

    def setup(self, config: str):
        self._config_path = config
        self.reload_config()
        weights_dir = get_weight_dir('facebook--nllb-200-distilled-600M')
        self._tokenizer = AutoTokenizer.from_pretrained(weights_dir)
        self._model = AutoModelForSeq2SeqLM.from_pretrained(weights_dir)
        self._model.to("cpu")

    def reload_config(self):
        if os.path.isfile(self._config_path):
            with open(self._config_path, newline='') as csv_file:
                reader = csv.reader(csv_file)
                self._language_map = {(r[0], r[1]): r[2] for r in reader}
            return True
        return False

    @staticmethod
    def _detect_language(text: str) -> str:
        return detect(text)

    @staticmethod
    def _detect_alphabet(text: str) -> str:
        result = Translator._ad.detect_alphabet(text)
        return result.pop()

    def id_text(self, text: str) -> tuple[str, str]:
        lang = self._detect_language(text)
        alph = self._detect_alphabet(text)
        return lang, alph
