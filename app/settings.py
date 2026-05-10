import os
from dotenv import load_dotenv

load_dotenv()

RENSHUU_API_KEY = os.getenv("RENSHUU_API_KEY")
RENSHUU_BASE_URL = "https://api.renshuu.org/v1"