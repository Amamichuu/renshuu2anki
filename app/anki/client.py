import requests
import os


class AnkiClient:
    def __init__(self):
        # Local AnkiConnect endpoint (Anki desktop must be running)
        self.url = "http://localhost:8765"

        # Target deck where cards will be created (configurable)
        self.deck_name = os.getenv("ANKI_DECK_NAME", "🇯🇵")

        # Anki note type (must include: Front, Back, RenshuuID fields)
        self.model_name = "Basic"

        # Ensure deck exists before syncing cards
        self._ensure_deck_exists()

    def request(self, action, params=None):
        payload = {
            "action": action,
            "version": 6,
            "params": params or {}
        }

        response = requests.post(self.url, json=payload)
        return response.json()

    def _ensure_deck_exists(self):
        # Creates the deck if it does not already exist
        self.request("createDeck", {"deck": self.deck_name})

    def note_exists(self, renshuu_id: str) -> bool:
        # Prevent duplicates using RenshuuID as unique key
        # Ensures idempotent sync (safe to re-run anytime)
        result = self.request("findNotes", {
            "query": f"RenshuuID:{renshuu_id}"
        })

        return len(result.get("result", [])) > 0

    def add_card(self, sentence):
        # Skip if already exists (deduplication layer)
        if self.note_exists(sentence.source):
            return None

        # Anki note structure
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

                # Static tag for filtering and organization
                "tags": ["renshuu"]
            }
        }

        response = self.request("addNote", payload)
        return response