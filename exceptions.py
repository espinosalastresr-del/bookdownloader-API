class LibGenException(Exception):
    """Excepción base."""


class SearchError(LibGenException):
    """Error al buscar libros."""


class DownloadError(LibGenException):
    """Error al descargar un libro."""


class BookNotFound(LibGenException):
    """Libro no encontrado."""


class InvalidResponse(LibGenException):
    """HTML inesperado."""