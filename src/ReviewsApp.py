import random
from utils import ReviewItem, SummarizedItem
from typing import Optional, Literal
from translate_module import Translator
from summary_module import SummaryGenerator
from loguru import logger


class SummarizeApp:
    def __init__(self):
        base_model_name = "facebook--bart-large-cnn"
        complex_model_name = "VisteK528--facebook-bart-cnn-ium-v3"
        self._translator = Translator()
        self._translator.setup("translator_config")
        self._base_model = SummaryGenerator(base_model_name)
        logger.info("Base model loaded")
        self._complex_model = SummaryGenerator(complex_model_name)
        logger.info("Complex model loaded")
        logger.info("Application initialized")

    def __call__(self, item: ReviewItem, model: Optional[Literal["base", "complex"]] = None):
        result: SummarizedItem = SummarizedItem()
        if model is None:
            model = random.choice(["base", "complex"])
        if model == "base":
            result = self.run_base(item)
        elif model == "complex":
            result = self.run_complex(item)
        else:
            logger.error(f"Something failed | model set {model} | input {ReviewItem}")

        return result

    def run_base(self, item: ReviewItem) -> SummarizedItem:
        item_src = item.comment
        translated = self._translator(item.comment)
        item.comment = translated.translation
        summary = self._base_model(item)
        logger.info(
            f"[user]:[base]|{item_src}|{item.rate}|{translated.translation}|{translated.source_alphabet}|{translated.source_language}|{summary.summarized_comment}|{summary.confidence}")
        return summary

    def run_complex(self, item: ReviewItem) -> SummarizedItem:
        item_src = item.comment
        translated = self._translator(item.comment)
        item.comment = translated.translation
        summary = self._complex_model(item)
        logger.info(
            f"[user]:[complex]|{item_src}|{item.rate}|{translated.translation}|{translated.source_alphabet}|{translated.source_language}|{summary.summarized_comment}|{summary.confidence}")
        return summary

    def log(self):
        pass
