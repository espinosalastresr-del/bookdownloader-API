from urllib.parse import parse_qs
from urllib.parse import urljoin
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from models import Book


class SearchParser:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def parse(self, html: str) -> list[Book]:

        soup = BeautifulSoup(html, "lxml")

        books: list[Book] = []

        for item in soup.select("div.book-item"):

            title = self._text(item, ".book-title a")
            publisher = self._text(item, ".book-publisher")
            author = self._text(item, ".book-author")

            image = item.select_one("img")

            cover = None

            if image:

                cover = urljoin(
                    self.base_url,
                    image.get("data-src") or image.get("src")
                )

            download = item.select_one(".btn-download")

            md5 = ""

            if download:

                href = urljoin(
                    self.base_url,
                    download["href"]
                )

                md5 = parse_qs(
                    urlparse(href).query
                ).get("md5", [""])[0]

            year = None
            language = None
            file_type = None
            size = None

            for span in item.select(".book-details span"):

                text = span.get_text(" ", strip=True)

                strong = span.find("strong")

                if strong is None:
                    continue

                value = strong.get_text(strip=True)

                if text.startswith("Year"):
                    year = value

                elif text.startswith("Language"):
                    language = value

                elif text.startswith("File"):
                    file_type = value

                else:
                    size = value

            books.append(
                Book(
                    id=md5,
                    md5=md5,
                    title=title,
                    author=author,
                    publisher=publisher,
                    year=year,
                    language=language,
                    file_type=file_type,
                    size=size,
                    cover=cover
                )
            )

        return books

    @staticmethod
    def _text(node, selector):

        value = node.select_one(selector)

        if value is None:
            return None

        return value.get_text(strip=True)


class DownloadParser:

    @staticmethod
    def parse(html: str) -> str:

        soup = BeautifulSoup(html, "lxml")

        a = soup.select_one("table#main a[href^='get.php']")

        if a is None:
            raise ValueError("No se encontró el enlace de descarga.")

        return a["href"]