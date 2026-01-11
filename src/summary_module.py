from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from utils import ReviewItem, SummarizedItem, force_cleanup, get_weight_dir


class SummaryGenerator:
    def __init__(self, model_name: str) -> None:
        self._model_name = model_name
        weights_dir = get_weight_dir(model_name)
        self._tokenizer = AutoTokenizer.from_pretrained(weights_dir)
        self._model = AutoModelForSeq2SeqLM.from_pretrained(weights_dir)
        self._model.to("cpu")

    def __call__(self, review: ReviewItem) -> SummarizedItem:
        assert type(review) == ReviewItem
        self._model.to("cuda")

        inputs = self._tokenizer(
            review.comment,
            return_tensors="pt",
            max_length=1024,
            truncation=True
        ).to("cuda")
        summary_ids = self._model.generate(
            inputs["input_ids"],
            max_length=100,
            min_length=20,
            do_sample=False,
            num_beams=4,
            num_return_sequences=1,
            early_stopping=True,
            length_penalty = 2.0,
            no_repeat_ngram_size=3
        )

        summary = self._tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        self._model.to("cpu")
        force_cleanup()

        return SummarizedItem(summarized_comment=summary, confidence=0.0)
