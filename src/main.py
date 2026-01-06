from typing import Optional, Literal
from fastapi import FastAPI
from utils import ReviewItem
from ReviewsApp import SummarizeApp
import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO", format="{time} {level} {message}")
logger.add("logs/app.log", rotation="10 MB", level="INFO", format="{time} {level} {message}")
app = FastAPI()
sumapp = SummarizeApp()


@app.post("/summarize")
def summarize(review: ReviewItem, model: Optional[Literal["base", "complex"]] = None):
    return sumapp(review, model)
