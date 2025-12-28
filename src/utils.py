from pydantic import BaseModel, Field


class ReviewItem(BaseModel):
    comment: str
    rate: int


class SummarizedItem(BaseModel):
    summarized_comment: str = Field(default="")
    confidence: float = Field(default=0.0)


class TranslatedItem(BaseModel):
    translation: str
    source_language: str
    source_alphabet: str
