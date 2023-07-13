from argparse import ArgumentParser
from pathlib import Path

from dotenv import load_dotenv
from os import environ as os_environ


BSKY_SUFFIX = ".bsky.social"


def parse_args():
    argp = ArgumentParser("Bsky Scraper")

    argp.add_argument("-a", "--actor", type=str, required=True)
    argp.add_argument("-d", "--dotenv", action="store_true", required=False)
    argp.add_argument("-l", "--limit", type=int, default=25)
    argp.add_argument("-u", "--username", type=str, required=False)
    argp.add_argument("-p", "--password", type=str, required=False)

    argp.add_argument("-j", "--json", type=str)
    argp.add_argument("-v", "--verbose", action="store_true")

    argp.add_argument("--follows", action="store_true")
    argp.add_argument("--followers", action="store_true")

    args = argp.parse_args()

    if args.json and not Path(args.json).parent.exists():
        if args.verbose:
            print(f"Creating save-as folder: {args.json}")
        
        Path(args.json).parent.mkdir(parents=True)

    if not args.actor.endswith(BSKY_SUFFIX):
        args.actor += BSKY_SUFFIX

    if args.dotenv:
        load_dotenv()

        args.username = os_environ["BSKY_USERNAME"]
        args.password = os_environ["BSKY_PASSWORD"]

        del os_environ["BSKY_USERNAME"]
        del os_environ["BSKY_PASSWORD"]

        if not args.username.endswith(BSKY_SUFFIX):
            args.username += BSKY_SUFFIX

    return args
