.PHONY: docker docker-run

 
docker:
	docker buildx build --platform linux/amd64 .
	docker buildx build --load --platform linux/amd64 -t bsky.social/scraper .

docker-run:
	docker run -it --rm bsky.social/scraper
