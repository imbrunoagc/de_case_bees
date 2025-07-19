import os
from dotenv import load_dotenv

load_dotenv('.env')

class Settings:
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", 1.0))
    PER_PAGE = int(os.getenv("PER_PAGE", 200))
    BASE_URL = os.getenv("BASE_URL", None)

    ENDEPOINTS = {
        "base": BASE_URL,
        "meta": f"{BASE_URL}/meta"
    }

settings = Settings()
print(settings.BASE_URL)