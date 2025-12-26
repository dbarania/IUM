from pydantic import BaseModel, Field


class ReviewItem(BaseModel):
    comment: str
    rate: int


class SummarizedItem(BaseModel):
    summarized_comment: str = Field(default="")
    confidence: float = Field(default=0.0)
