import random
from utils import ReviewItem, SummarizedItem
from typing import Optional, Literal


class SummarizeApp:
    def __init__(self):
        pass

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
        return SummarizedItem(summarized_comment="Base model", confidence=0.5)

    def run_complex(self, item: ReviewItem) -> SummarizedItem:
        return SummarizedItem(summarized_comment="Complex model", confidence=0.7)

    def log(self):
        pass
