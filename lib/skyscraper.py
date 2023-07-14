"""
Bluesky Scraper library.
"""

import time

from dataclasses import asdict, fields
from typing import Callable, Dict, List, Union

from joblib import delayed, Parallel
from random import uniform

from atproto import Client
from atproto.xrpc_client.models.app.bsky.actor.get_profiles import Response

from .types import ActorT, UrlT
from .utils import append_bsky_domain, fetch_image


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

    def get_profile(self, actor: ActorT) -> Response:
        """Get actor profile(s)."""

        if isinstance(actor, List):
            actor = [append_bsky_domain(act) for act in actor]
            return self.client.bsky.actor.get_profiles({"actors": actor})

        actor = append_bsky_domain(actor)
        profile = self.client.bsky.actor.get_profile({"actor": actor})

        return Response(profiles=[profile])

    def get_profile_avatar(
        self,
        *,
        actor: ActorT = None,
        url: UrlT = None,
        folder: str = "downloads",
        threads: int = 4,
    ) -> None:
        if not (actor or url):
            raise ValueError("Neither actor nor URL are specified.")

        if actor:
            resp = self.get_profile(actor)
            url = [prof.avatar for prof in resp.profiles if prof and prof.avatar]

        self.fetch_images(url, folder, threads)

    def get_profile_banner(
        self,
        *,
        actor: ActorT = None,
        url: UrlT = None,
        folder: str = "downloads",
        threads: int = 4,
    ) -> None:
        if not (actor or url):
            raise ValueError("Neither actor nor URL are specified.")

        if actor:
            resp = self.get_profile(actor)
            url = [prof.banner for prof in resp.profiles if prof and prof.banner]

        self.fetch_images(url, folder, threads)
    
    @staticmethod
    def fetch_images(url: UrlT, folder: str, threads: int = 4) -> None:
        threads = min(len(url), threads)
        
        with Parallel(n_jobs=threads) as jobs:
            jobs(delayed(fetch_image)(_, folder) for _ in url)
