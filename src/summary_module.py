from transformers import pipeline
from utils import ReviewItem, SummarizedItem


class SummaryGenerator:
    def __init__(self, model_name: str) -> None:
        self._model_name = model_name
        self._tokenizer = model_name

        self._model = pipeline("summarization", model=self._model_name, tokenizer=self._tokenizer)

    def __call__(self, review: ReviewItem) -> SummarizedItem:
        assert type(review) == ReviewItem
        summary = self._model(
            review.comment,
            max_length=100,
            min_length=20,
            do_sample=False
        )

        return SummarizedItem(summarized_comment=summary[0]['summary_text'], confidence=0.0)

if __name__ == "__main__":
    text = "Tim and Pippa are lovely, so welcoming and friendly. It’s an excellent location for getting into town as it’s just around the corner from the tube. They also provided a great breakfast with homemade jam! Things to note are a comfy bed and great private bathroom. We’re looking forward to going back to stay next week!"
    item = ReviewItem(comment=text, rate=5)
    model = SummaryGenerator("VisteK528/facebook-bart-cnn-ium-v1")
    out = model(item)
    print(out.summarized_comment)