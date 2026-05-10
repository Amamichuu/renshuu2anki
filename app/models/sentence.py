from pydantic import BaseModel

class Sentence(BaseModel):
    japanese: str
    english: str
    source: str  # Renshuu unique ID (required)