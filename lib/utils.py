import requests

from pathlib import Path


def fetch_image(url: str, folder: str) -> None:
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
