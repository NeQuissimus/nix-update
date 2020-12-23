import json
import urllib.request
from typing import Optional
from urllib.parse import ParseResult

from ..utils import extract_version, info


def fetch_pypi_version(url: ParseResult, version_extractor: str) -> Optional[str]:
    if url.netloc != "pypi":
        return None
    parts = url.path.split("/")
    package = parts[2]
    pypi_url = f"https://pypi.org/pypi/{package}/json"
    info(f"fetch {pypi_url}")
    resp = urllib.request.urlopen(pypi_url)
    data = json.loads(resp.read())
    version = data["info"]["version"]
    assert isinstance(version, str)
    return extract_version(version, version_extractor)
