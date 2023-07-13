#!/usr/bin/env python

import json
import sys

from pathlib import Path
from typing import Dict

from atproto.exceptions import UnauthorizedError

import context  # pylint: disable=unused-import

# pylint: disable=no-name-in-module,import-error
from lib.arguments import parse_args
from lib.skyscraper import BskyClient


def save_to_json(pathname: str, data: Dict) -> None:
    saveas = Path(pathname)
    saveas.write_text(json.dumps(data), encoding="utf8")


def main():
    args = parse_args()

    bsky = BskyClient()

    try:
        bsky.login(args.username, args.password)
    except UnauthorizedError as error:
        print(error.content)
        sys.exit(1)

    if args.followers:
        followers = bsky.get_followers(actor=args.actor, limit=args.limit)

        if args.json:
            save_to_json(args.json, followers)
        else:
            print(json.dumps(followers, indent=4))
        
        if args.verbose:
            print(f"{args.actor} is folloed by {len(followers)} accounts.")

    if args.follows:
        follows = bsky.get_follows(actor=args.actor, limit=args.limit)
        if args.json:
            save_to_json(args.json, follows)
        else:
            print(json.dumps(follows, indent=4))
        
        if args.verbose:
            print(f"{args.actor} follows {len(follows)} accounts.")

    # TODO: expand functionality:
    # - blocks:
    # - list
    # - list_mutes
    # - mutes


if __name__ == "__main__":
    main()
