import requests
import logging
from app.settings import RENSHUU_API_KEY, RENSHUU_BASE_URL

logger = logging.getLogger(__name__)


class RenshuuClient:
    def get_list(self, list_id: int):
        # Build endpoint for fetching a specific Renshuu list
        url = f"{RENSHUU_BASE_URL}/list/{list_id}"

        headers = {
            "Authorization": f"Bearer {RENSHUU_API_KEY}"
        }

        logger.info(f"Requesting Renshuu list: {list_id}")

        try:
            # Timeout prevents hanging requests
            response = requests.get(url, headers=headers, timeout=10)

            logger.debug(f"Status: {response.status_code}")

            if response.status_code != 200:
                logger.error(f"Error response: {response.text}")

            response.raise_for_status()

            logger.info("List fetched successfully")

            return response.json()

        except requests.exceptions.Timeout:
            logger.error("Request to Renshuu API timed out")
            raise

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while requesting Renshuu API: {e}")
            raise