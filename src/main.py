from typing import Optional, Literal
from fastapi import FastAPI
from utils import ReviewItem
from ReviewsApp import SummarizeApp

app = FastAPI()
sumapp = SummarizeApp()

@app.post("/summarize")
def summarize(review: ReviewItem, model: Optional[Literal["base", "complex"]] = None):
    return sumapp(review, model)
