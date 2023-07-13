Simple example usage:

```
# create a .env file with your credentials (don't leak secrets)

cat <<__EOF__> .env
BSKY_USERNAME=<YOUR_BSKY_USERNAME>
BSKY_PASSWORD=<YOUR_BSKY_PASSWORD>
__EOF__

./scripts/scraper.py -a socialvirus -d --follows -j data/socialvirus-follows.json -v
./scripts/scraper.py -a socialvirus -d --followers -j data/socialvirus-followers.json -v
```
