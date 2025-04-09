

URL: str = "http://127.0.0.1:8000/"

class Target:
    """
    Registered sender of a sender
    """
    def __init__(self, name: str, url: str = URL):
        self._name: str = name
        self._url = url if url.endswith("/") else url + "/"

    @property
    def name(self) -> str:
        """Name of the """
        return self._name

    @property
    def base_url(self) -> str:
        return self._url

    @property
    def url(self) -> str:
        return self._url + self._name

    def __str__(self) -> str:
        return f"Base URL: {self._url}, name: {self._name}"
