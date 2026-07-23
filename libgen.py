from urllib.parse import urljoin

from curl_cffi import requests

from app.config import get_settings
from app.exceptions import BookNotFound
from app.parser import DownloadParser
from app.parser import SearchParser


class LibGenClient:

    def __init__(self):

        self.settings = get_settings()

        self.session = requests.Session()

        self.search_parser = SearchParser(
            self.settings.BASE_URL
        )

    def _get(self, url: str, **kwargs):

        kwargs.setdefault(
            "impersonate",
            self.settings.USER_AGENT
        )

        kwargs.setdefault(
            "timeout",
            self.settings.TIMEOUT
        )

        response = self.session.get(
            url,
            **kwargs
        )

        response.raise_for_status()

        return response

    # -----------------------------------

    # Buscar libros

    # -----------------------------------

    def search(self, query: str):

        params = {
            "mode": "fulltext",
            "q": query
        }

        response = self._get(
            f"{self.settings.BASE_URL}/search.php",
            params=params
        )

        return self.search_parser.parse(
            response.text
        )

    # -----------------------------------

    # Obtener GET

    # -----------------------------------

    def get_download_link(
        self,
        md5: str
    ) -> str:

        response = self._get(
            f"{self.settings.DOWNLOAD_URL}/ads.php",
            params={
                "md5": md5
            }
        )

        href = DownloadParser.parse(
            response.text
        )

        return urljoin(
            self.settings.DOWNLOAD_URL,
            href
        )

    # -----------------------------------

    # Stream

    # -----------------------------------

    def download(self, md5: str):

        url = self.get_download_link(md5)

        response = self._get(
            url,
            stream=True
        )

        return response

    # -----------------------------------

    # Portada

    # -----------------------------------

    def cover(self, md5: str):

        url = (
            f"{self.settings.BASE_URL}"
            f"/cover.php?md5={md5}"
        )

        response = self._get(
            url,
            stream=True
        )

        return response

    # -----------------------------------

    # Libro

    # -----------------------------------

    def get_book(
        self,
        md5: str
    ):

        books = self.search(md5)

        for book in books:

            if book.md5 == md5:
                return book

        raise BookNotFound()