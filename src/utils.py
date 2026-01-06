import gc
import torch
from pydantic import BaseModel, Field



class ReviewItem(BaseModel):
    comment: str
    rate: int


class TranslatedItem(BaseModel):
    translation: str
    source_language: str
    source_alphabet: str


class SummarizedItem(BaseModel):
    summarized_comment: str = Field(default="")
    confidence: float = Field(default=0.0)

def force_cleanup():
    """Aggressively frees GPU memory."""
    gc.collect()
    torch.cuda.empty_cache()