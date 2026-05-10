from app.renshuu.client import RenshuuClient
from app.renshuu.parser import parse_list
from app.anki.client import AnkiClient


class RenshuuAnkiSyncService:
    def __init__(self):
        # External API client (Renshuu data source)
        self.renshuu = RenshuuClient()

        # Anki integration client (creates flashcards via AnkiConnect)
        self.anki = AnkiClient()

    def sync_list(self, list_id: int):
        """
        Main orchestration flow:
        Renshuu list → parsed sentences → Anki cards
        """

        raw = self.renshuu.get_list(list_id)

        sentences = parse_list(raw)

        results = []

        for s in sentences:

            result = self.anki.add_card(s)

            results.append((s.japanese, result))

        return results