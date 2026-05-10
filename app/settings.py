import os
from dotenv import load_dotenv

load_dotenv()

RENSHUU_API_KEY = os.getenv("RENSHUU_API_KEY")
if not RENSHUU_API_KEY:
    raise RuntimeError(
        "Missing required environment variable 'RENSHUU_API_KEY'. "
        "Set it in your environment or in a .env file, for example: "
        "RENSHUU_API_KEY=your_api_key_here"
    )
RENSHUU_BASE_URL = "https://api.renshuu.org/v1"