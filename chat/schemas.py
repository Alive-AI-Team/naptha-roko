from pydantic import BaseModel
from enum import Enum


class Model(str, Enum):
    MISTRAL = "mistral"
    GEMMA = "gemma"
    QWEN = "qwen"
    PHI = "phi"
    LLAMA3 = "llama3"


class InputSchema(BaseModel):
    prompt: str
    model: Model = Model.MISTRAL
