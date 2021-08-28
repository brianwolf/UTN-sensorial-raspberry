VERSION ?= local
DOCKER_USER ?= utnsensorial
LOG_FILE_PATH ?= ~/.sensorial/logs/app.log
DB_FILE_PATH ?= ~/.sensorial/db/sqlite.db

.SILENT:

logs-tail l:
	tail -f $(LOG_FILE_PATH)


logs-clean lc:
	rm -fr $(LOG_FILE_PATH).*
	> $(LOG_FILE_PATH)


db-clean dbc:
	> $(DB_FILE_PATH)


db-size dbs:
	du -ha $(DB_FILE_PATH)


docker-run r:
	docker run -it --rm -p 80:80 ${DOCKER_USER}/sensorial-raspberry:${VERSION}


docker-build b:
	docker build . -t ${DOCKER_USER}/sensorial-raspberry:${VERSION} --build-arg ARG_VERSION=${VERSION}


docker-build-arm bx:
	docker buildx build . -t ${DOCKER_USER}/sensorial-raspberry:${VERSION} --build-arg ARG_VERSION=${VERSION} --platform linux/amd64,linux/arm/v6,linux/arm/v7,linux/arm64/v8


python-env pye:
	virtualenv -p python3.9 env