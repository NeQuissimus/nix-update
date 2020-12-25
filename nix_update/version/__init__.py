from urllib.parse import urlparse

from ..errors import VersionError
from ..utils import extract_version
from .github import fetch_github_version
from .gitlab import fetch_gitlab_version
from .pypi import fetch_pypi_version
from .rubygems import fetch_rubygem_version

# def find_repology_release(attr) -> str:
#    resp = urllib.request.urlopen(f"https://repology.org/api/v1/projects/{attr}/")
#    data = json.loads(resp.read())
#    for name, pkg in data.items():
#        for repo in pkg:
#            if repo["status"] == "newest":
#                return repo["version"]
#    return None


fetchers = [
    fetch_pypi_version,
    fetch_github_version,
    fetch_gitlab_version,
    fetch_rubygem_version,
]


def fetch_latest_version(url_str: str, version_regex: str) -> str:
    url = urlparse(url_str)

    for fetcher in fetchers:
        version = fetcher(url, version_regex)
        if version is not None:
            extracted = extract_version(version, version_regex)
            if extracted is not None:
                return extracted

    raise VersionError(
        "Please specify the version. We can only get the latest version from github/gitlab/pypi/rubygems projects right now"
    )
