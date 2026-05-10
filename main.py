import logging
from app.services.renshuu_anki_sync_service import RenshuuAnkiSyncService

# Renshuu list ID used as the source of sentences to sync
RENSHUU_LIST_ID = 10626774

logger = logging.getLogger(__name__)


def main():
    service = RenshuuAnkiSyncService()

    logger.info("Starting sync...")

    results = service.sync_list(RENSHUU_LIST_ID)

    for sentence, result in results:

        # Case 1: duplicate (skipped intentionally)
        if result is None:
            logger.info(f"Skipped duplicate: {sentence}")
            continue

        # Case 2: AnkiConnect error
        if result.get("error"):
            logger.warning(f"Failed: {sentence} -> {result}")
            continue

        # Case 3: success
        logger.info(f"Added: {sentence}")

    logger.info("Sync finished.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    main()