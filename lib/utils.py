import requests

from pathlib import Path
from typing import Union


BSKY_SUFFIX = ".bsky.social"


def append_bsky_domain(actor: str) -> str:
    if not actor.endswith(BSKY_SUFFIX):
        actor += BSKY_SUFFIX
    return actor


def fetch_image(url: str, folder: Union[str, Path]) -> None:
    filename = url.split("/")[-1]
    if "@" in filename:
        filename = filename.replace("@", ".")

    folder = Path(folder)
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)

    resp = requests.get(url, stream=True)
    if resp.status_code == requests.codes.ok:
        with open(f"{folder}/{filename}", "wb") as fp:
            for chunk in resp.iter_content(512):
                fp.write(chunk)
