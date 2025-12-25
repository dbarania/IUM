from typing import Optional, Literal
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.post("/summarize")
def summarize(model: Optional[Literal["original", "testing"]] = None):
    if model is None:
        return {"model": "Model is empty"}
    return {"model": model}
