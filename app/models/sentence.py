from pydantic import BaseModel

class Sentence(BaseModel):
    japanese: str
    english: str
    source: str | None = None