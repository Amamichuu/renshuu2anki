import re
from app.models.sentence import Sentence


def remove_noise_parentheses(text: str) -> str:
    """
    Remove only long explanatory annotations from Renshuu.
    Keeps grammar examples intact.
    """
    return re.sub(r"（[^）]{6,}）", "", text)


def normalize_japanese(text: str) -> str:
    """
    Lightweight normalization for Anki:
    - removes Renshuu noise
    - converts full-width parentheses content into natural form
    - removes formatting spaces
    """

    # 1. Remove long noise annotations
    text = remove_noise_parentheses(text)

    # 2. Keep grammar inside parentheses, remove brackets only
    # Example: （のに） → のに
    text = re.sub(r"[（(]([^）)]*?)[）)]", r"\1", text)

    # 3. Remove API formatting spaces
    text = re.sub(r"\s+", "", text)

    return text.strip()


def parse_list(data: dict) -> list[Sentence]:
    """
    Converts Renshuu API response into clean Anki sentences.
    """

    terms = data["contents"]["terms"]
    sentences = []

    for item in terms:
        sentences.append(
            Sentence(
                japanese=normalize_japanese(item["japanese"]),
                english=item["meaning"]["eng"],
                source=item["id"]
            )
        )

    return sentences