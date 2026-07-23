from functools import lru_cache

from dotenv import load_dotenv

import os

load_dotenv()


class Settings:

    APP_NAME: str = os.getenv("APP_NAME", "Book API")

    VERSION: str = os.getenv("APP_VERSION", "0.1.0")

    BASE_URL: str = os.getenv(
        "BASE_URL",
        "https://libgen.com.de"
    )

    DOWNLOAD_URL: str = os.getenv(
        "DOWNLOAD_URL",
        "https://libgen.li"
    )

    USER_AGENT: str = os.getenv(
        "USER_AGENT",
        "chrome"
    )

    TIMEOUT: int = int(
        os.getenv("REQUEST_TIMEOUT", 30)
    )


@lru_cache
def get_settings():

    return Settings()