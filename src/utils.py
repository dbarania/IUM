import gc
import torch
from pydantic import BaseModel, Field
import os
from pathlib import Path
from typing import Optional


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


HF_DEFAULT_HOME = os.environ.get("HF_HOME", "~/.cache/huggingface/hub")
ENOUGH_VRAM = os.environ.get("ENOUGH_VRAM", "true") in ('true', "True", 1)


def get_weight_dir(
    model_ref: str,
    *,
    model_dir: str | os.PathLike[str] = HF_DEFAULT_HOME,
    revision: str = "main",
) -> Path:
    """
    Parse model name to locally stored weights.
    Args:
        model_ref (str) : Model reference containing org_name/model_name such as 'meta-llama/Llama-2-7b-chat-hf'.
        revision (str): Model revision branch. Defaults to 'main'.
        model_dir (str | os.PathLike[Any]): Path to directory where models are stored. Defaults to value of $HF_HOME (or present directory)

    Returns:
        str: path to model weights within model directory
    """
    model_dir = Path(model_dir).expanduser()
    assert model_dir.is_dir()
    model_path = model_dir / "--".join(["models", *model_ref.split("/")])
    assert model_path.is_dir()
    snapshot_hash = (model_path / "refs" / revision).read_text()
    weight_dir = model_path / "snapshots" / snapshot_hash
    assert weight_dir.is_dir()
    return weight_dir
