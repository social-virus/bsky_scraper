"""
Bluesky Scraper library.
"""

import json
import time

from dataclasses import asdict, fields
from typing import Callable, Dict
from random import uniform

from atproto import Client


BSKY_SUFFIX = ".bsky.social"


class BskyClient:
    """Bsky Client class."""

    def __init__(self):
        self.client = Client()

    def login(self, username: str, password: str):
        """Log into bsky. Allow convenient use of shorthand name."""

        if not username.endswith(BSKY_SUFFIX):
            username += BSKY_SUFFIX
        self.client.login(username, password)

    @staticmethod
    def get_data(response):
        """Convenience function for pulling data fields from responses."""

        return getattr(response, fields(response)[0].name)

    def looping_caller(self, callee: Callable[[Dict], Dict], params: Dict):
        """Ureasonable use of black magic."""

        resp = callee(params)
        data = self.get_data(resp)

        while resp.cursor is not None:
            time.sleep(uniform(0.15, 2.95))
            params["cursor"] = resp.cursor
            resp = callee(params)
            data.extend(self.get_data(resp))

        return [asdict(datum) for datum in data]

    def get_followers(self, actor: str, limit: int = 50):
        """Scrape followers."""

        params = {
            "actor": actor,
            "limit": limit,
        }

        graph = self.client.bsky.graph

        return self.looping_caller(graph.get_followers, params)

    def get_follows(self, actor: str, limit: int = 50):
        """Scrape follows."""

        params = {
            "actor": actor,
            "limit": limit,
        }

        graph = self.client.bsky.graph

        return self.looping_caller(graph.get_follows, params)
