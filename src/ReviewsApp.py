import random
from utils import ReviewItem, SummarizedItem
from typing import Optional, Literal
from translate_module import Translator
from summary_module import SummaryGenerator


class SummarizeApp:
    def __init__(self):
        complex_model_name = "VisteK528/facebook-bart-cnn-ium-v1"
        base_model_name = "Falconsai/text_summarization"
        self._translator = Translator()
        self._translator.setup("translator_config")
        self._base_model = SummaryGenerator(base_model_name)
        self._complex_model = SummaryGenerator(complex_model_name)

    def __call__(self, item: ReviewItem, model: Optional[Literal["base", "complex"]] = None):
        result: SummarizedItem = SummarizedItem()
        if model is None:
            model = random.choice(["base", "complex"])
        if model == "base":
            result = self.run_base(item)
        elif model == "complex":
            result = self.run_complex(item)
        else:
            print("TODO something failed")

        self.log()
        return result

    def run_base(self, item: ReviewItem) -> SummarizedItem:
        translated = self._translator(item.comment)
        item.comment = translated.translation
        return self._base_model(item)

    def run_complex(self, item: ReviewItem) -> SummarizedItem:
        translated = self._translator(item.comment)
        item.comment = translated.translation
        return self._complex_model(item)

    def log(self):
        pass
