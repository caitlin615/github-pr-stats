build:
	docker build -t pr-stats --rm .

run:
	docker run --rm -it --env-file=.env -v `pwd`:/app pr-stats

shell:
	docker run --rm -it --env-file=.env -v `pwd`:/app pr-stats sh

.PHONY: build run shell
