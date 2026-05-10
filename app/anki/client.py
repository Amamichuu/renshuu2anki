import requests


class AnkiClient:
    def __init__(self):
        # Local AnkiConnect endpoint (Anki desktop must be running)
        self.url = "http://localhost:8765"

        # Target deck where cards will be created
        self.deck_name = "🇯🇵"

        # Anki note type (must include: Front, Back, RenshuuID fields)
        self.model_name = "Basic"

    def request(self, action, params=None):
        payload = {
            "action": action,
            "version": 6,
            "params": params or {}
        }

        response = requests.post(self.url, json=payload)
        return response.json()

    def note_exists(self, renshuu_id: str) -> bool:
        # Prevent duplicates using RenshuuID as unique key
        # This ensures idempotent sync (no duplicate cards)
        result = self.request("findNotes", {
            "query": f"RenshuuID:{renshuu_id}"
        })

        return len(result.get("result", [])) > 0

    def add_card(self, sentence):
        if self.note_exists(sentence.source):
            return None  # silently skip duplicates

        # Card structure
        payload = {
            "note": {
                "deckName": self.deck_name,
                "modelName": self.model_name,
                "fields": {
                    "Front": sentence.japanese,
                    "Back": sentence.english,

                    # Unique identifier for deduplication
                    "RenshuuID": sentence.source
                },

                # Static tag for future filtering in Anki
                "tags": ["renshuu"]
            }
        }

        response = self.request("addNote", payload)

        return response